import type {Metadata} from 'next';
import {ArtifactViewer} from '@/components/artifact-viewer';

export const metadata: Metadata = {title: 'Visualizador Ouro'};

export default function GoldViewerPage() {
  return (
    <ArtifactViewer
      title="Visualizador Ouro"
      description="Rota reservada para o futuro explorador com explicação de SQLite, categorias e gráficos."
    />
  );
}
