import type {Metadata} from 'next';
import {ArtifactViewer} from '@/components/artifact-viewer';
export const metadata: Metadata = {title: 'Explorar dados'};
export default function ExplorePage() {
  return <ArtifactViewer title="Explorar dados" description="Consulte categorias, amostras e comparações derivadas do SQLite. O banco não é carregado no navegador." src="/artifacts/prototype/index.html" />;
}
