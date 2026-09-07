## Why

Depois que entidades são detectadas (capability `deteccao-entidades`) e o operador seleciona categorias (capability `selecao-categorias`), o sistema precisa substituir cada entidade selecionada por um marcador de pseudo-anonimização estável (`prefixo+índice`), preservando a distinção entre entidades e o sentido semântico do texto. Hoje não existe nenhuma implementação de mascaramento no repositório — apenas a especificação em [docs/especificacoes/003-mascaramento-pseudonimizacao/spec.md](../../../docs/especificacoes/003-mascaramento-pseudonimizacao/spec.md).

## What Changes

- Introduzir a capability `mascaramento-pseudonimizacao`, cobrindo a aplicação de marcadores `prefixo+índice` sobre o texto, com reaproveitamento de índice para a mesma entidade repetida, aplicação sem invalidar offsets (direita para a esquerda), e relatório de contagem por tipo sem dados pessoais.
- Formalizar como requisitos verificáveis: numeração apenas das categorias selecionadas (RF03), preservação de entidades não selecionadas, ausência do valor original na saída, e prevenção de sobreposição inválida entre marcadores.

## Capabilities

### New Capabilities
- `mascaramento-pseudonimizacao`: substituição de entidades selecionadas por marcadores `prefixo+índice`, preservando distinção entre entidades e sentido semântico do texto.

### Modified Capabilities
(nenhuma)

## Impact

- Código novo em `src/backend/` para aplicação de marcadores sobre o texto a partir da lista de `EntidadeDetectada` (capability `deteccao-entidades`) e da seleção de categorias (capability `selecao-categorias`).
- Depende de `deteccao-entidades` e de `selecao-categorias`; é pré-requisito para a repetição de processamento descrita na especificação 006 e para `auditoria-operacoes` (evento de anonimização).
