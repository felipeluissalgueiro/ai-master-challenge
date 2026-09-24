# MAR-102 — interface, contexto e transporte do chat

Data: 23/09/2026. Lia, modo A e autorrevisão autorizada.
Estado: código integrado e testado com transporte simulado; **inferência real
desabilitada**, sem autenticação ou quota global provisionadas. Não é Done.

## Implementado

- Consulta contextual em cada recomendação; somente ID, snapshot e pergunta
  seguem do navegador. Servidor resolve a evidência, não aceita fatos do cliente.
- Pergunta até 1.500 caracteres, body até 8 KiB, contexto até 48 mil caracteres,
  saída até 600 tokens, timeout do transporte 30s, sem retries/fallback automático.
- Modelo somente por configuração do servidor, JSON schema, IDs de evidência
  validados e resposta exibida como texto, sem HTML executável.
- Rejeição de origem divergente, snapshot antigo, ID desconhecido, campos extras,
  referências falsas e saída truncada. Erros não expõem corpo do provedor.
- Envio duplicado bloqueado na UI; edição/unmount aborta e invalida resposta antiga.
- Fronteiras separadas para autenticação, reserva atômica durável e transporte.

**A política real nega todos os acessos e retorna 503.** Não há variável que
simule proteção pronta. Chave/modelo sozinhos não habilitam a rota.
Os adapters de autorização e quota ainda precisam de implementação real e
validação da infraestrutura escolhida; não confundir testes com mocks com esse aceite.

## Evidência dos gates na entrega

- Lint, TypeScript e build: PASS.
- Unitários: 27/27 PASS; nove novos cenários de chat/contexto/transporte.
- Browser: 32/32 PASS, 16 desktop e 16 mobile.
- Rota real sem proteção: 503; simulador permanece utilizável.
- Sucesso, texto HTML inerte e resposta atrasada: browser com interceptação
  explícita de transporte, não resposta real de OpenRouter.
- Busca em .next/static por nomes de configuração, endpoint de provedor e
  credencial sintética de teste: nenhum resultado. Chave real não foi lida.
- Nenhum screenshot, vídeo, deploy, autenticação de produção ou chamada paga.

O contexto inicial de audiência excedeu o limite; foram mantidos os resumos
auditados dos cruzamentos e omitida a listagem completa de células, com limite
explícito no contexto. Não foram amostradas linhas nem recalculadas estatísticas.
Seletores mobile foram restritos ao conteúdo ativo para não colidir com os
fragmentos transitórios do streaming Next. Rodada final passou sem retries.

## Dependências para habilitação

1. Verificar proteção real em página e API no projeto/deployment escolhido;
   não presumir benefício pelo nome do plano.
2. Implementar controle atômico/durável global, com valores aprovados, antes de
   substituir o adapter bloqueado. Contador local não serve.
3. Escolher modelo compatível com structured outputs; instalar chave exclusiva
   no servidor pelo canal autorizado. Configurar orçamento é atribuição de Felipe.
4. Autorizar e executar teste real de inferência e proteção. Prompts não garantem
   ausência de alucinação; validar referências não comprova cada afirmação.

## Investigação sem alteração externa

Consulta oficial identificou que Password Protection no Pro pode ter cobrança
adicional por projeto; o plano pago não foi tratado como autorização de cobrança.
WAF limita por região, portanto não é um contador global durável para este contrato.
A CLI Vercel retornou uma página de 20 projetos; consulta paginada, não censo nem
prova de ausência. Nenhum projeto/configuração foi criado ou alterado.

Fontes consultadas:
- [OpenRouter — contrato de chat](https://openrouter.ai/docs/api_reference/overview).
- [Vercel — Password Protection e preço](https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/password-protection).
- [Vercel — escopo regional do rate limiting](https://vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting).

As skills de autenticação e variáveis Vercel orientaram a separação de
configuração/segredo e habilitação. Não foram provisionados Clerk/Auth0/Descope.
