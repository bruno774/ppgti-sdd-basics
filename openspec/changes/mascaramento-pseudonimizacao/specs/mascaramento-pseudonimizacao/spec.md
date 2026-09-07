## Purpose

Substitui, no texto normalizado, cada entidade detectada e selecionada pelo operador por um marcador de pseudo-anonimização estável e distinguível, preservando o sentido semântico e a estrutura do documento.

## ADDED Requirements

### Requirement: Substituição por marcador prefixo+índice
O sistema SHALL substituir cada entidade selecionada pelo operador por um marcador no formato `prefixo+índice`, usando o prefixo definido no catálogo de categorias para o tipo da entidade.

#### Scenario: Duas ocorrências da mesma entidade recebem o mesmo marcador
- **WHEN** o mesmo nome de pessoa aparece duas vezes no documento e `NOME` está selecionado
- **THEN** ambas as ocorrências recebem o mesmo marcador (ex.: `nom1`)

#### Scenario: Duas entidades diferentes do mesmo tipo recebem índices diferentes
- **WHEN** dois nomes de pessoas diferentes aparecem no documento e `NOME` está selecionado
- **THEN** o sistema atribui marcadores diferentes (ex.: `nom1` e `nom2`), na ordem de primeira aparição

### Requirement: Preservação de categorias não selecionadas
O sistema SHALL manter inalteradas, no texto de saída, todas as entidades cujo tipo não foi selecionado pelo operador para anonimização.

#### Scenario: Seleção parcial preserva tipos não escolhidos
- **WHEN** um documento tem `NOME` e `ENDERECO` detectados, mas apenas `NOME` está selecionado
- **THEN** o endereço permanece no texto de saída sem qualquer alteração

### Requirement: Aplicação sem invalidar offsets
O sistema SHALL aplicar as substituições de forma que a posição de uma entidade ainda não processada nunca seja invalidada por uma substituição anterior, e SHALL impedir que uma substituição sobreponha parcialmente outra entidade selecionada.

#### Scenario: Substituições da direita para a esquerda
- **WHEN** múltiplas entidades selecionadas existem em posições diferentes do mesmo texto
- **THEN** o sistema aplica as substituições sem deslocar a posição de entidades ainda não processadas

#### Scenario: Entidades adjacentes ou parcialmente sobrepostas
- **WHEN** duas entidades selecionadas têm posições adjacentes ou parcialmente sobrepostas
- **THEN** o sistema aplica ambas as substituições sem corromper ou truncar nenhuma das duas

### Requirement: Preservação de estrutura e ausência de valor original
O sistema SHALL preservar acentuação, pontuação, parágrafos e ordem do texto fora dos trechos substituídos, e SHALL garantir que a saída anonimizada não contenha o valor original de nenhuma entidade selecionada nem um mapa de reidentificação embutido.

#### Scenario: Texto acentuado com múltiplos parágrafos
- **WHEN** um texto com acentuação e múltiplos parágrafos é mascarado
- **THEN** a saída preserva a acentuação e as quebras de parágrafo fora dos trechos substituídos

#### Scenario: Ausência de valor original na saída
- **WHEN** o texto de saída é inspecionado após a anonimização
- **THEN** nenhum valor original das entidades selecionadas está presente na saída

### Requirement: Relatório de contagem por tipo
O sistema SHALL produzir um relatório de contagem de entidades mascaradas por tipo canônico, sem incluir nenhum dado pessoal.

#### Scenario: Contagem reflete apenas os tipos selecionados
- **WHEN** a anonimização é concluída com uma seleção de categorias
- **THEN** o relatório de contagem lista apenas os tipos selecionados e a quantidade de marcadores atribuídos a cada um
