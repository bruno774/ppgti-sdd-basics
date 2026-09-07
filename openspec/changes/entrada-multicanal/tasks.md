## 1. Contrato de dados

- [ ] 1.1 Modelar `DocumentoOrigem` (canal, texto, identificador_origem, tamanho_bytes) com validação Pydantic e verificar com teste que instâncias válidas para os quatro canais (`pdf`, `docx`, `texto`, `extensao`) são aceitas
- [ ] 1.2 Definir hierarquia de exceções base (`EntradaMulticanalError`) e garantir que exceções específicas de cada canal herdem dela, verificando com teste de tipo (`isinstance`)

## 2. Canal PDF (adaptação do existente)

- [ ] 2.1 Criar função adaptadora que chama `extract_pdf_text` existente e retorna `DocumentoOrigem(canal="pdf", ...)`, verificando com teste que o texto e o canal são corretos
- [ ] 2.2 Verificar com teste que erros já existentes (`PdfExtractionError`, `PdfTextUnavailableError`) continuam sendo levantados sem alteração de comportamento

## 3. Canal DOCX

- [ ] 3.1 Implementar extração de texto de DOCX com `python-docx`, preservando parágrafos, e verificar com teste que um DOCX válido produz `DocumentoOrigem(canal="docx", ...)` com o texto esperado
- [ ] 3.2 Implementar rejeição de DOCX corrompido ou inválido com erro acionável e verificar com teste que a exceção é levantada sem processar parcialmente o conteúdo
- [ ] 3.3 Implementar validação de tamanho máximo e extensão de arquivo antes do parsing, verificando com teste que arquivos acima do limite ou com extensão inválida são rejeitados antes de abrir o documento

## 4. Canal texto colado/clipboard e canal extensão

- [ ] 4.1 Implementar função que aceita uma string e produz `DocumentoOrigem(canal="texto", ...)`, validando o limite de tamanho configurado, e verificar com teste que texto acima do limite é rejeitado
- [ ] 4.2 Implementar função que aceita texto e um identificador de campo e produz `DocumentoOrigem(canal="extensao", identificador_origem=..., ...)`, verificando com teste que o identificador é preservado no contrato

## 5. Validação final

- [ ] 5.1 Rodar `python -m pytest` e `python -m compileall .` e registrar o resultado
- [ ] 5.2 Revisar manualmente cada cenário da spec `entrada-multicanal` confirmando que existe teste cobrindo o cenário
