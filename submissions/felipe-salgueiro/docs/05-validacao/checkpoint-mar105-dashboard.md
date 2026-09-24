# MAR-105 — dados conectados ao dashboard

Data: 23/09/2026. Execução: Lia, modo A, autorrevisão autorizada.
Implementado e testado; não é encerramento da issue, QA visual aprovado ou deploy.

## Entrega

- Home consome o JSON canônico MAR-99 sem duplicação ou SQLite em runtime.
- Panorama com 52.214 posts, mediana 19,899% e 33/60 comparações acima nos patrocinados.
- Sete dimensões disponíveis no painel: plataforma, formato, categoria, quartil de
  seguidores do post e três rótulos predominantes de audiência.
- Filtro de uma dimensão/valor; vazio e combinação não exportada têm mensagens e limpeza.
- Oito recomendações ligadas a evidência, regra, snapshot, ação e limite.
- Ausência de custo/receita/CRM/benchmark não vira zero. Simulador segue separado.

## Contrato e revisão

Validação de unidades percent/percentage_points, contagens reconciliadas,
resumos numéricos, IDs únicos e referências das oito recomendações.
Contrato inválido lança erro para o boundary do app; não renderiza resultado parcial.
Filtros afetam apenas o painel de comparação, nunca as conclusões gerais.
Não há mediana de medianas ou classificação financeira inventada.
Faixas mínimo/máximo exibidas são extremos das medianas já exportadas, não nova
inferência estatística. Identidade navy/coral existente preservada.

O Turbopack inicialmente não resolvia o JSON fora de app/. A raiz de resolução
e tracing foi ajustada para solution/, com caminho relativo. Não foi criada
uma cópia concorrente do snapshot. O deploy deverá incluir essa pasta.

## Verificações reais na branch de entrega

- ESLint: PASS.
- Unitários: 18/18 PASS, sendo seis novos testes do contrato/filtros.
- Build Next e TypeScript: PASS; home renderizada no servidor por query.
- Playwright: 26/26 PASS, 13 desktop e 13 mobile, incluindo seis novos cenários.
- Busca de SQLite/DB em .next: nenhum arquivo encontrado.
- Diff whitespace: PASS.

Falhas corrigidas durante a integração: título de grupo a 17px foi elevado
para 18px; seletores textuais/label globais colidiam com conteúdo transitório
duplicado. Foram delimitados ao conteúdo principal, sem remover as asserções.
Na primeira rodada integrada houve 25/26; após essa correção, 26/26.

## Pendências

Não houve screenshots, gravação, QA visual por imagem, aceite humano, uso de
credencial, chamada LLM ou deploy. Relatórios/prototype em revisão não foram
integrados. Autorrevisão não foi apresentada como revisão independente.
Chat contextual, acesso protegido e limite de consumo são a próxima frente.
O teste de contrato inválido foi unitário; falha de fonte em runtime não foi
injetada no navegador. Não declarar essa camada como validada.
