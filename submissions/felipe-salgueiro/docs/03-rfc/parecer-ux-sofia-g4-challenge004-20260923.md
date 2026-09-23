<!-- Snapshot integral do parecer e síntese entregues pela Sofia em 23/09/2026; consolidação e ressalva de revisão pela Lia. Não é aprovação de implementação. -->

# Parecer UX — G4 Challenge 004

**Data:** 23/09/2026
**Responsável:** Sofia — UX, Time Dev
**Solicitante:** Felipe Salgueiro
**Destino:** insumo para Lia consolidar na RFC do Challenge 004
**Estado:** proposta UX concluída; não implementada, não validada em browser e não publicada

## Decisão UX

Usar Astryx de forma seletiva como base de componentes e padrões, com tema próprio inspirado somente em referências públicas atuais do G4 Educação. A interface não deve parecer Meta/Astryx genérico, Cadência nem uma reprodução não autorizada de produto oficial G4.

A jornada do Head de Marketing governa a arquitetura. A interface deve abrir por conclusão legível, apresentar um ou dois números contextualizados, indicar a ação candidata e permitir chegar à evidência e aos limites. Tabelas cruas não entram no topo.

## Três artefatos distintos

1. **Visualizador Ouro existente:** preservar `solution/prototype/index.html` e seu gerador como artefato técnico e auditável. Não redesenhar nem substituir silenciosamente.
2. **Relatório executivo HTML:** criar uma página separada que responda às oito perguntas obrigatórias em linguagem de decisão.
3. **Dashboard, simulador e chat:** tratar como diferencial interativo. O simulador é determinístico e hipotético; o chat apenas explica a recomendação selecionada, seus números e limites.

O botão **Ver relatórios** deve oferecer:

- **Análise de performance e estratégia**;
- **Explorar dados**;
- relatórios futuros somente como itens sinalizados “Em evolução”, nunca como conteúdo fictício.

Não dividir a navegação principal apenas entre orgânico e pago, nem reproduzir a arquitetura Bronze/Prata/Ouro ou as tabelas do banco como arquitetura de informação.

## Mapa das oito perguntas

| Pergunta do Head | Seção e ação | Componentes Astryx candidatos |
|---|---|---|
| 1. O que gera engajamento? | **Onde aparece o melhor sinal.** Comparar plataforma, formato, categoria e faixa de creator; priorizar recortes para teste. | `Layout`, `Card`, `Grid`, `Badge`, `Heading`, `Text` |
| 2. Patrocínio funciona? | **Patrocínio: diferença pequena e instável.** Mostrar flag, métricas, n, dispersão e limites; testar sem escala ou corte automático. | `Banner`, `Card`, `Badge`; `Table` somente no detalhe |
| 3. Qual audiência predomina? | Comparar idade/gênero predominantes e localização principal sem apresentar os rótulos como composição percentual. | `Tabs`/`TabList`, `Card`, `MetadataList` |
| 4. O que não funciona? | Separar desempenho inferior, recorte vazio e evidência insuficiente; propor redução, teste ou medição. | `Badge`, `Banner`, `EmptyState` |
| 5. Onde concentrar esforço? | Priorizar plataforma, formato, categoria e faixa; marcar frequência como não identificável. | `Card`, `Grid`, `List`, `Button` |
| 6. Qual política de patrocínio? | Apresentar thresholds como proposta de experimento, nunca como descoberta do dataset. Abrir simulador contextual. | `FormLayout`, `TextInput`, `Button`, `Card` |
| 7. O que parar? | Lista para reduzir, suspender como hipótese ou medir melhor, cada item ligado à evidência e ao limite. | `List`, `Badge`, `Collapsible` |
| 8. Quais quick wins? | Ações executáveis na semana: teste, instrumentação ou recorte prioritário. | `Card`, `List` |

## Contrato de leitura executiva

Cada bloco deve seguir a sequência:

> **Conclusão legível → 1–2 números contextualizados → ação candidata → evidência e limite**

Exemplo de patrocínio:

> **Patrocínio não mostra vantagem material neste cenário simulado.**
> Mediana de 10.100 views em ambos os grupos; interações/views de 19,9014% no patrocinado e 19,8977% no não patrocinado segundo a flag.
> **Ação:** testar recortes promissores com regra definida previamente.
> **Limite:** não há gasto, alcance, conversão, randomização ou janela comum.

## Wireframe textual

### Desktop

```text
┌──────────────────────────────────────────────────────────────────────┐
│ G4 Challenge 004                         [Ver relatórios ▾] [Método] │
├──────────────────────────────────────────────────────────────────────┤
│ [Análise de performance e estratégia] [Explorar dados]              │
├───────────────────────────────────────────────┬──────────────────────┤
│ Tese executiva                                │ Simulador hipotético │
│ Conclusão + 2 números + ação + limite         │ Custo informado     │
│                                               │ Views/interações ref.│
│ O que gera engajamento                        │ Vendas hipotéticas   │
│ Patrocínio                                    │ Resultados calculados│
│ Audiência predominante                        ├──────────────────────┤
│ O que não funciona                            │ Pergunte sobre esta  │
│                                               │ recomendação         │
│ Estratégia                                    │ Chat contextual      │
│ Onde concentrar                               │ [Abrir conversa]     │
│ Política de patrocínio                        └──────────────────────┘
│ O que parar
│ Quick wins da semana
│ Evidência e limitações [expandir]
└──────────────────────────────────────────────────────────────────────┘
```

“Explorar dados” pode conter filtros e tabela detalhada; a visão executiva não.

### Mobile

```text
[G4 Challenge 004]                [Relatórios]

[Performance e estratégia] [Explorar dados →]

[Tese executiva]
Conclusão
2 números
Ação
Evidência/limite

[O que gera engajamento]
[Patrocínio]
[Audiência]
[O que não funciona]
[Onde concentrar]
[Política]
[O que parar]
[Quick wins]

[Simular patrocínio]
[Conversar sobre a recomendação]
```

- Uma coluna.
- Tabs com rolagem horizontal e rótulos completos.
- Tabelas detalhadas viram cards comparativos ou região rolável explicitamente rotulada.
- Simulador e chat ficam após o contexto correspondente; podem ter CTA inferior persistente, sem cobrir conteúdo.
- Validação mobile real permanece obrigatória antes de aprovação UX.

## Identidade G4 e tokens

As referências oficiais atuais mostram uma identidade de alto contraste, linguagem empresarial direta e hierarquia tipográfica forte.

### Comprovado visualmente em propriedades G4

- Navy/azul muito escuro como base institucional.
- Coral/laranja no símbolo e em acentos.
- Branco como superfície e contraste.
- Tipografia sans-serif robusta.
- Marca geométrica G4 e comunicação voltada à aplicabilidade e execução.

### Aproximado — exige validação no CSS/asset oficial antes de implementar

| Token proposto | Valor provisório | Estado |
|---|---:|---|
| `--g4-navy-950` | `#111827` | aproximado |
| `--g4-navy-800` | `#1E293B` | aproximado |
| `--g4-coral-500` | `#F2675C` | aproximado |
| `--g4-surface` | `#FFFFFF` | visualmente consistente; hex trivial |
| `--g4-surface-muted` | `#F5F6F8` | aproximado |
| `--g4-border` | `#D9DDE5` | aproximado |
| fonte | sans geométrica/neo-grotesca | família exata não comprovada |

Esses valores não são manual de marca. A RFC deve exigir extração dos tokens do CSS ou assets oficiais antes da implementação. Também deve incluir transparência equivalente a: “Projeto desenvolvido para o Challenge 004; não é um produto oficial nem implica afiliação com o G4 Educação.”

Fontes oficiais consultadas:

- <https://g4educacao.com/>
- <https://g4educacao.com/blog>
- <https://g4educacao.com/sobre>

## Componentes e documentação Astryx

Usar Astryx seletivamente, com `Layout` como raiz da página e `AppShell` reservado ao chrome global. `Grid minChildWidth` é o padrão documentado para cards responsivos. `Table` é adequada à auditoria, não ao topo executivo. Não colocar componentes experimentais de gráficos no caminho crítico.

Documentação consultada:

- <https://github.com/felipeluissalgueiro/astryx>
- <https://github.com/felipeluissalgueiro/astryx/blob/main/packages/cli/README.md>
- <https://github.com/felipeluissalgueiro/astryx/blob/main/packages/core/README.md>
- <https://github.com/facebook/astryx/wiki/Contributing-Templates>

O CLI documenta `component`, `search`, `docs`, `template`, `theme build` e `doctor`. Ele não foi executado porque o clone Linux esperado não está presente e instalar dependências estava fora do escopo.

## Estados obrigatórios

- **Loading:** `Skeleton` que preserve a estrutura do resumo e dos cards; não mostrar zero temporário.
- **Empty:** “Nenhum recorte corresponde aos filtros” + **Limpar filtros**; não confundir com desempenho zero.
- **Insuficiente:** informar qual evidência falta e oferecer medir melhor ou definir experimento.
- **Error:** mensagem humana, opção de tentar novamente e acesso preservado à metodologia/evidência estática.
- **Chat indisponível:** relatório e simulador continuam funcionais; explicar indisponibilidade sem expor chave, modelo ou detalhes sensíveis.
- **Simulador inválido:** rejeitar custo negativo e vendas fracionárias; vazio significa não informado; zero vendas significa custo por venda não calculável.
- **Sucesso do simulador:** resultados hipotéticos permanecem rotulados como cenário, separados das métricas observadas.

## Limites dos dados que a UI deve preservar

- O dataset é simulado intencionalmente. Rankings são descritivos do cenário, não benchmark de mercado.
- `creator_id` é a chave canônica; `creator_name` é inconsistente e não deve rotular ranking.
- `creator_profile_eligible` usa regra histórica superada e `measure_better` é fixo; nenhum dos dois pode orientar a decisão.
- Datas aleatórias não sustentam frequência ótima, horário ideal ou tendência real.
- Views não são alcance, impressões, retenção nem pessoas únicas.
- Não há custo, receita, conversão ou atribuição; não existe ROI ou CAC observável.
- O simulador pode calcular custo por mil views, por interação e por venda hipotética. Custo por venda não é CAC.
- Leads, vendas, CRM, CAC e SLM devem aparecer somente como não mensurados ou evolução futura, nunca como zero ou capacidade já entregue.

## Riscos técnicos e de adoção

- Astryx está em beta/pre-1.0 e o núcleo atual requer React 19; há risco de mudanças incompatíveis.
- O fork canônico existe, mas o clone Linux documentado como `/home/felipe/astryx` não foi encontrado neste host.
- Astryx fornece CSS pré-compilado, temas por custom properties e integração Next.js sem plugin de build, mas a compatibilidade precisa de spike antes de produção.
- `@astryxdesign/lab` e `@astryxdesign/vega` não são pacotes publicados estáveis; gráficos experimentais não devem entrar no caminho crítico.
- O bundle deve ser medido após a seleção final de componentes.
- Proteção nativa da Vercel, entitlement/cobrança e acesso dos avaliadores seguem pendentes.
- Chat depende de rota servidor, chave OpenRouter exclusiva, limite de consumo e proteção contra abuso.
- A ausência de custos, conversões, alcance e retenção impede ROI, CAC ou promessa de entrega.
- Datas aleatórias impedem recomendação de frequência.

## Critérios de aceite de usabilidade

- As oito perguntas são localizáveis sem interpretação da arquitetura de dados.
- Cada recomendação possui evidência, denominador, n, dispersão, limite e ação.
- Observado, hipótese e futuro têm tratamento visual distinto.
- O relatório continua compreensível sem abrir chat ou simulador.
- Não há navegação primária dividida apenas em orgânico/pago.
- Foco visível, operação por teclado, contraste e textos alternativos.
- Validação em desktop e celular real.
- Nenhum estado vazio ou falha aparece como zero.
- Simulador nunca chama custo por venda de CAC ou ROI.
- Visualizador Ouro permanece preservado e acessível separadamente.

## Pronto para a RFC

- Arquitetura de informação e hierarquia executiva.
- Separação dos três artefatos.
- Mapeamento das oito perguntas.
- Componentes Astryx candidatos.
- Estados obrigatórios.
- Wireframes desktop/mobile.
- Limites analíticos e regras do simulador.
- Riscos técnicos e critérios de aceite UX.

## Pendente para a RFC ou implementação

- Exportação e contrato JSON Ouro final.
- Tokens e fonte G4 extraídos de fonte técnica oficial.
- Thresholds determinísticos de suficiência e patrocínio.
- Template Astryx final após disponibilidade do CLI/clone.
- Modelo/configuração OpenRouter e orçamento.
- Entitlement da proteção Vercel.
- Benchmark externo comparável.
- Spike de compatibilidade React 19, bundle e acessibilidade.
- Teste em navegador e dispositivo móvel real.

## Síntese enviada à Lia

Direção: preservar `solution/prototype/index.html` como visualizador Ouro; criar relatório executivo HTML separado cobrindo os oito itens; tratar dashboard, simulador e chat como diferencial. O topo segue conclusão → 1–2 números contextualizados → ação → evidência, sem tabela crua e sem navegação orgânico/pago.

Astryx recomendado seletivamente: `Layout`, `LayoutHeader`, `LayoutContent`, `Tabs`/`TabList`, `Card`, `Grid`, `Badge`, `Banner`, `Table` apenas em Explorar dados, `EmptyState`, `Skeleton`, `Button`, `TextInput` e `FormLayout`; `AppShell` apenas como chrome. Evitar `lab`/`vega` não publicados.

Desktop: header G4 + Ver relatórios; abas Performance e estratégia / Explorar dados; coluna principal com resumo e oito blocos; rail com simulador e chat contextual. Mobile: header compacto, tabs horizontais, cards em uma coluna, acesso persistente a simulador/chat e tabela auditável adaptada.

Identidade G4 observável: navy escuro, coral, branco e sans robusta; hex e família exatos não foram comprovados e permanecem aproximados até validação de CSS/asset oficial. Estados: loading, empty, insuficiente, error e chat indisponível, sem converter ausência em zero.

Dados: sintéticos; `creator_id` canônico e nome inconsistente; não usar eligibility histórica nem `measure_better`; datas não sustentam frequência; sem custo, conversão, alcance ou retenção; simulador explicitamente hipotético.

Riscos: Astryx beta/pre-1.0, React 19, clone Linux ausente; proteção Vercel e controles OpenRouter pendentes. Aceites: oito perguntas cobertas, recomendação rastreável, teclado/mobile real, observado versus hipótese separados e limites explícitos.

## Registro do trabalho realizado

Sofia leu integralmente o perfil operacional obrigatório de Felipe, `times/dev/sofia/CLAUDE.md`, `memory/STATE.md`, `memory/decisions.md`, `context/astryx-ui-standard.md`, a skill canônica `astryx-planejar-ui`, o PRD v0.5, o gate técnico de Vitor, o relatório final dos dados e os READMEs da solução e do protótipo. Investigou o fork Astryx e referências públicas oficiais do G4.

Não editou o fork G4, não instalou dependências, não executou o pipeline, não acessou credenciais, não fez deploy, não publicou e não criou issues. Este parecer é insumo UX para a RFC, não implementação, validação final ou aprovação de publicação.

## Nota de revisão da Lia — limites de interpretação

O parecer acima é preservado como proposta da Sofia, não como validação independente de todas as afirmações. No exemplo executivo, “não mostra vantagem material” deve ser lido apenas como diferença descritiva pequena: não foi estabelecido limiar econômico, equivalência estatística ou efeito causal. A redação final deverá dizer “diferença observada pequena; vantagem econômica não demonstrável com estes dados”. Os aceites listados são critérios futuros, não testes executados. Componentes Astryx são candidatos: API, versão e compatibilidade precisam ser conferidas antes da implementação. Tokens G4 são aproximados, não comprovados como oficiais.

Observações visuais e consultas de fontes são atribuídas à investigação da Sofia; a Lia não revalidou independentemente a identidade visual do site G4 nesta integração. Este documento é a fonte de registro no Marketing; a cópia no fork é snapshot para avaliação, não uma fonte editável independente.
