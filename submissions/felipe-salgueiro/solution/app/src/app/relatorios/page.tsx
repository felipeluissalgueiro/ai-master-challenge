import type {Metadata} from 'next';
import {Suspense} from 'react';
import {Badge} from '@astryxdesign/core/Badge';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {Layout} from '@astryxdesign/core/Layout';
import {Text} from '@astryxdesign/core/Text';

import {QueryPreservingButton} from '@/components/query-preserving-button';

export const metadata: Metadata = {title: 'Relatórios'};

const reports = [
  {
    title: 'Análise de performance e estratégia',
    description: 'Rota preservada; conteúdo e linguagem de gestor aguardam a revisão aprovada.',
    href: '/relatorios/executivo',
    status: 'Em revisão',
  },
  {
    title: 'Explorar dados',
    description: 'Rota preservada; explicação de SQLite, categorias e gráficos ainda está bloqueada.',
    href: '/relatorios/visualizador',
    status: 'Em revisão',
  },
] as const;

export default function ReportsPage() {
  return (
    <Layout
      height="auto"
      contentWidth={1080}
      padding={6}
      content={(
        <div className="page-stack">
          <section className="compact-hero">
            <Text as="p" type="label">Rotas reservadas</Text>
            <Heading level={1}>Ver relatórios</Heading>
            <Text as="p" type="large" color="secondary">
              A navegação permanece testável, mas nenhum artefato reprovado é copiado ou exibido pelo shell.
            </Text>
          </section>

          <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
            {reports.map((report) => (
              <Card key={report.href} padding={6} minHeight={280}>
                <div className="report-card">
                  <Badge label={report.status} variant="warning" />
                  <Heading level={2}>{report.title}</Heading>
                  <Text as="p" type="supporting">{report.description}</Text>
                  <div className="report-card__action">
                    <Suspense
                      fallback={(
                        <Button
                          href={report.href}
                          label={`Abrir ${report.title}`}
                          variant="primary"
                          target="_blank"
                          rel="noopener noreferrer"
                        />
                      )}
                    >
                      <QueryPreservingButton
                        href={report.href}
                        label={`Abrir ${report.title}`}
                        variant="primary"
                        target="_blank"
                        rel="noopener noreferrer"
                      />
                    </Suspense>
                  </div>
                </div>
              </Card>
            ))}
          </Grid>

          <Text as="p" type="supporting">
            A publicação está congelada até a revisão da Maria e um novo handoff completo com hashes.
          </Text>
        </div>
      )}
    />
  );
}
