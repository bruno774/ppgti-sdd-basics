## Context

Ver [proposal.md](proposal.md) para a motivação. Já existe extração de PDF em `src/backend/pdf_extraction.py` (arquivo em disco) e `src/backend/pdf_binary_extraction.py` (bytes), cada uma com sua própria hierarquia de exceções. Não existe ainda extração de DOCX, aceitação de texto colado, nem contrato comum de saída entre canais.

## Goals / Non-Goals

**Goals:**
- Definir um contrato `DocumentoOrigem` único, usado pelos quatro canais, sem forçar reescrita da extração de PDF já implementada.
- Definir como cada canal mapeia seus próprios erros (arquivo corrompido, protegido, sem texto) para um conjunto de exceções coerente entre canais.

**Non-Goals:**
- Implementar OCR para PDFs digitalizados (fora de escopo, ver `docs/requisitos/requisitos-funcionais.md`).
- Implementar a extensão de navegador em si (capability separada `extensao-navegador`); esta capability só define o contrato de entrada que a extensão consome.

## Decisions

- **Contrato `DocumentoOrigem` como modelo Pydantic em módulo próprio**, independente de Django, para reaproveitamento pelos quatro canais e pela extensão. Alternativa considerada: cada canal retornar apenas uma string — rejeitada por perder a informação de canal/origem necessária para auditoria (RF06.1).
- **Extração de PDF existente é envolvida (wrapped), não reescrita.** Uma função adaptadora chama `extract_pdf_text` já implementada e constrói o `DocumentoOrigem` a partir do resultado, preservando as exceções existentes (`PdfExtractionError`, `PdfTextUnavailableError`). Alternativa considerada: reescrever a extração de PDF do zero dentro do novo módulo — rejeitada por duplicar lógica já testada.
- **DOCX usa `python-docx`**, iterando parágrafos do documento (`document.paragraphs`), com tratamento de exceção para arquivo corrompido/inválido mapeado para um erro de domínio próprio (`DocxExtractionError`).
- **Texto colado e extensão de navegador não têm "extração", apenas validação de tamanho** antes de produzir o `DocumentoOrigem`; a diferença entre os dois canais é apenas o valor do campo `canal` e a presença de `identificador_origem` para a extensão.

## Risks / Trade-offs

- [Bibliotecas de parsing de DOCX podem ter vulnerabilidades conhecidas] → Mitigação: manter `python-docx` atualizado e validar tamanho/extensão antes do parsing, como já ocorre com PDF.
- [Unificar contrato de erro entre PDF (já implementado com suas próprias exceções) e os demais canais pode gerar inconsistência] → Mitigação: manter as exceções específicas de cada canal, mas garantir que todas herdem de uma exceção base comum de extração, permitindo tratamento uniforme pela camada de detecção.
