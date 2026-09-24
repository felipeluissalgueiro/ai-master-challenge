import {readFile, writeFile, mkdir, readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

// Exact reviewed handoff. No directory copy: SQLite and other sources cannot enter public/.
export const ARTIFACTS = {
  'reports/performance-strategy.html': '754a05702142ced9ce80ed5a7939219ae5fb899df3ae14583f5fad3639e54145',
  'reports/evidence.json': 'de0502d33bec4b09fe6970686196f4c83c1fe484b659c40fc607b75d6d1ddf1d',
  'reports/manifest.json': '78cad418d970c335b576cdab9e22363f573301ee6b01d4cd58f5438b2b6d184a',
  'reports/README.md': '4cccf79baeb7f878d007e986bce906980910d6561ae9729e242811c69a706a6a',
  'prototype/index.html': '4bb3b412f47ba9932fe78db3eeeb74a90088b6bee1ff4a559deda090731d767b',
};

export async function prepareArtifacts(solutionRoot, outputRoot) {
  const contents = await Promise.all(Object.entries(ARTIFACTS).map(async ([name, hash]) => {
    const bytes = await readFile(path.join(solutionRoot, name));
    if (createHash('sha256').update(bytes).digest('hex') !== hash) throw Error('Unreviewed artifact: ' + name);
    return [name, bytes];
  }));
  const font = await readFile(path.join(solutionRoot, 'assets/fonts/manrope-latin-variable.woff2.b64'));
  if (createHash('sha256').update(font).digest('hex') !== 'adab05b4f4899a536269273ea0fe507cf735547fa72f26a4d118cbac423fbb67') throw Error('Unreviewed font');
  contents.push(['fonts/manrope.woff2', Buffer.from(font.toString().trim(), 'base64')]);
  const allowed = new Set(contents.map(([name]) => name));
  async function verify(directory, prefix = '') {
    const entries = await readdir(directory, {withFileTypes: true}).catch(error => {
      if (error.code === 'ENOENT') return [];
      throw error;
    });
    for (const entry of entries) {
      const relative = prefix + entry.name;
      if (entry.isDirectory()) await verify(path.join(directory, entry.name), relative + '/');
      else if (!entry.isFile() || !allowed.has(relative)) throw Error('Unexpected public artifact: ' + relative);
    }
  }
  await verify(outputRoot);
  for (const [name, bytes] of contents) {
    const destination = path.join(outputRoot, name);
    await mkdir(path.dirname(destination), {recursive: true});
    await writeFile(destination, bytes);
  }
  return contents.length;
}

const scriptPath = fileURLToPath(import.meta.url);
if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  const appRoot = path.resolve(path.dirname(scriptPath), '..');
  console.log('Verified public artifacts:', await prepareArtifacts(path.resolve(appRoot, '..'), path.join(appRoot, 'public/artifacts')));
}
