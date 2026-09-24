import {Button} from '@astryxdesign/core/Button';
import {Heading} from '@astryxdesign/core/Heading';
import {Layout} from '@astryxdesign/core/Layout';

export function ArtifactViewer({title, description, src}: {title: string; description: string; src: string}) {
  return <Layout height="auto" contentWidth={1280} padding={4} content={
    <div className="viewer-page">
      <div className="viewer-heading">
        <div><Heading level={1}>{title}</Heading><p>{description}</p></div>
        <div className="viewer-actions">
          <Button href={src} target="_blank" rel="noopener noreferrer" label="Abrir em tela inteira" variant="primary" />
          <Button href="/relatorios" label="Todos os relatórios" variant="secondary" />
        </div>
      </div>
      <iframe className="artifact-frame" title={title} src={src} sandbox="allow-scripts allow-popups" />
    </div>
  } />;
}
