import assert from 'node:assert/strict';
import test from 'node:test';
import {formatCost, simulateCosts} from '../src/lib/simulator.ts';

const scenario = {cost: 2000, views: 10000, interactions: 2000, sales: 20,
  costBasis: 'campaign', metricsBasis: 'campaign', costPeriod: 'semana-1', metricsPeriod: 'semana-1'};

test('calculates hypothetical unit costs: R$ 2000 / 20 sales = R$ 100', () => {
  const result = simulateCosts(scenario);
  assert.deepEqual(result.errors, []);
  assert.equal(result.hypothetical, true);
  assert.equal(result.costPerThousandViews.value, 200);
  assert.equal(result.costPerInteraction.value, 1);
  assert.equal(result.costPerSale.value, 100);
  assert.equal('cac' in result, false);
});

test('zero cost with positive denominators is a valid zero', () => {
  assert.equal(simulateCosts({...scenario, cost: 0}).costPerSale.value, 0);
});

test('missing values remain unavailable instead of becoming zero', () => {
  for (const key of ['cost', 'views', 'interactions', 'sales']) {
    const result = simulateCosts({...scenario, [key]: null});
    const selected = {cost: 'costPerSale', views: 'costPerThousandViews',
      interactions: 'costPerInteraction', sales: 'costPerSale'}[key];
    assert.equal(result[selected].status, 'unavailable');
    assert.equal(result[selected].value, null);
  }
});

test('zero denominators never produce Infinity or zero costs', () => {
  const result = simulateCosts({...scenario, views: 0, interactions: 0, sales: 0});
  for (const key of ['costPerThousandViews', 'costPerInteraction', 'costPerSale']) {
    assert.equal(result[key].value, null);
  }
  assert.match(result.costPerSale.reason, /Sem vendas/);
});

test('rejects negative, NaN, infinite and string values at runtime', () => {
  for (const key of ['cost', 'views', 'interactions', 'sales']) {
    for (const invalid of [-1, NaN, Infinity, -Infinity, '2000', undefined]) {
      const result = simulateCosts({...scenario, [key]: invalid});
      assert.ok(result.errors.length > 0);
      assert.equal(result.costPerSale.value, null);
    }
  }
});

test('sales must be safe whole counts', () => {
  for (const sales of [0.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.ok(simulateCosts({...scenario, sales}).errors.length);
  }
});

test('validation names are readable in Portuguese', () => {
  for (const [key, name] of Object.entries({cost: 'Custo', views: 'Visualizações', interactions: 'Interações', sales: 'Vendas'})) {
    assert.equal(simulateCosts({...scenario, [key]: -1}).errors[0], `${name}: informe um número finito não negativo.`);
  }
  assert.match(simulateCosts({...scenario, sales: 1.5}).errors[0], /^Vendas: use uma quantidade inteira/);
});

test('refuses mixing per-post reference with campaign investment', () => {
  assert.ok(simulateCosts({...scenario, metricsBasis: 'post'}).errors.length);
  assert.ok(simulateCosts({...scenario, costBasis: 'unknown', metricsBasis: 'unknown'}).errors.length);
});

test('requires matching nonempty periods', () => {
  for (const metricsPeriod of ['semana-2', '', null, undefined]) {
    assert.ok(simulateCosts({...scenario, metricsPeriod}).errors.length);
  }
});

test('keeps precision until currency display and handles overflow', () => {
  const result = simulateCosts({...scenario, cost: 1, sales: 3});
  assert.equal(result.costPerSale.value, 1 / 3);
  assert.match(formatCost(result.costPerSale), /0,33/);
  const extreme = simulateCosts({...scenario, cost: Number.MAX_VALUE, views: 0.01});
  assert.equal(extreme.costPerThousandViews.value, null);
  assert.match(formatCost(extreme.costPerThousandViews), /limite numérico/);
});

test('does not mutate input and works without services', () => {
  const input = Object.freeze({...scenario});
  assert.deepEqual(simulateCosts(input), simulateCosts(input));
  assert.deepEqual(input, scenario);
});
