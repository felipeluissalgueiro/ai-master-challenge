import type {ExplainDependencies} from './explanation';
import {generateExplanation} from './openrouter';

/**
 * Deployment protection and a durable global quota are NOT configured yet.
 * No env flag or client header may pretend they exist. Replace these adapters
 * only after real verification; provider credentials alone cannot enable chat.
 */
export function chatDependencies(): ExplainDependencies {
  return {
    available: false,
    authorize: async () => false,
    reserveCall: async () => false,
    generate: (context, question) => generateExplanation(context, question, {
      apiKey: process.env.OPENROUTER_API_KEY ?? '', model: process.env.OPENROUTER_MODEL ?? '',
    }),
  };
}
