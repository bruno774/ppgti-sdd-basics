## Why

Toda operação relevante do sistema (detecção, seleção de tipos, anonimização, exportação) precisa ser registrada em um log de auditoria íntegro, não editável e sem nenhum dado pessoal, conforme [docs/especificacoes/005-auditoria/spec.md](../../../docs/especificacoes/005-auditoria/spec.md). Hoje não existe nenhuma implementação de auditoria no repositório.

## What Changes

- Introduzir a capability `auditoria`, cobrindo o registro de eventos append-only para detecção, seleção, anonimização e exportação, com consulta por período, operador ou canal.
- Formalizar como requisitos verificáveis: ausência de dado pessoal em qualquer campo do evento, imutabilidade dos registros pela interface padrão, e um evento distinto por execução (reaproveitando o conceito de `ExecucaoAnonimizacao` já desenhado na capability `selecao-categorias`).

## Capabilities

### New Capabilities
- `auditoria`: registro append-only de eventos de detecção, seleção, anonimização e exportação, sem dados pessoais, com consulta por período/operador/canal.

### Modified Capabilities
(nenhuma)

## Impact

- Código novo em `src/backend/` para o modelo de evento de auditoria e a função de registro/consulta.
- Consumido por `selecao-categorias` (troca de perfil, cadastro de categoria, seleção e repetição de execução), `deteccao-entidades` e `mascaramento-pseudonimizacao` (evento de detecção/anonimização); esta capability não depende de nenhuma delas para existir isoladamente (o contrato de evento pode ser definido e testado antes da integração).
