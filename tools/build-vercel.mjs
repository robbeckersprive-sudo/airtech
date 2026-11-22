// Publish the checked-in HTML and assets without exposing source or review files.
import { cp, mkdir, readdir, rm, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { transform } from 'esbuild';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const output = path.join(root, 'dist');
if (path.dirname(output) !== root.replace(/[\\/]$/, '')) throw new Error('Build output must stay inside the project.');
try {
  await rm(output, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
} catch (error) {
  if (!['EPERM', 'ENOTEMPTY'].includes(error.code)) throw error;
  // Windows may retain an open directory handle. Clear files without requiring
  // removal of the directory itself; stale published files must never survive.
  async function clearFiles(directory) {
    for (const entry of await readdir(directory, {withFileTypes:true})) {
      const file=path.join(directory,entry.name);
      if (entry.isDirectory()) await clearFiles(file);
      else await rm(file,{force:true,maxRetries:5,retryDelay:200});
    }
  }
  await clearFiles(output);
}
await mkdir(output, { recursive: true });
let pages = 0;
for (const entry of await readdir(root, { withFileTypes: true })) {
  if (entry.isFile() && /\.html?$/.test(entry.name)) {
    await cp(path.join(root, entry.name), path.join(output, entry.name));
    pages++;
  }
}
for (const folder of ['assets', 'images', 'images-flow-groen']) {
  await cp(path.join(root, folder), path.join(output, folder), { recursive: true });
}
console.log(`Prepared ${pages} HTML pages and website assets in dist/.`);

// Bundle styles per page, preserving the original cascade and relative font/image URLs.
const bundles = new Map();
async function readStyles(file, ancestors = []) {
  if (ancestors.includes(file)) throw new Error(`Circular CSS import: ${file}`);
  let source = await readFile(file, 'utf8');
  const imports = [...source.matchAll(/@import\s+(?:url\(\s*)?['"]([^'"]+)['"]\s*\)?\s*;/g)];
  for (const match of imports) {
    const imported = path.resolve(path.dirname(file), match[1]);
    if (path.dirname(imported) !== path.dirname(file)) throw new Error(`Unsupported CSS import: ${match[1]}`);
    source = source.replace(match[0], await readStyles(imported, [...ancestors, file]));
  }
  if (/@import\b/.test(source)) throw new Error(`Unresolved CSS import in ${file}`);
  return source;
}
for (const entry of await readdir(output)) {
  if (!/\.html?$/.test(entry)) continue;
  const file = path.join(output, entry);
  let html = await readFile(file, 'utf8');
  const pattern = /<link rel="stylesheet" href="(assets\/css\/[^"?]+)(?:\?[^"\s]*)?">/g;
  const matches = [...html.matchAll(pattern)];
  if (matches.length) {
    const key = matches.map(m => m[1]).join('|');
    let bundle = bundles.get(key);
    if (!bundle) {
      const sources = await Promise.all(matches.map(m => readStyles(path.join(root, m[1]))));
      const {code} = await transform(sources.join('\n'), {loader:'css', minify:true, target:['chrome109','safari16.4','firefox115']});
      bundle = `assets/css/page-${createHash('sha256').update(code).digest('hex').slice(0,12)}.css`;
      await writeFile(path.join(output,bundle),code);
      bundles.set(key,bundle);
    }
    let first = true;
    html = html.replace(pattern, () => { if (!first) return ''; first=false; return `<link rel="stylesheet" href="${bundle}">`; });
    await writeFile(file,html);
  }
}
for (const entry of await readdir(path.join(output,'assets/js'))) {
  if (!entry.endsWith('.js') || entry === 'rotor3d.js') continue;
  const file = path.join(output,'assets/js',entry);
  const {code} = await transform(await readFile(file,'utf8'), {loader:'js', minify:true, target:'es2020', legalComments:'eof'});
  await writeFile(file,code);
}
console.log(`Minified JavaScript and created ${bundles.size} page stylesheet bundles.`);
