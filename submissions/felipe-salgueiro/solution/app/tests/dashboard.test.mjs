import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {parseDashboard, selectProfiles} from '../src/lib/dashboard.ts';
const snapshot = JSON.parse(readFileSync(new URL('../../data/app/dashboard.json', import.meta.url), 'utf8'));
test('real snapshot has reconciled numbers and eight evidence-backed actions', () => {
  const data = parseDashboard(snapshot);
  assert.equal(data.overall.rows, 52214);
  assert.equal(data.overall.interaction_per_view_pct.median, 19.8992318886063);
  assert.equal(data.recommendations.length, 8);
  assert.equal(data.sponsorship.positive_cells, 33);
});
test('filter returns the original statistic without recomputing medians', () => {
  const data = parseDashboard(snapshot), selected = selectProfiles(data, {dimension: 'platform', value: 'Instagram'});
  assert.equal(selected.status, 'ready'); assert.equal(selected.rows.length, 1);
  assert.equal(selected.rows[0].interaction_per_view_pct.median, 19.888954987110846);
});
test('unknown value is empty, unsupported cross is not silently calculated', () => {
  const data = parseDashboard(snapshot);
  assert.equal(selectProfiles(data, {value: 'inexistente'}).status, 'empty');
  assert.equal(selectProfiles(data, {platform: 'Instagram', format: 'video'}).status, 'unsupported');
  assert.equal(selectProfiles(data, {dimension: '__proto__'}).status, 'unsupported');
  assert.equal(selectProfiles(data, {dimension: ['platform', 'content_type']}).status, 'unsupported');
});
test('missing evidence fails closed', () => {
  const input = structuredClone(snapshot); input.recommendations[0].evidence_ids = ['absent'];
  assert.throws(() => parseDashboard(input), /sem evidência/);
});
test('wrong units and fabricated commercial values fail closed', () => {
  const input = structuredClone(snapshot); input.metric.unit = 'percentage_points';
  assert.throws(() => parseDashboard(input), /Contrato/);
  input.metric.unit = 'percent'; input.commercial.revenue = 0;
  assert.throws(() => parseDashboard(input), /comercial/);
});
test('invalid numbers fail rather than render misleading values', () => {
  const input = structuredClone(snapshot); input.evidence.find(item => item.id === 'ev-overall').data.rows = NaN;
  assert.throws(() => parseDashboard(input), /Métrica/);
});
