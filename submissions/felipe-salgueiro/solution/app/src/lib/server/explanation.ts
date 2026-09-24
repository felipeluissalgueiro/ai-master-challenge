import type {Dashboard} from '../dashboard';

export type Explanation = {explanation: string; evidence_ids: string[]; out_of_scope: boolean};
export type ExplainContext = {snapshot_id: string; recommendation_id: string; recommendation: unknown;
  evidence: {id: string; source_pointer: string; data: unknown}[]};
export type ExplainDependencies = {
  available: boolean;
  authorize: (request: Request) => Promise<boolean>;
  reserveCall: (request: Request) => Promise<boolean>;
  generate: (context: ExplainContext, question: string) => Promise<unknown>;
};
const headers = {'Cache-Control': 'no-store'};
function result(status: number, error: string) { return Response.json({error}, {status, headers}); }
function compact(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(compact);
  if (!value || typeof value !== 'object') return value;
  const row = value as Record<string, unknown>;
  // Keep complete groups, only the metric used in this product; never sample rows.
  const omitted = new Set(['interaction_per_follower_pct', 'total_interactions', 'views', 'all_cells', 'post_hoc_example', 'rank_context', 'contexts']);
  return Object.fromEntries(Object.entries(row).filter(([key]) => !omitted.has(key)).map(([key, item]) => [key, compact(item)]));
}
export function contextFor(data: Dashboard, id: string): ExplainContext | null {
  const recommendation = data.recommendations.find(item => item.id === id);
  if (!recommendation) return null;
  return {snapshot_id: data.snapshot_id, recommendation_id: id, recommendation,
    evidence: data.evidence.filter(item => recommendation.evidence_ids.includes(item.id)).map(item => ({
      id: item.id, source_pointer: item.source_pointer, data: {
        presentation_limit: 'Resumo: não contém todas as células. Não inferir recorte ausente; consulte o dashboard ou a evidência completa.',
        summary: compact(item.data),
      },
    }))};
}
export function validateExplanation(value: unknown, context: ExplainContext): Explanation {
  if (!value || typeof value !== 'object') throw Error('Invalid response');
  const row = value as Record<string, unknown>;
  if (typeof row.explanation !== 'string' || !row.explanation.trim() || row.explanation.length > 5000
      || typeof row.out_of_scope !== 'boolean' || !Array.isArray(row.evidence_ids)
      || row.evidence_ids.length > context.evidence.length
      || (!row.out_of_scope && !row.evidence_ids.length)
      || row.evidence_ids.some(id => typeof id !== 'string' || !context.evidence.some(item => item.id === id))) throw Error('Invalid response');
  return {explanation: row.explanation, out_of_scope: row.out_of_scope, evidence_ids: [...new Set(row.evidence_ids as string[])]};
}
export async function explainRequest(request: Request, data: Dashboard, deps: ExplainDependencies): Promise<Response> {
  if (!deps.available) return result(503, 'Chat indisponível. A análise e o simulador continuam disponíveis.');
  try {
    if (!await deps.authorize(request)) return result(401, 'Acesso não autorizado.');
    if (request.headers.get('origin') !== new URL(request.url).origin) return result(403, 'Origem não permitida.');
    if (!request.headers.get('content-type')?.startsWith('application/json')) return result(415, 'Envie uma pergunta em JSON.');
    const reader = request.body?.getReader();
    if (!reader) return result(400, 'Pergunta ausente.');
    const chunks: Uint8Array[] = []; let bytes = 0;
    while (true) {
      const chunk = await reader.read(); if (chunk.done) break;
      bytes += chunk.value.byteLength;
      if (bytes > 8192) {await reader.cancel(); return result(413, 'Pergunta excede o limite.');}
      chunks.push(chunk.value);
    }
    const merged = new Uint8Array(bytes); let offset = 0;
    for (const chunk of chunks) {merged.set(chunk, offset); offset += chunk.length;}
    let body: Record<string, unknown>;
    try { body = JSON.parse(new TextDecoder().decode(merged)); } catch { return result(400, 'JSON inválido.'); }
    if (!body || typeof body !== 'object' || Array.isArray(body)
        || Object.keys(body).some(key => !['recommendation_id', 'snapshot_id', 'question'].includes(key))
        || typeof body.question !== 'string' || !body.question.trim() || body.question.length > 1500
        || typeof body.recommendation_id !== 'string') return result(400, 'Pergunta ou contexto inválido.');
    if (body.snapshot_id !== data.snapshot_id) return result(409, 'Dados atualizados. Recarregue a página.');
    const context = contextFor(data, body.recommendation_id);
    if (!context) return result(404, 'Recomendação não encontrada.');
    if (JSON.stringify(context).length > 48000) return result(422, 'Contexto excede o limite seguro.');
    // Must be atomic and durable across serverless instances. No in-memory quota.
    if (!await deps.reserveCall(request)) return result(429, 'Limite de consultas atingido.');
    const answer = validateExplanation(await deps.generate(context, body.question.trim()), context);
    return Response.json({...answer, snapshot_id: data.snapshot_id, recommendation_id: body.recommendation_id}, {headers});
  } catch { return result(502, 'Não foi possível obter uma explicação agora. Sem nova tentativa automática.'); }
}
