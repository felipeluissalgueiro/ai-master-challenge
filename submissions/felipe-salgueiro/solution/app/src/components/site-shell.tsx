import {Suspense, type ReactNode} from 'react';
import Link from 'next/link';
import {AppShell} from '@astryxdesign/core/AppShell';
import {Button} from '@astryxdesign/core/Button';

import {QueryPreservingButton} from '@/components/query-preserving-button';

export function SiteShell({children}: {children: ReactNode}) {
  const topNav = (
    <header className="site-header">
      <div className="site-header__inner">
        <Link className="brand" href="/" aria-label="Challenge 004 Insight Lab — início">
          <span className="brand__mark" aria-hidden="true">C004</span>
          <span className="brand__copy">
            <strong>Insight Lab</strong>
            <small>Solução independente</small>
          </span>
        </Link>

        <nav className="primary-nav" aria-label="Navegação principal">
          <Link href="/">Performance e estratégia</Link>
          <Link href="/explorar">Explorar dados</Link>
          <Link href="/simulador">Simular custos</Link>
          <Suspense fallback={<Button href="/relatorios" label="Ver relatórios" variant="primary" size="sm" />}>
            <QueryPreservingButton href="/relatorios" label="Ver relatórios" variant="primary" size="sm" />
          </Suspense>
        </nav>
      </div>
    </header>
  );

  return (
    <div className="brand-shell">
      <a className="skip-link" href="#main-content">Ir para o conteúdo</a>
      <AppShell topNav={topNav} height="auto" variant="surface" contentPadding={0}>
        <div id="main-content" tabIndex={-1}>{children}</div>
      </AppShell>
    </div>
  );
}
