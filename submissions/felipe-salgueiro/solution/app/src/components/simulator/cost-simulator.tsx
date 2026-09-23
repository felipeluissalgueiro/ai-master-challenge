'use client';

import {useState, type CSSProperties, type FormEvent} from 'react';
import {simulateCosts, formatCost, type ScenarioBasis, type Simulation} from '../../lib/simulator';

const grid: CSSProperties = {display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 230px), 1fr))', gap: '1rem'};
const field: CSSProperties = {display: 'grid', gap: '.4rem'};
const control: CSSProperties = {padding: '.75rem', font: 'inherit', border: '1px solid #64748b', borderRadius: '.4rem', width: '100%', boxSizing: 'border-box'};
const numericFields = [
  {key: 'cost', label: 'Custo total (R$)', step: '0.01'},
  {key: 'views', label: 'Visualizações estimadas', step: 'any'},
  {key: 'interactions', label: 'Interações estimadas', step: 'any'},
  {key: 'sales', label: 'Vendas atribuídas no cenário', step: '1'},
] as const;

function numberOrMissing(value: string): number | null {
  return value.trim() === '' ? null : Number(value);
}

export function CostSimulator() {
  const [values, setValues] = useState({cost: '', views: '', interactions: '', sales: ''});
  const [basis, setBasis] = useState<ScenarioBasis>('campaign');
  const [period, setPeriod] = useState('');
  const [result, setResult] = useState<Simulation | null>(null);

  function calculate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setResult(simulateCosts({
      cost: numberOrMissing(values.cost), views: numberOrMissing(values.views),
      interactions: numberOrMissing(values.interactions), sales: numberOrMissing(values.sales),
      costBasis: basis, metricsBasis: basis, costPeriod: period, metricsPeriod: period,
    }));
  }

  return (
    <section aria-labelledby="simulator-title" style={{maxWidth: 960, margin: 'auto', padding: '1.5rem'}}>
      <h1 id="simulator-title">Quanto essa campanha precisaria entregar?</h1>
      <p>Simule o custo por visualização, interação e venda antes de decidir investir.</p>
      <p id="scenario-warning"><strong>Cenário hipotético.</strong> A base não contém custos ou vendas reais.
        Nenhum valor é preenchido como resultado observado. Custo por venda não é CAC nem prova retorno.</p>
      <form onSubmit={calculate} aria-describedby="scenario-warning" noValidate>
        <fieldset style={{border: 0, padding: 0, margin: '1.5rem 0'}}>
          <legend style={{fontWeight: 700, marginBottom: '1rem'}}>Use o mesmo escopo e período para todas as entradas</legend>
          <div style={grid}>
            <label style={field}>Escopo
              <select value={basis} style={control} onChange={event => {setBasis(event.target.value as ScenarioBasis); setResult(null);}}>
                <option value="campaign">Campanha completa</option><option value="post">Um único post</option>
              </select>
            </label>
            <label style={field}>Período do cenário
              <input value={period} style={control} placeholder="Ex.: 1 a 7 de outubro" maxLength={100}
                onChange={event => {setPeriod(event.target.value); setResult(null);}} />
            </label>
            {numericFields.map(({key, label, step}) => (
              <label key={key} style={field}>{label}
                <input type="number" inputMode={key === 'sales' ? 'numeric' : 'decimal'} min="0" step={step}
                  value={values[key]} style={control} aria-describedby="scenario-input-help"
                  onChange={event => {setValues({...values, [key]: event.target.value}); setResult(null);}} />
              </label>
            ))}
          </div>
        </fieldset>
        <p id="scenario-input-help">Deixe em branco o que você ainda não sabe. Inclua no custo os valores que deseja comparar
          (creator, produção e distribuição). Não misture custo da campanha com métricas médias de um post.</p>
        <button type="submit" style={{...control, width: 'auto', background: '#17243b', color: '#fff', cursor: 'pointer'}}>Calcular cenário</button>
      </form>
      <div aria-live="polite" aria-atomic="true" style={{marginTop: '1.5rem'}}>
        {!result && <p>Preencha suas hipóteses e calcule. Alterar uma entrada invalida o resultado anterior.</p>}
        {result && result.errors.length > 0 && <div role="alert"><h2>Revise as entradas</h2><ul>{result.errors.map(error => <li key={error}>{error}</li>)}</ul></div>}
        {result && result.errors.length === 0 && <>
          <h2>Custos estimados — não resultados da base</h2>
          <dl style={grid}>
            {[
              ['Por mil visualizações', result.costPerThousandViews],
              ['Por interação', result.costPerInteraction],
              ['Por venda atribuída no cenário', result.costPerSale],
            ].map(([label, item]) => (
              <div key={String(label)} style={{padding: '1rem', border: '1px solid #94a3b8', borderRadius: '.5rem'}}>
                <dt>{String(label)}</dt><dd style={{margin: '.5rem 0', fontSize: '1.3rem', fontWeight: 700}}>{formatCost(item as Simulation['costPerSale'])}</dd>
              </div>
            ))}
          </dl>
          <p>Fórmulas: custo ÷ views × 1.000; custo ÷ interações; custo ÷ vendas.
            Views não são alcance ou impressões. Esses custos, sozinhos, não dizem se há lucro.</p>
          <p><strong>Próxima decisão:</strong> compare o custo por venda com a margem do negócio e valide a atribuição no CRM.
            Essa conexão é uma capacidade futura, não está implementada.</p>
        </>}
      </div>
    </section>
  );
}
