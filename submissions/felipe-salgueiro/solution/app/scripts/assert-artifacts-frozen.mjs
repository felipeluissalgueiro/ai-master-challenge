import {readdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

export async function assertArtifactsFrozen(artifactsRoot) {
  let entries;
  try {
    entries = await readdir(artifactsRoot);
  } catch (error) {
    if (error && typeof error === 'object' && error.code === 'ENOENT') {
      return;
    }
    throw error;
  }

  if (entries.length > 0) {
    throw new Error(
      `Artifact publication is frozen; remove generated files from ${artifactsRoot} and wait for the approved handoff.`,
    );
  }
}

const scriptPath = fileURLToPath(import.meta.url);
if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  const appRoot = path.resolve(path.dirname(scriptPath), '..');
  await assertArtifactsFrozen(path.join(appRoot, 'public', 'artifacts'));
  console.log('Artifact publication freeze verified.');
}
