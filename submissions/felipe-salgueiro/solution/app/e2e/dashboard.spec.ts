import {test, expect} from '@playwright/test';
test('shows three decisions, weekly plan and working evidence links without chat', async ({page, request}) => {
  await page.goto('/');
  const main = page.locator('#main-content');
  await expect(main).toContainText('52.214');
  await expect(main.locator('.decision-card')).toHaveCount(3);
  await expect(main.locator('#conteudo .metric-value')).toHaveText('1,6 interação por 10 mil views');
  await expect(main.locator('#patrocinio')).toContainText('venda imediata não é critério universal');
  await expect(main.locator('#retorno')).toContainText('objetivo contratado');
  await expect(main.locator('#patrocinio')).toContainText('33 a 27');
  await expect(main.getByRole('heading', {name: 'Seu plano para esta semana'})).toBeVisible();
  await expect(main).not.toContainText('descriptive-q1');
  await expect(main).not.toContainText('Conferir evidência e regra');
  await expect(main).not.toContainText('Conversar sobre');
  const response = await request.post('/api/explain', {data: {question: 'test'}});
  expect(response.status()).toBe(404);
  await main.getByRole('link', {name: 'Ver análise de conteúdo'}).click();
  await expect(page).toHaveURL(/performance-strategy.html#engajamento$/);
  await expect(page.locator('#engajamento')).toBeVisible();
  await page.goto('/');
  await page.locator('#main-content').getByRole('link', {name: 'Ver comparação de patrocínio'}).click();
  await expect(page.locator('#patrocinio')).toBeVisible();
});
test('valid filter preserves exact values, empty filter has a recovery action', async ({page}) => {
  await page.goto('/?dimension=platform&value=Instagram');
  await expect(page.getByRole('article', {name: 'Instagram', exact: true})).toContainText('19,889%');
  await page.goto('/?dimension=platform&value=inexistente');
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

test('mobile has gutters and all menu destinations fit without horizontal scrolling', async ({page}) => {
  await page.setViewportSize({width: 390, height: 844});
  await page.goto('/');
  const geometry = await page.locator('#main-content .page-stack').evaluate(element => {
    const hero = element.querySelector('.hero')!.getBoundingClientRect();
    const nav = document.querySelector('.primary-nav')!;
    return {left: hero.left, right: hero.right, width: window.innerWidth, navOverflow: nav.scrollWidth - nav.clientWidth};
  });
  expect(geometry.left).toBeGreaterThanOrEqual(16);
  expect(geometry.right).toBeLessThanOrEqual(geometry.width - 16);
  expect(geometry.navOverflow).toBeLessThanOrEqual(1);
  const contrastColors = await page.locator('.primary-nav a').last().evaluate(element => {
    const style = getComputedStyle(element);
    return {foreground: style.color, background: style.backgroundColor};
  });
  expect(contrastColors).toEqual({foreground: 'rgb(0, 31, 53)', background: 'rgb(185, 145, 91)'});
  await expect(page.getByRole('link', {name: 'Simular custos', exact: true})).toBeInViewport();
});

test('changing Astryx selectors updates comparison without submitting', async ({page}) => {
  await page.goto('/');
  const main = page.locator('#main-content');
  await main.getByRole('combobox', {name: 'Comparar por', exact: true}).click();
  await page.getByRole('option', {name: 'Formato', exact: true}).click();
  await expect(page).toHaveURL(/dimension=content_type/);
  await expect(main.getByRole('article', {name: 'Instagram', exact: true})).toHaveCount(0);
  const group = main.getByRole('combobox', {name: 'Grupo', exact: true});
  await group.click();
  const option = page.getByRole('option').filter({hasNotText: 'Todos os grupos'}).first();
  const title = await option.innerText();
  await option.click();
  await expect(page).toHaveURL(/value=/);
  await expect(main.locator('[aria-labelledby="comparison-title"] article')).toHaveCount(1);
  await expect(main.locator('[aria-labelledby="comparison-title"] article')).toContainText(title.trim());
  await main.getByRole('combobox', {name: 'Comparar por', exact: true}).click();
  await page.getByRole('option', {name: 'Plataforma', exact: true}).click();
  await expect(page).toHaveURL(/dimension=platform$/);
  await expect(main.getByRole('article', {name: 'Instagram', exact: true})).toBeVisible();
});
