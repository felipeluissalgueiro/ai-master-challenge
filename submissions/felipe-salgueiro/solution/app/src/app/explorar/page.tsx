import type {Metadata} from 'next';
import {Banner} from '@astryxdesign/core/Banner';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {EmptyState} from '@astryxdesign/core/EmptyState';
import {Heading} from '@astryxdesign/core/Heading';
import {Layout} from '@astryxdesign/core/Layout';
import {Text} from '@astryxdesign/core/Text';

export const metadata: Metadata = {title: 'Explorar dados'};

export default function ExplorePage() {
  return (
    <Layout
      height="auto"
      contentWidth={960}
      padding={6}
      content={(
        <div className="page-stack">
          <section className="compact-hero">
            <Text as="p" type="label">Leitura técnica</Text>
            <Heading level={1}>Explorar dados</Heading>
            <Text as="p" type="large" color="secondary">
              A rota está pronta para explicar origem, categorias e gráficos sem expor o banco no navegador.
            </Text>
          </section>

          <Banner
            status="warning"
            title="Conteúdo analítico aguardando handoff"
            description="O explorador publicado anteriormente permanece fora do bundle enquanto sua arquitetura de informação é revisada."
          />

          <Card padding={6}>
            <EmptyState
              headingLevel={2}
              title="Visualização ainda não conectada"
              description="A integração futura deve explicar como ler as categorias e os gráficos a partir dos dados preparados, sem incluir SQLite no bundle."
              actions={(
                <div className="empty-actions">
                  <Button
                    href="/relatorios/visualizador"
                    label="Ver estado do visualizador"
                    variant="primary"
                  />
                  <Button href="/" label="Voltar às decisões" variant="secondary" />
                </div>
              )}
            />
          </Card>
        </div>
      )}
    />
  );
}
