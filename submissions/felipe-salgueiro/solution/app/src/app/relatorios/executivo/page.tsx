import type {Metadata} from 'next';
import {ArtifactViewer} from '@/components/artifact-viewer';

export const metadata: Metadata = {title: 'Análise de performance e estratégia'};

export default function ExecutiveReportPage() {
  return (
    <ArtifactViewer
      title="Análise de performance e estratégia"
      description="Rota reservada para a futura versão em linguagem de gestor."
    />
  );
}
