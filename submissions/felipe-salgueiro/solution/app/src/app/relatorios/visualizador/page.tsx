import type {Metadata} from 'next';
import {ArtifactViewer} from '@/components/artifact-viewer';
export const metadata: Metadata = {title: 'Visualizador Ouro'};
export default function GoldViewerPage() {
  return <ArtifactViewer title="Visualizador Ouro" description="Explore a camada de dados usada na análise, suas categorias e os limites das comparações." src="/artifacts/prototype/index.html" />;
}
