import Link from 'next/link';
import {Button} from '@astryxdesign/core/Button';
import {ComparisonFilters} from './comparison-filters';
import {Card} from '@astryxdesign/core/Card';
import {Badge} from '@astryxdesign/core/Badge';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {RecommendationChat} from '../chat/recommendation-chat';
import {DIMENSIONS, formatNumber as number, label, selectProfiles, type Dashboard} from '../../lib/dashboard';

const DECISION_TITLES: Record<string, string> = {
  'rec-q1': 'Teste conteúdo antes de concentrar em um canal',
  'rec-q2': 'Patrocínio não tem vantagem consistente',
  'rec-q3': 'Audiência: valide aderência à oferta',
  'rec-q4': 'Não confunda engajamento menor com desperdício',
  'rec-q5': 'Concentre esforço em experimentos comparáveis',
  'rec-q6': 'Condicione patrocínio ao custo por venda',
  'rec-q7': 'Pare de escalar sem medir resultado comercial',
  'rec-q8': 'Nesta semana: instrumente, teste e compare',
};

const DECISION_GROUPS = [
  {id: 'conteudo', title: 'Conteúdo e audiência', items: ['rec-q1', 'rec-q3', 'rec-q4']},
  {id: 'patrocinio', title: 'Investimento em patrocínio', items: ['rec-q2', 'rec-q6']},
  {id: 'proximos-passos', title: 'Prioridades do próximo ciclo', items: ['rec-q5', 'rec-q7', 'rec-q8']},
];

function MetricRange({data, dimension}: {data: Dashboard; dimension: string}) {
  const medians = data.profiles[dimension].map(row => row.interaction_per_view_pct.median);
  return <p>{DIMENSIONS[dimension]}: medianas de {number(Math.min(...medians), 3)}% a {number(Math.max(...medians), 3)}%.
    Essa faixa entre grupos não demonstra efeito causal.</p>;
}

export function PerformanceDashboard({data, query}: {data: Dashboard; query: Record<string, string | string[] | undefined>}) {
  const selection = selectProfiles(data, query);
  const sponsor = data.sponsorship;
  return <div className="page-stack">
    <section className="hero" aria-labelledby="page-title">
      <Heading id="page-title" level={1} type="display-2">Performance e decisões</Heading>
      <p>Não há um canal ou perfil de creator que justifique concentrar todo o investimento nesta base. Priorize testes de conteúdo e acompanhe vendas antes de escalar.</p>
      <p><strong>Dados sintéticos.</strong> Este exercício não mede a operação real do G4 nem é benchmark de mercado.</p>
      <div className="hero__actions"><Button href="/relatorios" label="Ver relatórios" variant="primary" /><Button href="/simulador" label="Simular custo por venda" variant="secondary" /></div>
    </section>
    <section aria-label="Panorama geral da base">
      <Grid columns={{minWidth: 220, max: 3, repeat: 'fit'}} gap={4}>
        <Card padding={5}><p>Posts analisados</p><strong className="metric-value">{number(data.overall.rows)}</strong><p>Base completa, não afetada pelos filtros abaixo.</p></Card>
        <Card padding={5}><p>Interações por visualizações</p><strong className="metric-value">{number(data.overall.interaction_per_view_pct.median, 3)}%</strong><p>Mediana das taxas dos posts; não é taxa agregada nem pessoas únicas.</p></Card>
        <Card padding={5}><p>Patrocínio: resultado misto</p><strong className="metric-value">{sponsor.positive_cells} de {sponsor.cells}</strong><p>Comparações com taxa maior nos patrocinados; {sponsor.negative_cells} no sentido contrário. Não prova efeito causal.</p></Card>
      </Grid>
    </section>
    <section className="page-section" aria-labelledby="comparison-title">
      <Heading id="comparison-title" level={2}>Compare antes de escolher</Heading>
      <p>Uma dimensão por vez. Os filtros afetam somente este painel; não combinamos medianas de grupos.</p>
      <ComparisonFilters dimension={selection.dimension} value={selection.value} profiles={data.profiles} />
      {selection.status !== 'ready' ? <div role="status" className="dashboard-notice">
        <h3>{selection.status === 'empty' ? 'Recorte sem registros' : 'Combinação de filtros não disponível'}</h3>
        <p>{selection.status === 'empty' ? 'Nenhuma categoria corresponde ao valor informado. Isso não é desempenho zero.' : 'Use apenas uma dimensão e seu valor. Cruzamentos não exportados não são estimados.'}</p>
        <Link href="/">Limpar filtros e ver a base</Link>
      </div> : <Grid columns={{minWidth: 240, max: 3, repeat: 'fit'}} gap={4}>
        {selection.rows.map(row => <Card key={row.label} padding={5}><article aria-label={label(row.label)}>
          <h3>{label(row.label)}</h3><p><strong>{number(row.interaction_per_view_pct.median, 3)}%</strong> de interações por views</p>
          <p>{number(row.interaction_per_view_pct.n)} posts · mediana do grupo</p>
          <p>Metade central dos posts: {number(row.interaction_per_view_pct.p25, 3)}% a {number(row.interaction_per_view_pct.p75, 3)}%.</p>
          <Link href={'/?dimension=' + encodeURIComponent(selection.dimension) + '&value=' + encodeURIComponent(row.label)}>Isolar este grupo</Link>
        </article></Card>)}
      </Grid>}
      <p>Fonte: ev-performance. Faixas de seguidores são quartis desta base no nível do post, não categorias comerciais de influenciadores.
        Rótulos de audiência indicam predominância, não a proporção de cada público.</p>
    </section>
    <section className="page-section" aria-labelledby="decisions-title">
      <Heading id="decisions-title" level={2}>O que fazer com esses dados</Heading>
      <p>Prioridades para conteúdo, patrocínio e medição. Cada ação mantém sua evidência e seus limites.</p>
      <nav className="decision-navigation" aria-label="Decisões por tema">
        {DECISION_GROUPS.map(group => <Button key={group.id} href={'#' + group.id} label={group.title} variant="secondary" />)}
      </nav>
      {DECISION_GROUPS.map(group => <section className="decision-group" id={group.id} key={group.id} aria-labelledby={group.id + '-heading'}>
      <h3 id={group.id + '-heading'}>{group.title}</h3>
      <Grid columns={{minWidth: 300, max: 2, repeat: 'fit'}} gap={4}>
        {data.recommendations.filter(item => group.items.includes(item.id)).map(item => <Card key={item.id} padding={5}>
          <article className="decision-card" id={item.id} aria-labelledby={item.id + '-title'}>
            <div><Badge label={['rec-q5', 'rec-q6', 'rec-q7', 'rec-q8'].includes(item.id) ? 'Ação proposta' : 'Leitura dos dados'} variant="neutral" /></div>
            <h4 id={item.id + '-title'}>{DECISION_TITLES[item.id]}</h4>
            {item.evidence_ids.includes('ev-performance') && !item.evidence_ids.includes('ev-sponsorship')
              && <MetricRange data={data} dimension="platform" />}
            {item.id === 'rec-q1' && <MetricRange data={data} dimension="content_type" />}
            {item.evidence_ids.includes('ev-audience') && <MetricRange data={data} dimension="audience_age_label" />}
            {item.evidence_ids.includes('ev-sponsorship') && <p>{sponsor.positive_cells} comparações a favor dos patrocinados e {sponsor.negative_cells} contra, entre {sponsor.cells} recortes comparáveis.
              Diferença mediana: {number(sponsor.median_delta_percentage_points, 4)} ponto percentual.</p>}
            {item.evidence_ids.includes('ev-overall') && <p>Base de {number(data.overall.rows)} posts; taxa mediana de {number(data.overall.interaction_per_view_pct.median, 3)}%.</p>}
            <p><strong>Ação proposta:</strong> {item.action}</p><p><strong>Limite:</strong> {item.limit}.</p>
            <details><summary>Conferir evidência e regra</summary>
              <p>{item.basis}.</p><p>Regra: <code>{item.rule_id}</code> · snapshot: <code>{data.snapshot_id}</code></p>
              <ul>{item.evidence_ids.map(id => {
                const evidence = data.evidence.find(entry => entry.id === id)!;
                return <li key={id}><code>{id}</code> — evidence.json <code>{evidence.source_pointer}</code></li>;
              })}</ul>
              <p>Arquivos canônicos no fork: solution/data/app/dashboard.json e solution/reports/evidence.json.</p>
            </details>
            <RecommendationChat key={data.snapshot_id + item.id} recommendationId={item.id} snapshotId={data.snapshot_id} />
          </article>
        </Card>)}
      </Grid>
      </section>)}
    </section>
    <section aria-labelledby="commercial-title" className="dashboard-notice">
      <Heading id="commercial-title" level={2}>Engajamento não fecha a conta sozinho</Heading>
      <p>Receita, custo por venda, CAC e benchmark externo: <strong>não mensurados</strong>.
        A fonte não contém custos, vendas atribuídas ou novos clientes.</p>
      <p>Para decidir investimento, registre custo e atribuição por campanha. Integração ao CRM é capacidade futura.</p>
      <Link href="/simulador">Testar suas hipóteses no simulador</Link>
    </section>
  </div>;
}
