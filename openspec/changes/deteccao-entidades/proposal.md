## Why

O sistema precisa identificar, no texto normalizado produzido pela entrada multicanal, ocorrências de dados pessoais e sensíveis do catálogo de entidades (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`), com posição, confiança e origem, sem aplicar nenhuma substituição nesta etapa. Hoje não existe nenhuma implementação de detecção no repositório — apenas a especificação em [docs/especificacoes/002-deteccao-entidades/spec.md](../../../docs/especificacoes/002-deteccao-entidades/spec.md) e o catálogo já modelado na capability `selecao-categorias` (`src/backend/categorias.py`).

## What Changes

- Introduzir a capability `deteccao-entidades`, cobrindo a identificação de entidades no texto, com tipo canônico, intervalo `[início, fim)`, confiança, origem (`regra`/`modelo`/`combinado`) e sinalização de revisão obrigatória para tipos sensíveis abaixo do limiar de confiança.
- Formalizar como requisitos verificáveis: determinismo da detecção, extensibilidade do catálogo sem alterar o fluxo principal, e ausência de inferência de tipos sensíveis por estereótipo ou contexto ambíguo.
- Reaproveita o catálogo já modelado em `src/backend/categorias.py` (capability `selecao-categorias`) como fonte dos tipos canônicos e do sinalizador `sensivel`.

## Capabilities

### New Capabilities
- `deteccao-entidades`: identificação de entidades pessoais e sensíveis no texto normalizado, com tipo, posição, confiança e origem, sem aplicar substituição.

### Modified Capabilities
(nenhuma)

## Impact

- Código novo em `src/backend/` para regras/detecção (ex.: expressões regulares para `CPF`, `EMAIL`, `TELEFONE`; heurísticas ou modelo NLP para `NOME`, `ENDERECO` e tipos sensíveis).
- Depende de `entrada-multicanal` (consome `DocumentoOrigem`) e de `selecao-categorias` (consome o catálogo de tipos); é pré-requisito de `mascaramento-pseudonimizacao`.
- Dependência potencial de spaCy (já registrada em [requirements.txt](../../../requirements.txt)) para tipos que exigem NLP; a escolha final de biblioteca por tipo fica a critério da implementação, desde que atenda aos critérios de determinismo e confiança da spec.
