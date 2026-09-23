import {Card} from '@astryxdesign/core/Card';
import {Grid} from '@astryxdesign/core/Grid';
import {Layout} from '@astryxdesign/core/Layout';
import {Skeleton} from '@astryxdesign/core/Skeleton';

export default function Loading() {
  return (
    <Layout
      height="auto"
      contentWidth={1180}
      padding={6}
      content={(
        <div className="loading-state" aria-busy="true" aria-label="Carregando estrutura de decisão">
          <Skeleton height={36} width="68%" radius={2} />
          <Skeleton height={20} width="92%" radius={2} index={1} />
          <Grid columns={{minWidth: 250, max: 2, repeat: 'fit'}} gap={4}>
            {Array.from({length: 4}, (_, index) => (
              <Card key={index} padding={5} minHeight={180}>
                <Skeleton height={20} width="44%" radius={2} index={index + 2} />
                <div className="skeleton-gap" />
                <Skeleton height={28} width="82%" radius={2} index={index + 3} />
              </Card>
            ))}
          </Grid>
        </div>
      )}
    />
  );
}
