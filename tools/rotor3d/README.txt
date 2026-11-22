Real-time 3D rotor for the hero dosing sheet (Nov 22).
Source: rotor3d.src.js (adapted from the supplied doseersluis-3d-pakket, Three.js 0.180.0, MIT: three-LICENSE.txt).
Rebuild: in a folder with "npm install three@0.180.0 esbuild@0.25.11", run
  NODE_PATH=<that folder>/node_modules <that folder>/node_modules/.bin/esbuild tools/rotor3d/rotor3d.src.js --bundle --minify --format=iife --target=es2020 --legal-comments=eof --outfile=assets/js/rotor3d.js
Housing photo: images/33-hero-doseersluis-behuizing-*.{webp,avif} (from doseersluis-behuizing.png).
