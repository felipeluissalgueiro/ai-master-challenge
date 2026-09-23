import {Banner} from '@astryxdesign/core/Banner';
import {Badge} from '@astryxdesign/core/Badge';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {EmptyState} from '@astryxdesign/core/EmptyState';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {Layout} from '@astryxdesign/core/Layout';
import {Text} from '@astryxdesign/core/Text';

import {HEAD_DECISIONS} from '@/lib/decisions';

export default function HomePage() {
  return (
    <Layout
      height="auto"
      contentWidth={1180}
      padding={6}
      content={(
        <div className="page-stack">
          <section className="hero" aria-labelledby="page-title">
            <Text as="p" type="label">Challenge 004 · social media</Text>
            <Heading id="page-title" level={1} type="display-2" textWrap="balance">
              Decisões de social media, sem atalhos causais.
            </Heading>
            <Text as="p" type="large" color="secondary">
              Um shell executivo para responder às oito perguntas do Head de Social Media.
              Valores e recomendações só aparecem quando houver evidência integrada ao contrato.
            </Text>
            <div className="hero__actions">
              <Button href="/relatorios" label="Ver relatórios" variant="primary" size="lg" />
              <Button href="/explorar" label="Explorar dados" variant="secondary" size="lg" />
            </div>
          </section>

          <Banner
            status="info"
            title="Shell pronto para integração"
            description="A navegação e a hierarquia de decisão estão disponíveis. Dados, números e recomendações continuam indisponíveis nesta Story."
          />

          <section aria-labelledby="decisions-title" className="page-section">
            <div className="section-heading">
              <div>
                <Text as="p" type="label" color="accent">Mapa de decisão</Text>
                <Heading id="decisions-title" level={2}>Oito perguntas para orientar a leitura</Heading>
              </div>
              <Text as="p" type="supporting">Sem números enquanto o contrato não estiver conectado.</Text>
            </div>

            <Grid columns={{minWidth: 250, max: 4, repeat: 'fit'}} gap={4}>
              {HEAD_DECISIONS.map((decision) => (
                <Card key={decision.id} padding={5} minHeight={250}>
                  <article className="decision-card" aria-labelledby={`decision-${decision.id}`}>
                    <div className="decision-card__meta">
                      <span className="decision-card__number" aria-hidden="true">{decision.number}</span>
                      <Badge label="Dados pendentes" variant="neutral" />
                    </div>
                    <Heading id={`decision-${decision.id}`} level={3}>{decision.title}</Heading>
                    <Text as="p" type="supporting">{decision.description}</Text>
                    <Text as="p" type="supporting" color="secondary">
                      Conclusão, evidência, ação e limite serão exibidos após a integração.
                    </Text>
                  </article>
                </Card>
              ))}
            </Grid>
          </section>

          <section aria-labelledby="data-state-title" className="page-section">
            <Card padding={5} variant="muted">
              <EmptyState
                headingLevel={2}
                title="Dados ainda não conectados"
                description="O shell não inventa métricas nem regras econômicas. A integração definitiva do snapshot pertence à etapa de dashboard."
                actions={<Button href="/relatorios" label="Ver estado das rotas" variant="secondary" />}
              />
              <span id="data-state-title" className="sr-only">Estado dos dados</span>
            </Card>
          </section>
        </div>
      )}
    />
  );
}
