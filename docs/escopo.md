# Escopo detalhado — RF03.1 e RF04.1

Este documento aprofunda duas funcionalidades específicas dos [requisitos funcionais](requisitos/requisitos-funcionais.md), com cenários de uso e justificativa de por que são boas candidatas para serem tratadas com *Spec-Driven Development* (SDD).

## RF03.1 — Seleção, pelo operador, dos tipos de entidade a anonimizar

> "Permitir que o operador escolha, antes da anonimização, quais tipos de entidade do catálogo serão efetivamente mascarados."

### Cenários de uso

1. **Seleção parcial em documento com múltiplos tipos sensíveis.** Um operador carrega um parecer administrativo em que o detector identificou `NOME`, `CPF`, `ENDERECO` e `CID_DOENCA`. O operador seleciona apenas `NOME` e `CPF` para anonimizar, pois o endereço e a condição de saúde são relevantes para o trâmite do processo. O sistema deve mascarar somente as entidades dos tipos selecionados e manter `ENDERECO` e `CID_DOENCA` inalterados no texto de saída, sem interferir na numeração dos marcadores dos tipos escolhidos.
2. **Reuso da seleção em uma sessão com múltiplos documentos.** Um operador processa uma série de peças processuais do mesmo caso (por exemplo três PDFs anexados a um mesmo protocolo) e quer aplicar a mesma seleção de tipos (`NOME`, `CPF`, `RG`) a todos eles, sem repetir a escolha a cada documento. O sistema deve persistir a configuração de seleção durante a sessão de trabalho (RF03.4) e aplicá-la de forma consistente a cada novo documento carregado, até que o operador altere a seleção.

### Por que é adequada ao SDD

- **Regra de negócio não trivial:** a funcionalidade não é uma simples chamada de função — envolve uma decisão de negócio (o que é anonimizado depende de uma escolha humana feita *antes* da substituição, nunca de um valor fixo no código) que precisa estar descrita em um contrato verificável antes da implementação, não descoberta durante a codificação.
- **Casos de borda relevantes:** tipos detectados mas não selecionados devem permanecer intactos; tipos selecionados mas não detectados não devem gerar erro; a seleção deve ser válida mesmo quando o catálogo é estendido (RF02.3) com um tipo novo ainda não previsto no momento da implementação original. Esses casos de borda só ficam explícitos quando escritos como cenários dado/quando/então antes do código.
- **Interação entre múltiplos artefatos:** a seleção afeta simultaneamente a etapa de detecção (quais tipos aparecem para revisão), a etapa de mascaramento (RF04) e a auditoria (RF06.1, que registra os tipos selecionados). Especificar o comportamento isoladamente evita que cada camada implemente sua própria interpretação divergente do que significa "tipo selecionado".
- **Manuseio de múltiplos documentos/canais:** a persistência da seleção (cenário 2) precisa de contrato explícito sobre o que é "sessão" e como a configuração atravessa diferentes canais de entrada (PDF, DOCX, texto, extensão), o que é mais seguro de acertar com uma especificação prévia do que com implementação ad hoc.

## RF04.1 — Substituição de entidades selecionadas por marcador de pseudo-anonimização

> "Substituir cada entidade selecionada por um marcador de pseudo-anonimização no formato `prefixo + índice sequencial` (por exemplo `nom1`, `end1`, `rel1`, `rel2`), conforme o catálogo de entidades."

### Cenários de uso

1. **Mesma entidade repetida ao longo de um documento longo.** Um contrato administrativo cita o nome de uma das partes oito vezes ao longo do texto. Ao selecionar `NOME` para anonimização, todas as oito ocorrências da mesma pessoa devem receber o marcador `nom1` (não `nom1`, `nom2`, ... para a mesma entidade), enquanto o nome de uma segunda pessoa citada no documento recebe `nom2`. O sistema precisa reconhecer que se trata da mesma entidade e reaproveitar o índice já atribuído.
2. **Duas entidades sensíveis do mesmo tipo, mas diferentes entre si.** Um laudo cita duas religiões diferentes das partes envolvidas. Ao selecionar `RELIGIAO`, o sistema deve atribuir marcadores distintos (`rel1` para a primeira citada, `rel2` para a segunda), preservando a distinção entre elas — nunca reduzindo ambas a um único marcador genérico, o que apagaria informação semanticamente relevante para quem processa o texto depois.

### Por que é adequada ao SDD

- **Regra de negócio com estado compartilhado:** atribuir índice sequencial por tipo exige manter contagem e reconhecimento de identidade da entidade *ao longo de todo o documento*, não apenas em uma substituição isolada; esse comportamento de manutenção de estado é fácil de implementar de forma inconsistente sem uma especificação prévia que descreva claramente quando um índice é reaproveitado (mesma entidade) e quando é incrementado (entidade nova do mesmo tipo).
- **Casos de borda de posição/texto:** entidades adjacentes ou parcialmente sobrepostas, acentuação, quebras de parágrafo e a exigência de aplicar substituições da direita para a esquerda (RF04.3) para não invalidar offsets são condições que só se tornam visíveis quando descritas como cenários explícitos — um desenvolvedor que só olhar o "caso feliz" facilmente introduz bugs de deslocamento de posição.
- **Múltiplas entidades e múltiplos tipos interagindo no mesmo texto:** a funcionalidade não mascara um valor isolado, mas um conjunto de entidades de tipos e instâncias diferentes que competem pelo mesmo espaço de texto (RF04.4 — impedir sobreposição parcial); isso exige um contrato de dados explícito (lista ordenada de entidades, regras de prioridade em caso de conflito) melhor definido antes da implementação do que descoberto por tentativa e erro.
- **Garantia de não vazamento, verificável por teste:** o requisito de que o valor original nunca apareça na saída (RF04.6) é uma condição de segurança que deve ser validada por critérios de aceite explícitos e testes automatizados dedicados, típicos de uma especificação SDD, e não apenas por revisão informal de código.
