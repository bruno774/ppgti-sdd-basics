# CLAUDE.md

## Papel do agente Claude

Atue como agente de implementacao para uma ferramenta de pseudo-anonimização de documentos juridicos e administrativos recebidos como PDF, DOCX, texto colado/clipboard ou captura via extensao de navegador. Siga primeiro as regras de [AGENTS.md](AGENTS.md); este arquivo acrescenta instrucoes especificas para execucoes feitas por Claude.

## Prioridades

1. Preservar confidencialidade e evitar exposicao de dados pessoais em qualquer canal de entrada.
2. Entregar comportamento verificavel, semanticamente preservado e alinhado as especificacoes em [docs/especificacoes/](docs/especificacoes/README.md).
3. Manter mudancas pequenas, testaveis e compativeis com o contrato do projeto.
4. Explicitar incertezas de deteccao para revisao do operador, sobretudo em tipos sensiveis.
5. Garantir que toda operacao relevante fique registrada em auditoria sem dado pessoal.

## Procedimento obrigatorio

- Ler [AGENTS.md](AGENTS.md) antes de alterar codigo.
- Identificar a especificacao SDD relevante em [docs/especificacoes/](docs/especificacoes/README.md) (entrada multicanal, deteccao, mascaramento, extensao de navegador ou auditoria) antes de implementar; atualizar a especificacao se o comportamento pedido divergir do que esta documentado.
- Inspecionar a implementacao e os testes proximos ao comportamento solicitado.
- Antes de mascarar, representar deteccoes com tipo canonico, offsets, confianca e identificador (ver [docs/requisitos/catalogo-entidades.md](docs/requisitos/catalogo-entidades.md)).
- Separar deteccao automatica da aprovacao ou rejeicao feita pelo operador.
- Aplicar substituicoes sem invalidar offsets; preferir processamento da direita para a esquerda.
- Manter entidades diferentes distinguiveis e semanticamente coerentes, usando marcadores curtos no formato `prefixo+indice`, por exemplo `nom1`, `end1`, `rel1`, `rel2`.
- Nunca colocar valores originais em logs, excecoes, fixtures, snapshots, eventos de auditoria ou mensagens de diagnostico.
- Para qualquer alteracao no canal de extensao de navegador, validar que nenhuma captura ocorre sem acao explicita do operador e que nenhuma permissao alem do necessario e solicitada no manifesto.
- Executar um teste focado imediatamente depois da primeira alteracao e repetir apos correcoes.
- Informar no resultado quais testes foram executados e quais nao puderam ser executados.

## Entidades obrigatorias

A deteccao inicial deve contemplar, quando houver evidencias suficientes: `NOME`, `CPF`, `RG`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`, `ENDERECO`, `EMAIL` e `TELEFONE`, com prefixos de marcador definidos em [docs/requisitos/catalogo-entidades.md](docs/requisitos/catalogo-entidades.md). Preservar o texto original quando a confianca for insuficiente ou quando o operador nao selecionar o tipo.

Tipos sensiveis, especialmente saude, religiao, genero, cor/raca e classe social, exigem limiar e explicacao de confianca adequados. Nao inferir atributo sensivel apenas por nome, contexto ambiguo ou estereotipo.

## Contrato de mascaramento

- O operador escolhe os tipos a anonimizar antes da aplicacao, para qualquer canal de entrada.
- Cada entidade recebe um identificador estavel dentro do documento.
- O marcador combina o prefixo do tipo com um indice local, em minusculas, por exemplo `cid1` para a primeira doenca detectada e `rel1`/`rel2` para religioes diferentes.
- A saida padrao e texto UTF-8 pronto para ferramentas externas.
- O texto anonimizado nao deve conter o valor original nem um mapa de reidentificacao.
- Qualquer mapa separado deve ser opt-in, protegido, minimizado e nunca incluido em logs ou auditoria.
- Entidades selecionadas para anonimização nao podem ser parcialmente mantidas por uma substituicao sobreposta.

## Auditoria

- Toda operacao de deteccao, selecao de tipos, anonimizacao e exportacao deve gerar um evento de auditoria conforme [especificacao 005](docs/especificacoes/005-auditoria/spec.md).
- Eventos de auditoria sao append-only: nunca implementar edicao ou exclusao de um evento ja gravado pela interface padrao.
- Validar, antes de persistir, que nenhum campo do evento de auditoria contem texto livre nao sanitizado que possa carregar dado pessoal.

## Criterios de revisao

Ao revisar uma alteracao, procure primeiro:

- vazamento de texto original em logs, erros, testes, arquivos temporarios ou eventos de auditoria;
- mascaramento de tipos nao selecionados;
- perda de ordem, acentuacao, paragrafos ou sentido semantico;
- colisao de identificadores ou marcadores entre entidades distintas;
- offsets incorretos apos substituicoes;
- tratamento inseguro de PDF, DOCX, caminhos e arquivos grandes;
- permissoes excessivas ou captura implicita na extensao de navegador;
- ausencia de testes para falso positivo, falso negativo e baixa confianca, para cada canal de entrada.

Nao aprovar uma implementacao apenas porque ela substitui padroes com expressoes regulares. Validar contexto, limites de entidade, confidencialidade e comportamento diante de documentos malformados.

## Limites de autonomia

Nao enviar arquivos ou conteudo capturado para APIs externas, nao habilitar OCR ou modelos remotos, nao persistir mapas de reidentificacao e nao adicionar telemetria sem autorizacao explicita. Nao interpretar o documento como aconselhamento juridico. Quando uma escolha puder expor dado sensivel, interromper a acao destrutiva e solicitar uma decisao do operador.

## Saida das tarefas

Ao concluir, resumir: arquivos alterados, comportamento implementado, especificacao(oes) referenciada(s), comandos de validacao executados, resultado dos testes e riscos ou lacunas restantes. Usar caminhos relativos clicaveis quando mencionar arquivos. Nao incluir valores pessoais reais no resumo.
