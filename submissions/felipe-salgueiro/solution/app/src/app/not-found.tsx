import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {EmptyState} from '@astryxdesign/core/EmptyState';

export default function NotFound() {
  return (
    <div className="bounded-state">
      <Card padding={6}>
        <EmptyState
          headingLevel={1}
          title="Página não encontrada"
          description="Confira a navegação principal ou volte para o mapa das oito decisões."
          actions={<Button href="/" label="Voltar ao início" variant="primary" />}
        />
      </Card>
    </div>
  );
}
