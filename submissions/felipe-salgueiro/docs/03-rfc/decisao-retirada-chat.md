# Redução de escopo — chat retirado

Decisão explícita de Felipe após revisão da interface. Esta decisão substitui
o escopo de chat no PRD v0.5, RFC-001 e MAR-102 para esta entrega.

- Retirar chat, endpoint, transporte OpenRouter, configuração de exemplo e
  testes exclusivos da funcionalidade. Código recuperável no histórico Git.
- Não provisionar modelo, chave, autenticação ou quota para a funcionalidade.
- Manter dashboard, simulador determinístico, relatório e explorador.
- Home: três decisões, evidência legível e plano de ação proposto para a semana.
  Não representar dados sintéticos como resultados semanais observados.
- Conferência: links navegáveis às seções do relatório e JSON acessível.
- Não é autorização de deploy, alteração de DNS ou encerramento de issues.

Verificações: lint, TypeScript, build; 18 testes unitários e 30 de navegador.
API removida retorna 404; links de conteúdo/patrocínio abrem âncoras reais.
QA por imagem em desktop e viewport mobile; sem aceite humano presumido.
Documentos e testes históricos permanecem evidência da evolução, não escopo atual.
