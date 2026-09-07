## Why

Um dos quatro canais de entrada previstos é a captura, por uma extensão de navegador, do conteúdo de uma caixa de texto em uma página web, mediante ação explícita do operador, com devolução opcional do texto anonimizado ao mesmo campo. Isso está descrito em [docs/especificacoes/004-extensao-navegador/spec.md](../../../docs/especificacoes/004-extensao-navegador/spec.md), mas não existe nenhum código de extensão no repositório (apenas a pasta reservada `src/extension/`).

## What Changes

- Introduzir a capability `extensao-navegador`, cobrindo a captura explícita de campo de texto, o envio ao backend de detecção/anonimização (canal `extensao` da capability `entrada-multicanal`), a exibição de entidades detectadas para seleção de categorias, e a devolução do texto anonimizado ao campo de origem.
- Formalizar como requisitos verificáveis: ausência de captura implícita, permissões mínimas no manifesto, e ausência de persistência do conteúdo capturado além da sessão em memória.

## Capabilities

### New Capabilities
- `extensao-navegador`: captura explícita de campo de texto por extensão de navegador, envio para detecção/anonimização e devolução do resultado ao campo de origem.

### Modified Capabilities
(nenhuma)

## Impact

- Código novo em `src/extension/` (JavaScript/TypeScript, Manifest V3), consumindo o canal `extensao` já definido em `entrada-multicanal` e o fluxo de seleção de categorias de `selecao-categorias`.
- Depende de `entrada-multicanal` (contrato de entrada) e de `mascaramento-pseudonimizacao` (para receber o texto anonimizado a devolver ao campo).
