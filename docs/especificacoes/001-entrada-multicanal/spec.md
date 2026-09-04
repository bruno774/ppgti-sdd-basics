# Especificação 001 — Entrada multicanal de documentos

## Objetivo

Permitir que o operador submeta conteúdo para anonimização por quatro canais distintos — PDF, DOCX, texto colado/clipboard e extensão de navegador — produzindo, em todos os casos, um texto normalizado e sua origem, prontos para a etapa de detecção de entidades.

## Escopo

Incluído:

- Extração de texto de PDF pesquisável (sem camada de imagem apenas).
- Extração de texto de DOCX (parágrafos, quebras de linha e estrutura textual relevante).
- Recebimento de texto colado diretamente em campo de entrada ou via clipboard.
- Recebimento de texto capturado por uma extensão de navegador a partir de uma caixa de texto de página web.
- Validação de formato, tamanho, integridade e proteção por senha antes da extração.

Fora de escopo:

- OCR de PDFs digitalizados (capacidade separada, não habilitada por padrão).
- Extração de imagens, planilhas ou outros formatos de documento.
- Interpretação de tabelas complexas ou formatação rica além do texto e da estrutura de parágrafos.

## Cenários

- **Dado** um PDF pesquisável válido, **quando** submetido para extração, **então** o sistema retorna o texto extraído, preservando parágrafos e ordem, junto com a origem `pdf`.
- **Dado** um PDF sem camada de texto, **quando** submetido, **então** o sistema retorna um erro acionável informando a ausência de texto extraível, sem tentar OCR implicitamente.
- **Dado** um DOCX válido, **quando** submetido, **então** o sistema retorna o texto extraído com parágrafos preservados e origem `docx`.
- **Dado** um arquivo protegido por senha sem credencial informada, **quando** submetido, **então** o sistema retorna erro acionável sem expor detalhes internos de parsing.
- **Dado** um texto colado pelo operador, **quando** enviado ao sistema, **então** o texto é aceito como está, com origem `texto`, respeitando o limite de tamanho configurado.
- **Dado** um texto capturado pela extensão de navegador, **quando** enviado, **então** o sistema recebe o texto com origem `extensao` e um identificador do campo de origem, sem exigir upload de arquivo.
- **Dado** um arquivo com extensão não suportada ou corrompido, **quando** submetido, **então** o sistema recusa a entrada com mensagem de erro clara, sem processar parcialmente o conteúdo.

## Contratos de dados

Entrada normalizada (`DocumentoOrigem`):

- `canal`: um de `pdf`, `docx`, `texto`, `extensao`.
- `texto`: conteúdo textual extraído, UTF-8.
- `identificador_origem`: identificador opcional (nome do arquivo, id do campo capturado), sem dado pessoal.
- `tamanho_bytes`: tamanho do conteúdo original, usado para validação de limite.

## Critérios de aceite

- Os quatro canais produzem o mesmo contrato de saída (`DocumentoOrigem`), permitindo que a etapa de detecção seja agnóstica ao canal.
- Erros de extração são acionáveis e não incluem trechos do conteúdo original.
- Limites de tamanho e formatos suportados são configuráveis e documentados.
- Testes cobrem PDF válido, PDF sem texto, PDF protegido, DOCX válido, DOCX corrompido, texto colado e texto via extensão.

## Riscos e não-escopo

- Parsing de PDF/DOCX malformados pode expor vulnerabilidades de bibliotecas de terceiros; exigir atualização e testes de robustez.
- A extensão de navegador depende de permissões concedidas pelo operador no navegador; falhas de permissão devem gerar mensagem clara, não falha silenciosa.
