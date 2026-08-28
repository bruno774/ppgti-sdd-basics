# Anonimizador de textos jurídicos e administrativos

## Visão geral

Projeto em desenvolvimento para identificar e anonimizar, de forma controlada, dados pessoais e dados pessoais sensíveis em documentos jurídicos e administrativos nos formatos PDF e TXT.

O fluxo previsto separa detecção, revisão do operador e aplicação do mascaramento. O operador escolhe quais tipos serão anonimizados, e cada ocorrência selecionada recebe um marcador próprio, preservando a distinção entre entidades e o sentido semântico do documento. A saída será texto UTF-8 pronto para processamento em ferramentas externas.

> **Status:** fase inicial. Atualmente, a aplicação de anonimização e a CLI ainda não foram implementadas. Os comandos planejados abaixo são um contrato funcional, não comandos disponíveis.

## Entidades previstas

A primeira versão deverá identificar, quando houver evidências suficientes:

`NOME`, `CPF`, `RG`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `CLASSE_SOCIAL`, `ENDERECO`, `EMAIL` e `TELEFONE`.

O catálogo deverá ser extensível. Informações de saúde, religião, gênero e classe social exigem limiar de confiança adequado e revisão humana; não devem ser inferidas apenas por nome, estereótipo ou contexto ambíguo.

## Instalação

### Pré-requisitos

- Python 3.11 ou versão mínima definida pelo projeto;
- PowerShell, Bash ou outro terminal compatível;
- Git, caso o projeto seja obtido de um repositório remoto.

Ainda não existe um arquivo de dependências ou um pacote instalável. Portanto, a preparação atual consiste em criar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Em terminais Bash, a ativação equivalente é:

```bash
python -m venv .venv
source .venv/bin/activate
```

Quando as dependências da aplicação forem definidas, elas deverão ser registradas em um arquivo próprio, como `requirements.txt` ou `pyproject.toml`, e esta seção deverá ser atualizada.

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

Detectar entidades em um PDF ou TXT:

```text
anonimizador detectar --entrada documento.pdf --saida entidades.json
```

Anonimizar somente os tipos escolhidos pelo operador:

```text
anonimizador anonimizar --entrada documento.txt --tipos NOME,CPF,ENDERECO --saida documento_anonimizado.txt
```

Validar o resultado anonimizado:

```text
anonimizador validar --entrada documento_anonimizado.txt
```

A aplicação deverá informar quando um PDF não possuir camada de texto utilizável. OCR será uma capacidade separada e explicitamente configurada.

## Formato da saída

Os marcadores devem ser ASCII, estáveis, tipados e facilmente reconhecíveis por ferramentas externas:

```text
Requerente: [NOME_001], CPF: [CPF_001].
Contato: [EMAIL_001], telefone [TELEFONE_001].
```

As substituições devem usar intervalos `[início, fim)`, preservar ordem, acentuação e parágrafos sempre que possível e não incluir o valor original nem um mapa de reidentificação na saída anonimizada.

## Estrutura do projeto

```text
.
├── docs/
│   └── adr/                 # Registros de decisões arquiteturais
├── src/
│   ├── backend/             # Extração, detecção e anonimização
│   └── frontend/            # Interface para revisão e seleção do operador
├── tests/
│   ├── backend/             # Testes dos componentes do backend
│   └── frontend/            # Testes da interface
├── AGENTS.md                # Diretrizes gerais para agentes e colaboradores
├── CLAUDE.md                # Instruções adicionais para agentes Claude
├── README.md                # Apresentação e uso do projeto
└── hello.py                 # Exemplo executável atual
```

As pastas de código e testes ainda estão reservadas para a implementação futura. Consulte [docs/adr/README.md](docs/adr/README.md) para registrar decisões arquiteturais.

## Privacidade e segurança

- Trate todo documento de entrada como confidencial.
- Não envie documentos a serviços externos sem autorização explícita e documentada.
- Não registre texto bruto, entidades originais ou conteúdo sensível em logs, erros e arquivos temporários.
- Valide caminhos, extensões e limites de tamanho antes da leitura.
- Remova ou proteja arquivos temporários após o processamento.
- Não confunda anonimização, pseudonimização e simples mascaramento.
- Não considere o resultado uma garantia de anonimização perfeita; a revisão humana continua necessária.

## Desenvolvimento e testes

Consulte [AGENTS.md](AGENTS.md) para as convenções gerais e [CLAUDE.md](CLAUDE.md) para instruções específicas de agentes Claude.

Validação mínima esperada para alterações futuras:

```powershell
python -m pytest
python -m compileall .
```

Os testes deverão cobrir PDFs e TXTs, cada tipo de entidade, casos negativos, acentuação, sobreposição, escolha parcial de tipos e ausência dos valores originais na saída, nos logs e nos erros.

## Não escopo

Este projeto não deve decidir se o conteúdo jurídico é verdadeiro, válido ou juridicamente correto, realizar classificação jurídica ou recomendar medidas legais. Também não promete OCR perfeito, não substitui revisão humana, não funciona como sistema geral de gestão documental e não recupera a identidade original a partir do texto anonimizado.

Imagens, planilhas e formatos adicionais ficam fora do escopo até que exista requisito explícito.

## Autoria

**Autor:** Bruno Silva

Informações adicionais de autoria, instituição, licença e contato serão incluídas quando forem formalmente definidas.
