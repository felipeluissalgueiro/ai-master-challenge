import {expect, test} from '@playwright/test';

test.beforeEach(async ({page}) => {
  const runtimeErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') runtimeErrors.push(message.text());
  });
  page.on('pageerror', (error) => runtimeErrors.push(error.message));
  (page as typeof page & {runtimeErrors?: string[]}).runtimeErrors = runtimeErrors;
});

test.afterEach(async ({page}) => {
  const runtimeErrors = (page as typeof page & {runtimeErrors?: string[]}).runtimeErrors ?? [];
  const unexpectedErrors = runtimeErrors.filter((message) => !(
    page.url().endsWith('/rota-inexistente')
    && message === 'Failed to load resource: the server responded with a status of 404 (Not Found)'
  ));
  expect(unexpectedErrors, 'browser console and page errors').toEqual([]);
});

test('navigates by keyboard and preserves the current query', async ({page}) => {
  await page.goto('/?platform=instagram&format=video');
  await expect(page.getByRole('heading', {level: 1})).toContainText('Performance e decisões');
  await expect(page.locator('.decision-card')).toHaveCount(3);
  await expect(page.locator('#main-content').getByText('Dados sintéticos.', {exact: true})).toBeVisible();

  const reportsLink = page.getByRole('link', {name: 'Ver relatórios'}).first();
  await reportsLink.focus();
  await expect(reportsLink).toBeFocused();
  const focusOutline = await reportsLink.evaluate((element) => getComputedStyle(element).outlineStyle);
  expect(focusOutline).not.toBe('none');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/relatorios\?platform=instagram&format=video$/);
  await expect(page.getByRole('heading', {level: 1, name: 'Ver relatórios'})).toBeVisible();
  await expect(
    page.getByRole('link', {name: 'Abrir Análise de performance e estratégia'}),
  ).toHaveAttribute('href', '/relatorios/executivo?platform=instagram&format=video');
});

test('opens both final report artifacts', async ({page}) => {
  const artifacts = [
    {
      route: '/relatorios/executivo',
      heading: 'Análise de performance e estratégia',
    },
    {
      route: '/relatorios/visualizador',
      heading: 'Visualizador Ouro',
    },
  ];

  for (const artifact of artifacts) {
    await page.goto(artifact.route);
    await expect(page.getByRole('heading', {level: 1, name: artifact.heading})).toBeVisible();
    await expect(page.locator('iframe')).toHaveCount(1);
    await expect(page.frameLocator('iframe').locator('h1')).toBeVisible();
    await expect(page.getByText('Publicação congelada')).toHaveCount(0);
  }
});

test('shows the actual explorer with keyboard access', async ({page}) => {
  await page.goto('/explorar');
  await expect(page.getByRole('heading', {level: 1, name: 'Explorar dados'})).toBeVisible();
  await expect(page.frameLocator('iframe').locator('h1')).toBeVisible();

  const fitsViewport = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
  expect(fitsViewport).toBeTruthy();

  const viewerLink = page.getByRole('link', {name: 'Abrir em tela inteira'});
  await viewerLink.focus();
  await expect(viewerLink).toBeFocused();
  const focusOutline = await viewerLink.evaluate((element) => getComputedStyle(element).outlineStyle);
  expect(focusOutline).not.toBe('none');
});

test('provides a keyboard skip link before the primary navigation', async ({page}) => {
  await page.goto('/');
  await page.keyboard.press('Tab');

  const skipLink = page.getByRole('link', {name: 'Ir para o conteúdo'});
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main-content')).toBeFocused();
});

test('keeps decision hierarchy and supporting text readable', async ({page}) => {
  await page.goto('/');

  const hierarchy = await page.evaluate(() => {
    const numericSize = (selector: string) => {
      const element = document.querySelector(selector);
      return element ? Number.parseFloat(getComputedStyle(element).fontSize) : 0;
    };
    const supportSizes = [...document.querySelectorAll('.decision-card p')]
      .map((element) => Number.parseFloat(getComputedStyle(element).fontSize));

    return {
      h1: numericSize('h1'),
      h2: numericSize('h2'),
      h3: numericSize('h3'),
      smallestSupportingText: Math.min(...supportSizes),
    };
  });

  expect(hierarchy.h1).toBeGreaterThan(hierarchy.h2);
  expect(hierarchy.h2).toBeGreaterThan(hierarchy.h3);
  expect(hierarchy.h3).toBeGreaterThanOrEqual(18);
  expect(hierarchy.smallestSupportingText).toBeGreaterThanOrEqual(14);
});

test('renders every public route without horizontal document overflow', async ({page}) => {
  const routes = [
    '/',
    '/explorar',
    '/relatorios',
    '/relatorios/executivo',
    '/relatorios/visualizador',
    '/simulador',
    '/rota-inexistente',
  ];

  for (const route of routes) {
    const response = await page.goto(route);
    if (route === '/rota-inexistente') expect(response?.status()).toBe(404);
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow, `horizontal overflow at ${route}`).toBeLessThanOrEqual(1);
  }

  await expect(page.getByRole('heading', {level: 1, name: 'Página não encontrada'})).toBeVisible();
});
