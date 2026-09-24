/** Hypothetical costs only. No CRM attribution, CAC, network or LLM dependency. */
export type ScenarioBasis = 'post' | 'campaign';
export type Scenario = {
  cost: number | null;
  views: number | null;
  interactions: number | null;
  sales: number | null;
  costBasis: ScenarioBasis;
  metricsBasis: ScenarioBasis;
  costPeriod: string;
  metricsPeriod: string;
};

export type UnitCost =
  | {status: 'calculated'; value: number; currency: 'BRL'}
  | {status: 'unavailable'; value: null; reason: string};

export type Simulation = {
  hypothetical: true;
  errors: string[];
  costPerThousandViews: UnitCost;
  costPerInteraction: UnitCost;
  costPerSale: UnitCost;
};

function unavailable(reason: string): UnitCost {
  return {status: 'unavailable', value: null, reason};
}

function validate(input: Scenario): string[] {
  const errors: string[] = [];
  const fieldNames = {cost: 'Custo', views: 'Visualizações', interactions: 'Interações', sales: 'Vendas'};
  for (const key of ['cost', 'views', 'interactions', 'sales'] as const) {
    const value = input[key];
    if (value !== null && (!Number.isFinite(value) || value < 0)) {
      errors.push(`${fieldNames[key]}: informe um número finito não negativo.`);
    }
  }
  if (input.sales !== null && !Number.isSafeInteger(input.sales)) {
    errors.push('Vendas: use uma quantidade inteira de vendas dentro do limite numérico.');
  }
  const bases = ['post', 'campaign'];
  if (!bases.includes(input.costBasis) || !bases.includes(input.metricsBasis)
      || input.costBasis !== input.metricsBasis) {
    errors.push('Custo e resultados devem representar o mesmo post ou campanha.');
  }
  if (typeof input.costPeriod !== 'string' || typeof input.metricsPeriod !== 'string'
      || !input.costPeriod.trim() || input.costPeriod.trim() !== input.metricsPeriod.trim()) {
    errors.push('Custo e resultados devem usar o mesmo período informado.');
  }
  return errors;
}

function ratio(cost: number | null, count: number | null, factor: number, empty: string): UnitCost {
  if (cost === null) return unavailable('Informe o custo total do cenário.');
  if (count === null) return unavailable('Informe o denominador do cenário.');
  if (count === 0) return unavailable(empty);
  // Divide before multiplying to avoid unnecessary overflow for large costs.
  const value = (cost / count) * factor;
  if (!Number.isFinite(value)) return unavailable('Resultado excede o limite numérico.');
  return {status: 'calculated', value, currency: 'BRL'};
}

export function simulateCosts(input: Scenario): Simulation {
  const errors = validate(input);
  if (errors.length) {
    const result = unavailable('Corrija as entradas inválidas antes de calcular.');
    return {hypothetical: true, errors, costPerThousandViews: result,
      costPerInteraction: result, costPerSale: result};
  }
  return {
    hypothetical: true,
    errors,
    costPerThousandViews: ratio(input.cost, input.views, 1000, 'Sem views no cenário.'),
    costPerInteraction: ratio(input.cost, input.interactions, 1, 'Sem interações no cenário.'),
    costPerSale: ratio(input.cost, input.sales, 1, 'Sem vendas atribuídas no cenário.'),
  };
}

/** Formatting is separate: calculations retain precision and never turn null into zero. */
export function formatCost(result: UnitCost): string {
  if (result.status === 'unavailable') return result.reason;
  return new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(result.value);
}
