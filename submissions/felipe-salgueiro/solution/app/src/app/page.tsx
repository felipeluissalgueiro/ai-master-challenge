import {Layout} from '@astryxdesign/core/Layout';
import snapshot from '../../../data/app/dashboard.json';
import {parseDashboard} from '@/lib/dashboard';
import {PerformanceDashboard} from '@/components/performance/dashboard';

export default async function HomePage({searchParams}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const data = parseDashboard(snapshot);
  return <Layout height="auto" contentWidth={1180} padding={6}
    content={<PerformanceDashboard data={data} query={await searchParams} />} />;
}
