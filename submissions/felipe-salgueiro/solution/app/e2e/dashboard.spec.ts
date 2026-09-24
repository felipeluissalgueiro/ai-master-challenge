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
