'use client';

import {useTransition} from 'react';
import {useRouter} from 'next/navigation';
import {Selector} from '@astryxdesign/core/Selector';
import {Button} from '@astryxdesign/core/Button';
import {DIMENSIONS, label, type Profile} from '../../lib/dashboard';

export function ComparisonFilters({dimension, value, profiles}: {
  dimension: string; value: string; profiles: Record<string, Profile[]>;
}) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  function select(nextDimension: string, nextValue = '') {
    const params = new URLSearchParams({dimension: nextDimension});
    if (nextValue) params.set('value', nextValue);
    startTransition(() => router.replace('/?' + params.toString(), {scroll: false}));
  }
  return <div className="dashboard-filters" aria-busy={pending}>
    <Selector label="Comparar por" value={dimension} placeholder="Selecione a dimensão"
      options={Object.entries(DIMENSIONS).map(([value, label]) => ({value, label}))}
      onChange={next => select(next)} isDisabled={pending} width="100%" />
    <Selector label="Grupo" value={value} placeholder="Selecione um grupo"
      options={[{value: '', label: 'Todos os grupos'}, ...profiles[dimension].map(row => ({value: row.label, label: label(row.label)}))]}
      onChange={next => select(dimension, next)} isDisabled={pending} width="100%" />
    <Button label="Limpar filtros" variant="secondary" onClick={() => select('platform')} isDisabled={pending} />
    <span role="status" className="filter-status">{pending ? 'Atualizando comparação…' : 'Comparação atualizada'}</span>
  </div>;
}
