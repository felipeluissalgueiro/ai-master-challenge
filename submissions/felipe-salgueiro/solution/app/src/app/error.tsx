'use client';

import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {EmptyState} from '@astryxdesign/core/EmptyState';

export default function ErrorPage({reset}: {error: Error & {digest?: string}; reset: () => void}) {
  return (
    <div className="bounded-state">
      <Card padding={6}>
        <EmptyState
          headingLevel={1}
          title="Não foi possível abrir esta área"
          description="A navegação continua disponível. Tente carregar a página novamente ou consulte o estado das rotas de relatório."
          actions={(
            <div className="empty-actions">
              <Button label="Tentar novamente" variant="primary" onClick={reset} />
              <Button href="/relatorios" label="Ver relatórios" variant="secondary" />
            </div>
          )}
        />
      </Card>
    </div>
  );
}
