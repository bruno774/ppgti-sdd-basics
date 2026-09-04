# Anonimizador de textos jurídicos e administrativos

## Visão geral

Projeto em desenvolvimento para identificar e anonimizar, de forma controlada, dados pessoais e dados pessoais sensíveis em documentos jurídicos e administrativos. A entrada pode chegar por quatro canais: arquivo PDF pesquisável, arquivo DOCX, texto colado diretamente (campo de entrada ou clipboard) ou captura feita por uma extensão de navegador a partir de uma caixa de texto de uma página web.

O fluxo previsto separa detecção, revisão do operador, aplicação do mascaramento e auditoria. O operador escolhe quais tipos serão anonimizados, e cada ocorrência selecionada recebe um marcador de pseudo-anonimização próprio, preservando a distinção entre entidades e o sentido semântico do documento. A saída será texto UTF-8 pronto para processamento em ferramentas externas, e cada operação relevante fica registrada em auditoria íntegra e sem dados pessoais.

> **Status:** fase inicial. Atualmente, a aplicação de anonimização, a CLI e a extensão de navegador ainda não foram implementadas. Os comandos planejados abaixo são um contrato funcional, não comandos disponíveis.

## Entidades previstas

A primeira versão deverá identificar, quando houver evidências suficientes:

`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE` e `CLASSE_SOCIAL`.

O catálogo, os prefixos de marcador e as regras de sensibilidade estão em [docs/requisitos/catalogo-entidades.md](docs/requisitos/catalogo-entidades.md). Informações de saúde, religião, gênero, cor/raça e classe social exigem limiar de confiança adequado e revisão humana; não devem ser inferidas apenas por nome, estereótipo ou contexto ambíguo.

## Instalação

### Pré-requisitos

- Python 3.11 ou versão mínima definida pelo projeto;
- PowerShell, Bash ou outro terminal compatível;
- Git, caso o projeto seja obtido de um repositório remoto.

Ainda não existe um pacote instalável. A preparação atual consiste em criar um ambiente virtual e instalar as dependências registradas em [requirements.txt](requirements.txt):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Em terminais Bash, a ativação equivalente é:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Comandos principais

### Comando disponível atualmente

O único código executável no momento é o exemplo [hello.py](hello.py):

```powershell
python hello.py
```

Saída esperada:

```text
Ola! Bem-vindo ao Python.
```

### Comandos planejados

Detectar entidades em um PDF, DOCX ou texto:

```text
anonimizador detectar --entrada documento.pdf --saida entidades.json
```

Anonimizar somente os tipos escolhidos pelo operador:

```text
anonimizador anonimizar --entrada documento.docx --tipos NOME,CPF,ENDERECO --saida documento_anonimizado.txt
```

Validar o resultado anonimizado:

```text
anonimizador validar --entrada documento_anonimizado.txt
```

Consultar auditoria:

```text
anonimizador auditoria listar --desde 2026-01-01 --operador op-123
```

A aplicação deverá informar quando um PDF não possuir camada de texto utilizável. OCR será uma capacidade separada e explicitamente configurada.

## Formato da saída

Os marcadores de pseudo-anonimização devem ser ASCII, estáveis, em minúsculas e no formato `prefixo + índice` (ver [catálogo de entidades](docs/requisitos/catalogo-entidades.md)):

```text
Requerente: nom1, CPF: cpf1.
Contato: ema1, telefone tel1.
```

As substituições devem usar intervalos `[início, fim)`, preservar ordem, acentuação e parágrafos sempre que possível e não incluir o valor original nem um mapa de reidentificação na saída anonimizada.

## Estrutura do projeto

```text
.
├── docs/
│   ├── adr/                  # Registros de decisões arquiteturais
│   ├── requisitos/           # Requisitos funcionais, não funcionais, catálogo de entidades e glossário
│   └── especificacoes/       # Especificações SDD por funcionalidade
├── src/
│   ├── backend/              # Extração, detecção, mascaramento e auditoria
│   ├── frontend/              # Interface para revisão e seleção do operador
│   └── extension/             # Extensão de navegador (captura e devolução de texto)
├── tests/
│   ├── backend/               # Testes dos componentes do backend
│   ├── frontend/              # Testes da interface
│   └── extension/             # Testes da extensão de navegador
├── AGENTS.md                  # Diretrizes gerais para agentes e colaboradores
├── CLAUDE.md                  # Instruções adicionais para agentes Claude
├── README.md                  # Apresentação e uso do projeto
└── hello.py                   # Exemplo executável atual
```

As pastas de código e testes ainda estão reservadas para a implementação futura. Consulte [docs/especificacoes/README.md](docs/especificacoes/README.md) para as especificações por funcionalidade e [docs/adr/README.md](docs/adr/README.md) para registrar decisões arquiteturais.

## Privacidade e segurança

- Trate todo documento, texto colado ou conteúdo capturado por extensão como confidencial.
- Não envie documentos ou conteúdo capturado a serviços externos sem opt-in explícito e documentado.
- Não registre texto bruto, entidades originais ou conteúdo sensível em logs, erros, arquivos temporários ou registros de auditoria.
- Valide caminhos, extensões e limites de tamanho antes da leitura de PDF/DOCX.
- Remova ou proteja arquivos temporários após o processamento.
- Aplique mínimo privilégio nas permissões solicitadas pela extensão de navegador.
- Não confunda anonimização, pseudonimização e simples mascaramento.
- Não considere o resultado uma garantia de anonimização perfeita; a revisão humana continua necessária, especialmente para tipos sensíveis.

## Desenvolvimento e testes

Consulte [AGENTS.md](AGENTS.md) para as convenções gerais e [CLAUDE.md](CLAUDE.md) para instruções específicas de agentes Claude.

Validação mínima esperada para alterações futuras:

```powershell
python -m pytest
python -m compileall .
```

Os testes deverão cobrir PDF, DOCX, texto colado/clipboard e captura via extensão, cada tipo de entidade, casos negativos, acentuação, sobreposição, escolha parcial de tipos, ausência dos valores originais na saída/logs/erros, e integridade dos registros de auditoria.

## Não escopo

Este projeto não deve decidir se o conteúdo jurídico é verdadeiro, válido ou juridicamente correto, realizar classificação jurídica ou recomendar medidas legais. Também não promete OCR perfeito, não substitui revisão humana, não funciona como sistema geral de gestão documental e não recupera a identidade original a partir do texto anonimizado.

Imagens, planilhas e formatos adicionais ficam fora do escopo até que exista requisito explícito.

## Autoria

**Autor:** Bruno Silva

Informações adicionais de autoria, instituição, licença e contato serão incluídas quando forem formalmente definidas.
