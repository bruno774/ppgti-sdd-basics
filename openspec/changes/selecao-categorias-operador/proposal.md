## Why

O operador precisa poder ajustar, antes de qualquer processamento, quais categorias de dados pessoais/sensíveis serão anonimizadas, respeitando três regras do PRD ainda não capturadas em uma spec-driven change formal: o perfil `operador` é sempre o padrão da sessão (outros perfis exigem troca explícita), o catálogo de categorias pode ser estendido mas nunca reduzido nas categorias padrão, e o processamento pode ser repetido sobre o mesmo texto de origem com uma seleção diferente de categorias. Essas regras já estão documentadas em [docs/especificacoes/006-selecao-categorias-operador/spec.md](../../../docs/especificacoes/006-selecao-categorias-operador/spec.md) e em [docs/to-do-spec006.md](../../../docs/to-do-spec006.md), mas ainda não existem como capability formal em `openspec/specs/`, o que impede rastrear esse comportamento pelo fluxo padrão de propose/apply/archive do OpenSpec.

## What Changes

- Introduzir a capability `selecao-categorias`, cobrindo: perfil ativo da sessão (`operador` por padrão), seleção de categorias antes do processamento, cadastro de categorias customizadas (sem remoção das padrão) e repetição do processamento sobre o texto de origem com nova seleção.
- Formalizar, como requisitos verificáveis (EARS/`SHALL`), as regras já descritas em prosa na especificação 006: perfil padrão, catálogo padrão imutável, unicidade de prefixo de marcador, e reprocessamento a partir do texto de origem (nunca do resultado já anonimizado).
- Não altera código existente (o projeto ainda não tem implementação da camada de seleção/catálogo); esta change cria apenas o contrato de comportamento a ser implementado.

## Capabilities

### New Capabilities
- `selecao-categorias`: seleção de categorias de anonimização pelo operador, perfil padrão da sessão, catálogo padrão não removível com extensão por categorias customizadas, e repetição do processamento sobre o texto de origem com nova seleção.

### Modified Capabilities
(nenhuma — `openspec/specs/` ainda não tem nenhuma capability existente)

## Impact

- Código afetado: ainda nenhum (`src/backend/` não implementa catálogo, perfis nem seleção hoje); esta change define o contrato antes da Fase 1 do plano em [docs/to-do-spec006.md](../../../docs/to-do-spec006.md).
- Documentação: `docs/especificacoes/006-selecao-categorias-operador/spec.md` passa a ser a referência histórica em português; a capability OpenSpec se torna a fonte formal de requisitos verificáveis para esta funcionalidade.
- Dependências: nenhuma dependência nova; reaproveita o catálogo de entidades e os requisitos RF03 já existentes em `docs/requisitos/`.
