# Requisitos funcionais

## RF01 — Entrada de documentos

- RF01.1: Aceitar arquivo PDF pesquisável como entrada.
- RF01.2: Aceitar arquivo DOCX como entrada.
- RF01.3: Aceitar texto colado diretamente em um campo de entrada (texto ou clipboard).
- RF01.4: Aceitar texto capturado por uma extensão de navegador a partir de uma caixa de texto de uma página web, mediante ação explícita do operador na página.
- RF01.5: Informar de forma clara quando um PDF não possuir camada de texto utilizável; OCR é capacidade separada, fora do escopo padrão, e só pode ser habilitada por configuração explícita.
- RF01.6: Rejeitar, com erro acionável, arquivos com formato inválido, corrompido, protegido por senha sem credencial informada, ou que excedam o limite de tamanho configurado.

## RF02 — Detecção de entidades

- RF02.1: Identificar, no mínimo, as entidades do [catálogo de entidades](catalogo-entidades.md): `NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE` e `CLASSE_SOCIAL`.
- RF02.2: Para cada detecção, produzir tipo canônico, intervalo de caracteres `[início, fim)`, texto correspondente, confiança e origem (regra, modelo ou combinação).
- RF02.3: Permitir extensão do catálogo de entidades sem alterar o fluxo principal de extração, revisão ou mascaramento.
- RF02.4: Aplicar limiar de confiança mais rigoroso a tipos sensíveis (saúde, crença, gênero, cor/raça, classe social) e sinalizar essas detecções para revisão obrigatória do operador.
- RF02.5: Ser determinístico para a mesma entrada, configuração e versão do modelo/regras.

## RF03 — Seleção e parametrização pelo operador

- RF03.1: Permitir que o operador escolha, antes da anonimização, quais tipos de entidade do catálogo serão efetivamente mascarados.
- RF03.2: Permitir que o operador aprove, rejeite ou ajuste individualmente uma detecção antes da aplicação do mascaramento, especialmente para tipos sensíveis ou de baixa confiança.
- RF03.3: Preservar no texto de saída, sem alteração, qualquer entidade cujo tipo não tenha sido selecionado pelo operador ou cuja detecção tenha sido rejeitada.
- RF03.4: Persistir a configuração de seleção de tipos escolhida pelo operador para reuso em uma mesma sessão de trabalho.

## RF04 — Mascaramento por pseudo-anonimização

- RF04.1: Substituir cada entidade selecionada por um marcador de pseudo-anonimização no formato `prefixo + índice sequencial` (por exemplo `nom1`, `end1`, `rel1`, `rel2`), conforme o [catálogo de entidades](catalogo-entidades.md).
- RF04.2: Garantir que entidades diferentes do mesmo tipo recebam índices diferentes e que a mesma entidade, quando repetida no documento, reutilize o mesmo índice.
- RF04.3: Aplicar as substituições da direita para a esquerda, ou estratégia equivalente, evitando deslocamento de posições após cada substituição.
- RF04.4: Impedir que uma substituição sobreponha parcialmente outra entidade selecionada, preservando a integridade de ambas.
- RF04.5: Preservar acentuação, pontuação, estrutura de parágrafos e ordem original do texto sempre que possível.
- RF04.6: Não incluir, na saída anonimizada, o valor original das entidades mascaradas nem um mapa de reidentificação embutido.

## RF05 — Saída

- RF05.1: Produzir como resultado primário um texto UTF-8 pronto para processamento por ferramentas externas.
- RF05.2: Gerar relatório de contagem de entidades por tipo, sem incluir valores pessoais.
- RF05.3: Permitir copiar o texto anonimizado de volta para a caixa de texto de origem quando o fluxo de entrada tiver sido a extensão de navegador.

## RF06 — Auditoria

- RF06.1: Registrar cada operação de detecção, seleção e anonimização em um log de auditoria, contendo identificador da operação, data/hora, identificador do operador, canal de entrada (PDF, DOCX, texto, extensão), tipos selecionados e contagem de entidades por tipo.
- RF06.2: Não registrar, em nenhuma hipótese, o valor original das entidades, o texto bruto do documento ou qualquer conteúdo que permita reidentificação, nos registros de auditoria.
- RF06.3: Permitir consulta ao histórico de operações de auditoria por período, operador ou canal de entrada.
- RF06.4: Garantir que os registros de auditoria sejam íntegros e não editáveis por meio da interface padrão da aplicação.

## RF07 — Validação do resultado

- RF07.1: Verificar se o texto de saída é UTF-8 legível e se os marcadores seguem o esquema definido no catálogo de entidades.
- RF07.2: Verificar ausência de sobreposição inválida entre marcadores.
- RF07.3: Sinalizar quando uma entidade de tipo selecionado para anonimização permanecer exposta de forma evidente no texto de saída.

## RF08 — Extensão de navegador

- RF08.1: Capturar o conteúdo de uma caixa de texto identificada pelo operador em uma página web, mediante ação explícita (por exemplo, clique em um botão da extensão).
- RF08.2: Enviar o conteúdo capturado ao componente de detecção/anonimização sem persistência não autorizada em servidores de terceiros.
- RF08.3: Exibir ao operador as entidades detectadas e permitir a seleção de tipos antes de aplicar a anonimização, respeitando os mesmos requisitos de RF03.
- RF08.4: Permitir a devolução do texto anonimizado para a mesma caixa de texto de origem, substituindo ou complementando o conteúdo, conforme escolha do operador.
