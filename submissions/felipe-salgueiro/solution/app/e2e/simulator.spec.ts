import {expect, test, type Page} from '@playwright/test';

async function fillScenario(page: Page) {
  await page.goto('/simulador');
  await page.getByLabel('Período do cenário').fill('Semana de teste');
  await page.getByLabel('Custo total (R$)').fill('2000');
  await page.getByLabel('Visualizações estimadas').fill('10000');
  await page.getByLabel('Interações estimadas').fill('2000');
  await page.getByLabel('Vendas atribuídas no cenário', {exact: true}).fill('20');
}

test('starts without invented commercial values', async ({page}) => {
  await page.goto('/simulador');
  await expect(page.getByText('Cenário hipotético.', {exact: true})).toBeVisible();
  for (const label of ['Custo total (R$)', 'Visualizações estimadas', 'Interações estimadas', 'Vendas atribuídas no cenário']) {
    await expect(page.getByLabel(label, {exact: true})).toHaveValue('');
  }
});

test('calculates and invalidates stale results when an input changes', async ({page}) => {
  await fillScenario(page);
  await page.getByRole('button', {name: 'Calcular cenário'}).click();
  const results = page.locator('dl');
  await expect(results).toContainText(/R\$\s*100,00/);
  await expect(results).toContainText(/R\$\s*200,00/);
  await expect(results).toContainText(/R\$\s*1,00/);
  await page.getByLabel('Custo total (R$)').fill('3000');
  await expect(results).toHaveCount(0);
});

test('distinguishes missing sales from zero attributed sales', async ({page}) => {
  await fillScenario(page);
  await page.getByLabel('Vendas atribuídas no cenário', {exact: true}).fill('0');
  await page.getByRole('button', {name: 'Calcular cenário'}).click();
  await expect(page.locator('dl')).toContainText('Sem vendas atribuídas no cenário.');
  await page.getByLabel('Vendas atribuídas no cenário', {exact: true}).fill('');
  await page.getByRole('button', {name: 'Calcular cenário'}).click();
  await expect(page.locator('dl')).toContainText('Informe o denominador do cenário.');
});

test('rejects fractional sales visibly without rendering financial results', async ({page}) => {
  await fillScenario(page);
  await page.getByLabel('Vendas atribuídas no cenário', {exact: true}).fill('2.5');
  await page.getByRole('button', {name: 'Calcular cenário'}).click();
  await expect(page.getByRole('region', {name: 'Quanto essa campanha precisaria entregar?'}).getByRole('alert')).toContainText('quantidade inteira');
  await expect(page.locator('dl')).toHaveCount(0);
});
