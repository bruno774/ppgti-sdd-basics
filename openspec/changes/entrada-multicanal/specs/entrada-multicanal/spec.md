## Purpose

Aceita conteúdo de quatro canais de entrada (PDF, DOCX, texto colado/clipboard e extensão de navegador) e produz um contrato normalizado de texto de origem, comum a todos os canais, para as etapas seguintes de detecção e mascaramento.

## ADDED Requirements

### Requirement: Extração de texto de PDF pesquisável
O sistema SHALL extrair o texto de um PDF pesquisável válido, preservando parágrafos e ordem, e SHALL rejeitar PDFs sem camada de texto utilizável sem tentar OCR implicitamente.

#### Scenario: PDF pesquisável válido
- **WHEN** um PDF pesquisável válido é submetido para extração
- **THEN** o sistema retorna o texto extraído com origem `pdf`, preservando parágrafos e ordem

#### Scenario: PDF sem camada de texto
- **WHEN** um PDF sem camada de texto utilizável é submetido
- **THEN** o sistema retorna um erro acionável informando a ausência de texto extraível, sem executar OCR

#### Scenario: PDF protegido por senha
- **WHEN** um PDF protegido por senha é submetido sem credencial
- **THEN** o sistema retorna um erro acionável, sem expor detalhes internos de parsing

### Requirement: Validacao de formato e conteudo potencialmente injetado
O sistema SHALL validar a assinatura de arquivos PDF existentes antes da extração e SHALL interromper o processamento quando o texto extraído contiver padrões de instruções potencialmente injetadas, emitindo apenas um alerta sem reproduzir o conteúdo detectado.

#### Scenario: Arquivo com formato incompatível
- **WHEN** um arquivo com extensão `.pdf` não possuir a assinatura PDF esperada
- **THEN** o sistema rejeita a entrada antes da extração e informa que o formato não é compatível

#### Scenario: Conteúdo com prompt injection
- **WHEN** o texto extraído contiver uma instrução potencialmente injetada
- **THEN** o sistema alerta o operador, interrompe o processamento e não reproduz o trecho detectado na mensagem de erro

### Requirement: Extração de texto de DOCX
O sistema SHALL extrair o texto de um DOCX válido, preservando parágrafos, e SHALL rejeitar arquivos DOCX corrompidos ou protegidos com um erro acionável.

#### Scenario: DOCX válido
- **WHEN** um DOCX válido é submetido para extração
- **THEN** o sistema retorna o texto extraído com parágrafos preservados e origem `docx`

#### Scenario: DOCX corrompido ou protegido
- **WHEN** um DOCX corrompido, ou protegido por senha sem credencial, é submetido
- **THEN** o sistema retorna um erro acionável, sem processar parcialmente o conteúdo

### Requirement: Entrada de texto colado ou capturado por extensão
O sistema SHALL aceitar texto colado diretamente (campo de entrada ou clipboard) e texto capturado por uma extensão de navegador, respeitando o limite de tamanho configurado.

#### Scenario: Texto colado pelo operador
- **WHEN** o operador cola texto em um campo de entrada
- **THEN** o sistema aceita o conteúdo com origem `texto`, respeitando o limite de tamanho configurado

#### Scenario: Texto capturado pela extensão de navegador
- **WHEN** uma extensão de navegador envia texto capturado de um campo de página
- **THEN** o sistema aceita o conteúdo com origem `extensao` e um identificador do campo de origem, sem exigir upload de arquivo

### Requirement: Rejeição de entradas inválidas
O sistema SHALL rejeitar, com erro acionável e sem processamento parcial, qualquer arquivo com formato não suportado, extensão inválida ou tamanho acima do limite configurado.

#### Scenario: Formato ou extensão não suportada
- **WHEN** um arquivo com extensão não suportada ou corrompida é submetido
- **THEN** o sistema recusa a entrada com mensagem de erro clara, sem processar parcialmente o conteúdo

#### Scenario: Tamanho acima do limite
- **WHEN** um arquivo ou texto excede o limite de tamanho configurado
- **THEN** o sistema rejeita a entrada com um erro acionável antes de iniciar a extração

### Requirement: Contrato normalizado de origem
O sistema SHALL produzir, para qualquer um dos quatro canais, um contrato normalizado (`DocumentoOrigem`) com canal, texto extraído, identificador de origem opcional e tamanho em bytes, permitindo que a etapa de detecção seja agnóstica ao canal.

#### Scenario: Mesmo contrato para os quatro canais
- **WHEN** conteúdo é aceito por qualquer um dos quatro canais (PDF, DOCX, texto, extensão)
- **THEN** o sistema produz um `DocumentoOrigem` com o mesmo formato de campos, variando apenas o valor do canal e da origem
