import {readFile, writeFile, mkdir, readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

// Exact reviewed handoff. No directory copy: SQLite and other sources cannot enter public/.
export const ARTIFACTS = {
  'reports/performance-strategy.html': 'b3f4a9e1cb3a04021926fef6aa3d98910fdefd5a6830cc004b25009194e98f2f',
  'reports/evidence.json': 'de0502d33bec4b09fe6970686196f4c83c1fe484b659c40fc607b75d6d1ddf1d',
  'reports/manifest.json': 'f86dc7edec0e4a6364cecc661b475ff21518e085787eb4687509ba60050236ed',
  'reports/README.md': 'fee0900b5b2f936124e7d6e4e43fa342b04b5127e46ace75837ef8d36f987377',
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
