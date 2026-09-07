## Why

O sistema precisa aceitar conteúdo de quatro canais distintos — PDF pesquisável, DOCX, texto colado/clipboard e captura via extensão de navegador — e entregar, para todos eles, o mesmo contrato normalizado de texto de origem, para que a detecção de entidades (capability separada) seja agnóstica ao canal de entrada. Hoje só existe extração de PDF (`src/backend/pdf_extraction.py`, `src/backend/pdf_binary_extraction.py`); não há suporte a DOCX, texto colado ou extensão, nem um contrato único de saída entre os canais. Isso está descrito em [docs/especificacoes/001-entrada-multicanal/spec.md](../../../docs/especificacoes/001-entrada-multicanal/spec.md), mas ainda não existe como capability OpenSpec.

## What Changes

- Introduzir a capability `entrada-multicanal`, com um contrato normalizado `DocumentoOrigem` (canal, texto, identificador de origem, tamanho em bytes) comum aos quatro canais.
- Formalizar como requisitos verificáveis: extração de PDF pesquisável (reaproveitando o código existente), extração de DOCX, aceitação de texto colado/clipboard, aceitação de captura via extensão de navegador, e rejeição de entradas inválidas (formato não suportado, corrompido, protegido por senha sem credencial, sem camada de texto).
- Não remove nem quebra a extração de PDF já implementada; adapta sua saída para o contrato `DocumentoOrigem` comum aos demais canais.

## Capabilities

### New Capabilities
- `entrada-multicanal`: extração/normalização de texto a partir de PDF, DOCX, texto colado/clipboard e extensão de navegador, produzindo um contrato único (`DocumentoOrigem`) para a etapa de detecção.

### Modified Capabilities
(nenhuma — `openspec/specs/` ainda não tem nenhuma capability existente)

## Impact

- Código afetado: `src/backend/pdf_extraction.py` e `src/backend/pdf_binary_extraction.py` (adaptação de saída para o contrato comum); novos módulos para DOCX, texto colado e extensão.
- Nova dependência: `python-docx` (já registrada em [requirements.txt](../../../requirements.txt)).
- Depende de nada; é pré-requisito para `deteccao-entidades` e `extensao-navegador`.
