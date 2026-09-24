import Link from 'next/link';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {Grid} from '@astryxdesign/core/Grid';
import {Heading} from '@astryxdesign/core/Heading';
import {ComparisonFilters} from './comparison-filters';
import {formatNumber as number, label, selectProfiles, type Dashboard} from '../../lib/dashboard';

export function PerformanceDashboard({data, query}: {data: Dashboard; query: Record<string, string | string[] | undefined>}) {
  const selection = selectProfiles(data, query);
  const sponsor = data.sponsorship;
  const rates = data.profiles.platform.map(row => row.interaction_per_view_pct.median);
  // Percentage-point difference × 100 expresses the same rate gap per 10,000 views.
  const platformGap = (Math.max(...rates) - Math.min(...rates)) * 100;
  return <div className="page-stack">
    <section className="hero" aria-labelledby="page-title">
      <Heading id="page-title" level={1} type="display-2">Performance e decisões</Heading>
      <p>O ranking sozinho não justifica trocar de canal. Antes de ampliar patrocínios, defina o objetivo da campanha e como medir seu resultado.</p>
      <p><strong>Dados sintéticos.</strong> {number(data.overall.rows)} posts analisados. A base não representa resultados da semana nem a operação real do G4.</p>
      <div className="hero__actions"><Button href="/relatorios" label="Ver relatórios" variant="primary" /><Button href="/simulador" label="Simular custo por venda" variant="secondary" /></div>
    </section>
    <section className="page-section" aria-labelledby="decisions-title">
      <Heading id="decisions-title" level={2}>O que merece sua atenção</Heading>
      <Grid columns={{minWidth: 280, max: 3, repeat: 'fit'}} gap={4}>
        <Card padding={5}><article className="decision-card" id="conteudo">
          <h3>Conteúdo: o ranking não justifica mudar de canal</h3>
          <p className="metric-value">{number(platformGap, 1)} interação por 10 mil views</p>
          <p>É a diferença entre as taxas medianas da plataforma com maior e menor resultado, expressa a cada 10 mil visualizações.</p>
          <p><strong>Decisão:</strong> não realoque toda a produção por essa diferença. Escolha o canal pela presença do seu público e pelo custo de produzir conteúdo.</p>
          <p><strong>Próximo teste:</strong> mantenha canal, formato e oferta; compare dois ganchos. Defina se quer medir atenção, interesse ou aquisição e colete as métricas correspondentes. É uma proposta para novos dados.</p>
          <Button href="/artifacts/reports/performance-strategy.html#engajamento" label="Ver análise de conteúdo" variant="secondary" />
        </article></Card>
        <Card padding={5}><article className="decision-card" id="patrocinio">
          <h3>Patrocínio: defina o resultado esperado antes de ampliar</h3>
          <p className="metric-value">{sponsor.positive_cells} a {sponsor.negative_cells}</p>
          <p>Em {sponsor.positive_cells} dos {sponsor.cells} grupos comparáveis, patrocinados tiveram mais engajamento; em {sponsor.negative_cells}, menos. Não há vantagem consistente.</p>
          <p><strong>Decisão:</strong> esta base não sustenta recomendar aumento ou corte de verba. Avalie cada parceria conforme o objetivo da campanha e suas métricas de sucesso.</p>
          <p><strong>Como medir:</strong> para aquisição, registre investimento e vendas atribuídas por link ou cupom. Para marca e consideração, defina indicadores próprios; venda imediata não é critério universal.</p>
          <Button href="/artifacts/reports/performance-strategy.html#patrocinio" label="Ver comparação de patrocínio" variant="secondary" />
        </article></Card>
        <Card padding={5}><article className="decision-card" id="retorno">
          <h3>Cortes: ainda não sabemos onde há desperdício</h3>
          <p className="metric-value">Retorno não medido</p>
          <p>Não há investimento, receita ou vendas atribuídas na fonte. Um post com menos interações pode vender mais; esta base não permite conferir isso.</p>
          <p><strong>Decisão:</strong> antes de cortar um canal ou dispensar um creator, confronte o resultado com o objetivo contratado. Os dados disponíveis não comprovam desperdício.</p>
          <p><strong>Próximo passo:</strong> informe custo e vendas esperadas no simulador para avaliar um cenário, sem confundi-lo com resultado realizado.</p>
          <Button href="/simulador" label="Simular custo por venda" variant="secondary" />
          <Link href="/artifacts/reports/performance-strategy.html#estrategia">Conferir estratégia e limites</Link>
        </article></Card>
      </Grid>
    </section>
    <section className="page-section dashboard-notice" aria-labelledby="week-title">
      <Heading id="week-title" level={2}>Seu plano para esta semana</Heading>
      <ol className="weekly-actions">
        <li><strong>Instrumentar as campanhas.</strong> Registrar objetivo e indicadores por parceiro. Para aquisição, incluir investimento, link/cupom e vendas atribuídas.</li>
        <li><strong>Preparar um teste de conteúdo.</strong> Escolher uma oferta e variar apenas o gancho em conteúdos comparáveis. Não há dados de retenção ou texto para escolher o melhor gancho retrospectivamente.</li>
        <li><strong>Definir a regra de investimento.</strong> Estabelecer o resultado esperado conforme o objetivo. Para aquisição, definir o custo por venda aceitável conforme a margem; comparar o teste com essa meta antes de escalar.</li>
      </ol>
      <p>Plano recomendado para execução, não achados de uma semana observada. Frequência ideal, leads, vendas e CAC estão <strong>não mensurados</strong>.</p>
      <Link href="/artifacts/reports/performance-strategy.html#estrategia">Abrir o plano completo e sua justificativa</Link>
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
      <p>Sobre os recortes: Faixas de seguidores são quartis desta base no nível do post, não categorias comerciais de influenciadores.
        Rótulos de audiência indicam predominância, não a proporção de cada público.</p>
    </section>

    <p>As oito perguntas do desafio, metodologia e limitações estão no <Link href="/artifacts/reports/performance-strategy.html#appendix">relatório completo</Link>. <Link href="/artifacts/reports/evidence.json">Baixar evidências em JSON</Link>.</p>
  </div>;
}
