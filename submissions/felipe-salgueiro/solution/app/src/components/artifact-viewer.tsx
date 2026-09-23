import {Banner} from '@astryxdesign/core/Banner';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {EmptyState} from '@astryxdesign/core/EmptyState';
import {Heading} from '@astryxdesign/core/Heading';
import {Layout} from '@astryxdesign/core/Layout';
import {Text} from '@astryxdesign/core/Text';

type ArtifactViewerProps = {
  title: string;
  description: string;
};

export function ArtifactViewer({title, description}: ArtifactViewerProps) {
  return (
    <Layout
      height="auto"
      contentWidth={1280}
      padding={4}
      content={(
        <div className="viewer-page">
          <div className="viewer-heading">
            <div>
              <Text as="p" type="label" color="accent">Rota reservada</Text>
              <Heading level={1}>{title}</Heading>
              <Text as="p" type="supporting">{description}</Text>
            </div>
            <Button href="/relatorios" label="Voltar aos relatórios" variant="secondary" />
          </div>

          <Banner
            status="warning"
            title="Publicação congelada"
            description="A arquitetura de informação e a linguagem visual deste artefato estão em revisão. Nenhum HTML ou paleta foi incorporado ao shell."
          />

          <Card padding={6}>
            <EmptyState
              headingLevel={2}
              title="Aguardando handoff aprovado"
              description="Esta rota permanece reservada para validar a navegação. O conteúdo só será conectado após a revisão da Maria e o novo handoff completo com hashes."
              actions={<Button href="/" label="Voltar ao shell" variant="primary" />}
            />
          </Card>
        </div>
      )}
    />
  );
}
