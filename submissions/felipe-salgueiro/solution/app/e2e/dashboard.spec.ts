import {test, expect} from '@playwright/test';
test('shows audited values, eight actions and readable provenance', async ({page}) => {
  await page.goto('/');
  await expect(page.getByRole('region', {name: 'Panorama geral da base'})).toContainText('52.214');
  await expect(page.getByRole('region', {name: 'Panorama geral da base'})).toContainText('19,899%');
  await expect(page.locator('.decision-card')).toHaveCount(8);
  const first = page.locator('#rec-q1');
  await first.getByText('Conferir evidência e regra').click();
  await expect(first).toContainText('ev-performance');
  await expect(first).toContainText('descriptive-q1-v1');
  await expect(page.getByText('Dados pendentes', {exact: true})).toHaveCount(0);
});
test('valid filter preserves exact values, empty filter has a recovery action', async ({page}) => {
  await page.goto('/?dimension=platform&value=Instagram');
  await expect(page.getByRole('article', {name: 'Instagram', exact: true})).toContainText('19,889%');
  await page.locator('#main-content').getByLabel('Valor exato do recorte').fill('inexistente');
  await page.getByRole('button', {name: 'Aplicar recorte'}).click();
  await expect(page.getByRole('heading', {name: 'Recorte sem registros'})).toBeVisible();
  await page.getByRole('link', {name: 'Limpar filtros e ver a base'}).click();
  await expect(page.getByRole('article', {name: 'Instagram', exact: true})).toBeVisible();
});
test('unsupported cross has no invented filtered metrics', async ({page}) => {
  await page.goto('/?platform=Instagram&format=video');
  await expect(page.getByRole('heading', {name: 'Combinação de filtros não disponível'})).toBeVisible();
  await expect(page.getByRole('article', {name: 'Instagram', exact: true})).toHaveCount(0);
  await expect(page.locator('#main-content').getByText('não mensurados', {exact: true})).toBeVisible();
});
