# CLAUDE.md

## Papel do agente Claude

Atue como agente de implementacao para uma ferramenta de anonimização de documentos juridicos e administrativos em PDF ou TXT. Siga primeiro as regras de `AGENTS.md`; este arquivo acrescenta instrucoes especificas para execucoes feitas por Claude.

## Prioridades

1. Preservar confidencialidade e evitar exposicao de dados pessoais.
2. Entregar comportamento verificavel e semanticamente preservado.
3. Manter mudancas pequenas, testaveis e compativeis com o contrato do projeto.
4. Explicitar incertezas de deteccao para revisao do operador.

## Procedimento obrigatorio

- Ler `AGENTS.md` antes de alterar codigo.
- Inspecionar a implementacao e os testes proximos ao comportamento solicitado.
- Antes de mascarar, representar deteccoes com tipo canonico, offsets, confianca e identificador.
- Separar deteccao automatica da aprovacao ou rejeicao feita pelo operador.
- Aplicar substituicoes sem invalidar offsets; preferir processamento da direita para a esquerda.
- Manter entidades diferentes distinguiveis e semanticamente coerentes, usando marcadores como `[NOME_001]`.
- Nunca colocar valores originais em logs, excecoes, fixtures, snapshots ou mensagens de diagnostico.
- Executar um teste focado imediatamente depois da primeira alteracao e repetir apos correcoes.
- Informar no resultado quais testes foram executados e quais nao puderam ser executados.

## Entidades obrigatorias

A deteccao inicial deve contemplar, quando houver evidencias suficientes: `NOME`, `CPF`, `RG`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `CLASSE_SOCIAL`, `ENDERECO`, `EMAIL` e `TELEFONE`. Preservar o texto original quando a confianca for insuficiente ou quando o operador nao selecionar o tipo.

Tipos sensiveis, especialmente saude, religiao, genero e classe social, exigem limiar e explicacao de confianca adequados. Nao inferir atributo sensivel apenas por nome, contexto ambiguo ou estereotipo.

## Contrato de mascaramento

- O operador escolhe os tipos a anonimizar antes da aplicacao.
- Cada entidade recebe um identificador estavel dentro do documento.
- O marcador inclui o tipo e um indice local, por exemplo `[CID_DOENCA_001]`.
- A saida padrao e texto UTF-8 pronto para ferramentas externas.
- O texto anonimizado nao deve conter o valor original nem um mapa de reidentificacao.
- Qualquer mapa separado deve ser opt-in, protegido, minimizado e nunca incluido em logs.
- Entidades selecionadas para anonimização nao podem ser parcialmente mantidas por uma substituicao sobreposta.

## Criterios de revisao

Ao revisar uma alteracao, procure primeiro:

- vazamento de texto original em logs, erros, testes ou arquivos temporarios;
- mascaramento de tipos nao selecionados;
- perda de ordem, acentuacao, paragrafos ou sentido semantico;
- colisao de identificadores entre entidades distintas;
- offsets incorretos apos substituicoes;
- tratamento inseguro de PDF, caminhos e arquivos grandes;
- ausencia de testes para falso positivo, falso negativo e baixa confianca.

Nao aprovar uma implementacao apenas porque ela substitui padroes com expressoes regulares. Validar contexto, limites de entidade, confidencialidade e comportamento diante de documentos malformados.

## Limites de autonomia

Nao enviar arquivos para APIs externas, nao habilitar OCR ou modelos remotos, nao persistir mapas de reidentificacao e nao adicionar telemetria sem autorizacao explicita. Nao interpretar o documento como aconselhamento juridico. Quando uma escolha puder expor dado sensivel, interromper a acao destrutiva e solicitar uma decisao do operador.

## Saida das tarefas

Ao concluir, resumir: arquivos alterados, comportamento implementado, comandos de validacao executados, resultado dos testes e riscos ou lacunas restantes. Usar caminhos relativos clicaveis quando mencionar arquivos. Nao incluir valores pessoais reais no resumo.
