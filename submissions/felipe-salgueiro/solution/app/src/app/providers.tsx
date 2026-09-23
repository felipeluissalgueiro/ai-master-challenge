'use client';

import type {ReactNode} from 'react';
import Link from 'next/link';
import {LinkProvider} from '@astryxdesign/core/Link';
import {Theme} from '@astryxdesign/core/theme';
import {neutralTheme} from '@astryxdesign/theme-neutral/built';

export function Providers({children}: {children: ReactNode}) {
  return (
    <Theme theme={neutralTheme} mode="light">
      <LinkProvider component={Link}>{children}</LinkProvider>
    </Theme>
  );
}
