/** Read-only presentation boundary. No statistics are recalculated here. */
export type Summary = {n: number; median: number; p25: number; p75: number};
export type Profile = {label: string; interaction_per_view_pct: Summary};
export type Recommendation = {id: string; question: string; action: string; basis: string;
  limit: string; status_label: string; rule_id: string; evidence_ids: string[]};
export type Evidence = {id: string; source_pointer: string; data: unknown};
export type Dashboard = {snapshot_id: string; recommendations: Recommendation[]; evidence: Evidence[];
  profiles: Record<string, Profile[]>; overall: {rows: number; interaction_per_view_pct: Summary};
  sponsorship: {cells: number; positive_cells: number; negative_cells: number; median_delta_percentage_points: number}};

export const DIMENSIONS: Record<string, string> = {
  platform: 'Plataforma', content_type: 'Formato', content_category: 'Categoria',
  follower_band: 'Faixa de seguidores no post', audience_age_label: 'Idade predominante',
  audience_gender_label: 'Gênero predominante', audience_location_label: 'Localização predominante',
};
export function formatNumber(value: number, digits = 0): string {
  return new Intl.NumberFormat('pt-BR', {maximumFractionDigits: digits, minimumFractionDigits: digits}).format(value);
}
export function label(value: string): string {
  const labels: Record<string, string> = {image: 'Imagem', video: 'Vídeo', text: 'Texto', mixed: 'Misto',
    beauty: 'Beleza', tech: 'Tecnologia', fitness: 'Fitness', female: 'Feminino', male: 'Masculino',
    'non-binary': 'Não binário', post_followers_q1: '1º quartil de seguidores',
    post_followers_q2: '2º quartil de seguidores', post_followers_q3: '3º quartil de seguidores',
    post_followers_q4: '4º quartil de seguidores'};
  return labels[value] ?? value;
}
function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw Error('Objeto de evidência inválido.');
  return value as Record<string, unknown>;
}
function numeric(value: unknown): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw Error('Métrica inválida.');
  return value;
}
function summary(value: unknown): Summary {
  const item = object(value);
  const result = {n: numeric(item.n), median: numeric(item.median), p25: numeric(item.p25), p75: numeric(item.p75)};
  if (!Number.isSafeInteger(result.n) || result.n <= 0 || result.p25 > result.median || result.median > result.p75) throw Error('Resumo inválido.');
  return result;
}
function text(value: unknown): string {
  if (typeof value !== 'string' || !value.trim()) throw Error('Texto de evidência ausente.');
  return value;
}
export function parseDashboard(input: unknown): Dashboard {
  const root = object(input), metric = object(root.metric), commercial = object(root.commercial);
  if (root.schema_version !== 1 || metric.unit !== 'percent' || metric.difference_unit !== 'percentage_points') throw Error('Contrato incompatível.');
  if (commercial.cac !== null || commercial.cost_per_sale !== null || commercial.revenue !== null) throw Error('Contrato comercial inesperado.');
  if (!Array.isArray(root.evidence) || !Array.isArray(root.recommendations)) throw Error('Evidência ausente.');
  const evidence = root.evidence.map(value => {const item = object(value); return {id: text(item.id), source_pointer: text(item.source_pointer), data: item.data};});
  const ids = new Set(evidence.map(item => item.id));
  if (ids.size !== evidence.length) throw Error('Evidência duplicada.');
  const get = (id: string) => object(evidence.find(item => item.id === id)?.data);
  const recommendations = root.recommendations.map(value => {
    const item = object(value);
    if (!Array.isArray(item.evidence_ids) || !item.evidence_ids.length || item.evidence_ids.some(id => !ids.has(String(id)))) throw Error('Recomendação sem evidência.');
    return {id: text(item.id), question: text(item.question), action: text(item.action), basis: text(item.basis),
      limit: text(item.limit), status_label: text(item.status_label), rule_id: text(item.rule_id), evidence_ids: item.evidence_ids.map(text)};
  });
  if (recommendations.length !== 8 || recommendations.some((item, index) => item.id !== `rec-q${index + 1}`)) throw Error('Cobertura incompleta.');
  const rawProfiles = object(get('ev-performance').profiles);
  const profiles: Record<string, Profile[]> = {};
  for (const key of Object.keys(DIMENSIONS)) {
    const rows = rawProfiles[key];
    if (!Array.isArray(rows) || !rows.length) throw Error('Recortes ausentes.');
    profiles[key] = rows.map(value => {const row = object(value); return {label: text(row.label), interaction_per_view_pct: summary(row.interaction_per_view_pct)};});
  }
  const overall = get('ev-overall'), sponsorship = object(get('ev-sponsorship').matched_cell_summary);
  const rows = numeric(overall.rows), totals = summary(overall.interaction_per_view_pct);
  if (rows !== totals.n || Object.values(profiles).some(items => items.reduce((sum, item) => sum + item.interaction_per_view_pct.n, 0) !== rows)) throw Error('Contagem não reconciliada.');
  const cells = numeric(sponsorship.cells), positive = numeric(sponsorship.positive_cells), negative = numeric(sponsorship.negative_cells);
  if (positive + negative !== cells) throw Error('Comparações não reconciliadas.');
  return {snapshot_id: text(root.snapshot_id), recommendations, evidence, profiles,
    overall: {rows, interaction_per_view_pct: totals}, sponsorship: {cells, positive_cells: positive, negative_cells: negative,
      median_delta_percentage_points: numeric(sponsorship.median_delta_percentage_points)}};
}
export function selectProfiles(data: Dashboard, query: Record<string, string | string[] | undefined>) {
  const dimension = query.dimension ?? 'platform', value = query.value ?? '';
  if (typeof dimension !== 'string' || typeof value !== 'string' || !Object.hasOwn(DIMENSIONS, dimension)
      || Object.keys(query).some(key => !['dimension', 'value'].includes(key))) {
    return {status: 'unsupported' as const, dimension: 'platform', value: '', rows: [] as Profile[]};
  }
  const rows = data.profiles[dimension].filter(row => !value || row.label === value);
  return {status: rows.length ? 'ready' as const : 'empty' as const, dimension, value, rows};
}
