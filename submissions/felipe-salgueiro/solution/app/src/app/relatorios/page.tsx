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
    description: 'Conclusões sobre conteúdo e patrocínio, prioridades de investimento e plano de ação.',
    href: '/relatorios/executivo',
    status: 'Disponível',
  },
  {
    title: 'Explorar dados',
    description: 'Leitura visual dos dados derivados do SQLite, com filtros, categorias e explicação dos gráficos.',
    href: '/relatorios/visualizador',
    status: 'Disponível',
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
            <Text as="p" type="label">Biblioteca de análises</Text>
            <Heading level={1}>Ver relatórios</Heading>
            <Text as="p" type="large" color="secondary">
              Consulte a análise executiva ou investigue os números que sustentam cada recomendação.
            </Text>
          </section>

          <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
            {reports.map((report) => (
              <Card key={report.href} padding={6} minHeight={280}>
                <div className="report-card">
                  <Badge label={report.status} variant="neutral" />
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
            Base sintética. Estes relatórios descrevem o dataset do desafio, não a operação real do G4.
          </Text>
        </div>
      )}
    />
  );
}
