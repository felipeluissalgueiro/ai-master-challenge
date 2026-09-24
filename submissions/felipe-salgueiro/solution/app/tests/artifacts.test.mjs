import assert from 'node:assert/strict';
import {mkdtemp, readFile, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import test from 'node:test';
import {ARTIFACTS, prepareArtifacts} from '../scripts/prepare-artifacts.mjs';

const source = fileURLToPath(new URL('../../', import.meta.url));
test('publishes only exact reviewed artifacts and the local font', async () => {
  const destination = await mkdtemp(path.join(tmpdir(), 'g4-artifacts-'));
  assert.equal(await prepareArtifacts(source, destination), 6);
  for (const name of Object.keys(ARTIFACTS)) {
    assert.deepEqual(await readFile(path.join(destination, name)), await readFile(path.join(source, name)));
  }
});
test('refuses unexpected files such as SQLite in the generated public directory', async () => {
  const destination = await mkdtemp(path.join(tmpdir(), 'g4-artifacts-guard-'));
  await writeFile(path.join(destination, 'database.sqlite'), 'not a database');
  await assert.rejects(prepareArtifacts(source, destination), /Unexpected public artifact/);
});
