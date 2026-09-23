import assert from 'node:assert/strict';
import {mkdir, mkdtemp, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {assertArtifactsFrozen} from '../scripts/assert-artifacts-frozen.mjs';

test('accepts an absent generated artifact directory', async () => {
  const root = await mkdtemp(path.join(tmpdir(), 'mar101-freeze-empty-'));
  await assert.doesNotReject(assertArtifactsFrozen(path.join(root, 'artifacts')));
});

test('blocks publication while report architecture is under review', async () => {
  const root = await mkdtemp(path.join(tmpdir(), 'mar101-freeze-block-'));
  const artifacts = path.join(root, 'artifacts');
  await mkdir(artifacts, {recursive: true});
  await writeFile(path.join(artifacts, 'report.html'), '<html></html>', 'utf8');

  await assert.rejects(
    assertArtifactsFrozen(artifacts),
    /Artifact publication is frozen/,
  );
});
