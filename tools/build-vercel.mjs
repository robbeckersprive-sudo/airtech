// Publish the checked-in HTML and assets without exposing source or review files.
import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const output = path.join(root, 'dist');
await rm(output, { recursive: true, force: true });
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
