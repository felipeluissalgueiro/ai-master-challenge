import snapshot from '../../../../../data/app/dashboard.json';
import {parseDashboard} from '@/lib/dashboard';
import {explainRequest} from '@/lib/server/explanation';
import {chatDependencies} from '@/lib/server/chat-policy';

export const runtime = 'nodejs';
export const maxDuration = 40;
export async function POST(request: Request) {
  return explainRequest(request, parseDashboard(snapshot), chatDependencies());
}
