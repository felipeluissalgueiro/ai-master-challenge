import {test, expect} from '@playwright/test';
async function openChat(page: import('@playwright/test').Page) {
  await page.goto('/');
  const card = page.locator('#main-content #rec-q1');
  await card.getByText('Conversar sobre esta recomendação').click();
  await card.getByLabel('Sua pergunta').fill('Por que testar antes de investir?');
  return card;
}
test('real route stays closed and the simulator stays usable', async ({page, request}) => {
  const result = await request.post('/api/explain', {data: {question: 'Q'}});
  expect(result.status()).toBe(503);
  const card = await openChat(page);
  await card.getByRole('button', {name: 'Enviar pergunta'}).click();
  await expect(card.getByRole('status')).toContainText('Chat indisponível');
  await page.getByRole('link', {name: 'Simular custos', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Quanto essa campanha precisaria entregar?'})).toBeVisible();
});
test('mocked transport renders plain text and prevents duplicate submission', async ({page}) => {
  let calls = 0;
  await page.route('**/api/explain', async route => {
    calls++; const body = route.request().postDataJSON();
    await new Promise(resolve => setTimeout(resolve, 250));
    await route.fulfill({json: {...body, explanation: '<img src=x onerror=alert(1)> Texto de teste.', evidence_ids: ['ev-performance'], out_of_scope: false}});
  });
  const card = await openChat(page);
  await card.getByRole('button', {name: 'Enviar pergunta'}).click();
  await expect(card.getByRole('button', {name: 'Consultando…'})).toBeDisabled();
  await expect(card).toContainText('<img src=x onerror=alert(1)>');
  await expect(card.locator('img')).toHaveCount(0); expect(calls).toBe(1);
});
test('edited question discards a delayed response without retry', async ({page}) => {
  let calls = 0;
  await page.route('**/api/explain', async route => {
    calls++; const body = route.request().postDataJSON();
    await new Promise(resolve => setTimeout(resolve, 300));
    await route.fulfill({json: {...body, explanation: 'OLD RESPONSE', evidence_ids: ['ev-performance'], out_of_scope: false}});
  });
  const card = await openChat(page);
  await card.getByRole('button', {name: 'Enviar pergunta'}).click();
  await expect(card.getByRole('button', {name: 'Consultando…'})).toBeDisabled();
  await card.getByLabel('Sua pergunta').fill('Pergunta alterada');
  await expect(card.getByRole('button', {name: 'Enviar pergunta'})).toBeEnabled();
  await page.waitForTimeout(400);
  await expect(card).not.toContainText('OLD RESPONSE'); expect(calls).toBe(1);
});
