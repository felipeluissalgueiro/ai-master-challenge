'use client';
import {useEffect, useRef, useState, type FormEvent} from 'react';

type Answer = {explanation: string; evidence_ids: string[]; out_of_scope: boolean};
export function RecommendationChat({recommendationId, snapshotId}: {recommendationId: string; snapshotId: string}) {
  const [question, setQuestion] = useState(''), [answer, setAnswer] = useState<Answer | null>(null);
  const [error, setError] = useState(''), [busy, setBusy] = useState(false);
  const active = useRef<AbortController | null>(null);
  useEffect(() => () => active.current?.abort(), [recommendationId, snapshotId]);
  function invalidate() { active.current?.abort(); active.current = null; setBusy(false); setAnswer(null); setError(''); }
  async function submit(event: FormEvent) {
    event.preventDefault();
    if (active.current || !question.trim()) return;
    const controller = new AbortController(); active.current = controller;
    setBusy(true); setAnswer(null); setError('');
    const timer = setTimeout(() => controller.abort(), 35000);
    try {
      const response = await fetch('/api/explain', {method: 'POST', headers: {'Content-Type': 'application/json'},
        signal: controller.signal, body: JSON.stringify({recommendation_id: recommendationId, snapshot_id: snapshotId, question})});
      const body = await response.json();
      if (active.current !== controller) return;
      if (!response.ok) {setError(typeof body.error === 'string' ? body.error : 'Chat indisponível.'); return;}
      if (body.snapshot_id !== snapshotId || body.recommendation_id !== recommendationId
          || typeof body.explanation !== 'string' || !Array.isArray(body.evidence_ids)
          || !body.evidence_ids.every((id: unknown) => typeof id === 'string')
          || typeof body.out_of_scope !== 'boolean') {setError('Resposta incompatível. Recarregue a página.'); return;}
      setAnswer(body);
    } catch {
      if (active.current === controller) setError('Consulta interrompida ou indisponível. Nenhuma tentativa automática foi enviada.');
    } finally {
      clearTimeout(timer);
      if (active.current === controller) {active.current = null; setBusy(false);}
    }
  }
  return <details className="recommendation-chat">
    <summary>Conversar sobre esta recomendação</summary>
    <p>Explicação por IA, limitada à evidência desta recomendação. Não substitui a análise.
      A consulta pode estar indisponível; os dados e o simulador não dependem dela.</p>
    <form onSubmit={submit}>
      <label htmlFor={'question-' + recommendationId}>Sua pergunta</label>
      <textarea id={'question-' + recommendationId} value={question} maxLength={1500} required rows={3}
        onChange={event => {invalidate(); setQuestion(event.target.value);}} />
      <button type="submit" disabled={busy || !question.trim()}>{busy ? 'Consultando…' : 'Enviar pergunta'}</button>
    </form>
    <div aria-live="polite" aria-atomic="true">
      {error && <p role="status">{error}</p>}
      {answer && <div><p><strong>{answer.out_of_scope ? 'Fora do escopo' : 'Explicação gerada por IA'}</strong></p>
        <p style={{whiteSpace: 'pre-wrap'}}>{answer.explanation}</p>
        <p>Evidências: {answer.evidence_ids.join(', ') || 'Não aplicável à pergunta.'}</p></div>}
    </div>
  </details>;
}
