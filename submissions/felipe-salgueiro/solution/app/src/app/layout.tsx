import type {Metadata} from 'next';
import type {ReactNode} from 'react';

import './globals.css';
import {Providers} from './providers';
import {SiteShell} from '@/components/site-shell';

export const metadata: Metadata = {
  title: {
    default: 'Challenge 004 Insight Lab',
    template: '%s · Challenge 004 Insight Lab',
  },
  description: 'Shell de decisão para análise de performance e estratégia de social media.',
};

export default function RootLayout({children}: Readonly<{children: ReactNode}>) {
  return (
    <html lang="pt-BR">
      <body>
        <Providers>
          <SiteShell>{children}</SiteShell>
        </Providers>
      </body>
    </html>
  );
}
