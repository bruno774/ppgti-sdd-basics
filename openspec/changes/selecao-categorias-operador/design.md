## Context

Ver [proposal.md](proposal.md) para a motivação. O backend ainda não implementa perfis de acesso, catálogo persistido de categorias, nem retenção de texto de origem para reprocessamento — este design cobre como introduzir essas três peças de forma coerente com a separação de camadas já adotada no projeto (extração, detecção, revisão/seleção, mascaramento, auditoria; ver [AGENTS.md](../../../AGENTS.md)).

## Goals / Non-Goals

**Goals:**
- Definir onde o perfil ativo, o catálogo de categorias e o estado de sessão para reprocessamento vivem na arquitetura (camada de domínio vs. camada web Django).
- Definir a estratégia de validação de unicidade de prefixo/tipo canônico ao cadastrar categorias customizadas.
- Definir a estratégia de retenção e expurgo do texto de origem que permite repetir o processamento sem reenvio.

**Non-Goals:**
- Definir o conjunto completo de permissões dos perfis `gestor` e `suporte` (aguarda especificação própria de perfis/autorização, ver "Open Questions").
- Especificar a interface visual da tela de seleção (tratado como detalhe de implementação em `tasks.md`, não requisito de comportamento).

## Decisions

- **Catálogo como dado de domínio, não hardcoded no código de mascaramento.** As categorias padrão são seedadas como registros de origem `padrao` em um repositório de catálogo (independente de Django, validado por Pydantic), e categorias customizadas são registros de origem `customizada` no mesmo repositório. Alternativa considerada: manter o catálogo padrão como constante em código e categorias customizadas em banco separado — rejeitada por criar duas fontes de verdade e dificultar a validação de unicidade de prefixo entre padrão e customizada.
- **Perfil como atributo de sessão, não de usuário persistido nesta change.** O perfil ativo (`operador` por padrão) é resolvido por sessão de trabalho; a troca explícita para `gestor`/`suporte` é uma ação de sessão auditável, não uma mudança de conta de usuário permanente. Alternativa considerada: modelar perfil como papel (role) persistido por usuário no banco — adiada porque exige um sistema de autenticação/autorização ainda não definido no projeto (ver "Open Questions").
- **Retenção do texto de origem por `id_origem`, escopada à sessão, com expiração configurável.** Isso permite repetir o processamento sem reenviar o conteúdo, mantendo o requisito de que a repetição sempre parte do texto original. Alternativa considerada: persistir o texto de origem de forma duradoura para reprocessamento futuro entre sessões — rejeitada por aumentar a superfície de exposição de dados confidenciais além do necessário (ver RNF01 em [docs/requisitos/requisitos-nao-funcionais.md](../../../docs/requisitos/requisitos-nao-funcionais.md)).
- **Validação de unicidade de prefixo/tipo canônico centralizada em uma única função de domínio**, chamada tanto pelo seed do catálogo padrão quanto pelo cadastro de categorias customizadas, evitando duas implementações divergentes da mesma regra.

## Risks / Trade-offs

- [Ausência de modelo de perfis/autenticação já implementado] → Mitigação: tratar perfil como atributo de sessão nesta change (ver Decisions); registrar como bloqueio explícito para qualquer refinamento que exija permissões diferenciadas reais entre `gestor` e `suporte`.
- [Retenção de texto de origem em sessão aumenta a janela de exposição de dados confidenciais] → Mitigação: expiração configurável e curta por padrão, expurgo explícito ao fim da sessão, e erro claro (não silencioso) quando o texto expira antes de uma repetição solicitada.
- [Cadastro de categorias customizadas mal definidas pode gerar falsos positivos na detecção] → Mitigação: a validação nesta change cobre apenas unicidade de tipo/prefixo; qualidade da categoria (limiar de confiança, ambiguidade) permanece responsabilidade de revisão humana, fora do escopo desta change.

## Open Questions

- Qual é o tempo padrão de retenção do texto de origem em sessão antes de exigir novo envio? Pode ser respondido durante a implementação (Fase 4 do plano em [docs/to-do-spec006.md](../../../docs/to-do-spec006.md)) sem alterar os requisitos desta spec, desde que o comportamento de expiração continue existindo.
- Os perfis `gestor` e `suporte` terão, no futuro, permissões que afetam a seleção de categorias (por exemplo, `gestor` podendo restringir quais categorias um `operador` pode desmarcar)? Isso não afeta esta change, mas pode gerar uma capability adicional depois.
