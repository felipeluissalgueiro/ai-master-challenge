'use client';

import {useSearchParams} from 'next/navigation';
import {Button} from '@astryxdesign/core/Button';

type QueryPreservingButtonProps = {
  href: string;
  label: string;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  target?: string;
  rel?: string;
};

export function QueryPreservingButton({href, ...buttonProps}: QueryPreservingButtonProps) {
  const searchParams = useSearchParams();
  const query = searchParams.toString();
  const destination = query ? `${href}?${query}` : href;

  return <Button href={destination} {...buttonProps} />;
}
