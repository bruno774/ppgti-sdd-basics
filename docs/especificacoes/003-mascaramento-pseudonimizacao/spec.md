# Especificação 003 — Mascaramento por pseudo-anonimização

## Objetivo

Substituir, no texto normalizado, cada entidade detectada e selecionada pelo operador por um marcador de pseudo-anonimização estável, tipado e distinguível, preservando o sentido semântico e a estrutura do documento.

## Escopo

Incluído:

- Aplicação de marcadores no formato `prefixo + índice` conforme o [catálogo de entidades](../../requisitos/catalogo-entidades.md) (por exemplo `nom1`, `end1`, `rel1`, `rel2`).
- Seleção prévia, pelo operador, dos tipos a mascarar (ver [requisitos funcionais RF03](../../requisitos/requisitos-funcionais.md#rf03--seleção-e-parametrização-pelo-operador)).
- Reaproveitamento do mesmo índice para a mesma entidade repetida no documento.
- Aplicação de substituições sem deslocar offsets de entidades ainda não processadas.

Fora de escopo:

- Reidentificação automática do valor original a partir do texto anonimizado.
- Geração de mapa de reidentificação persistente, salvo quando explicitamente solicitado, protegido e fora da saída padrão.

## Cenários

- **Dado** um documento com duas ocorrências do nome "documento de exemplo" referentes à mesma pessoa, **quando** `NOME` é selecionado para anonimização, **então** ambas as ocorrências recebem o marcador `nom1`.
- **Dado** um documento com dois nomes diferentes, **quando** `NOME` é selecionado, **então** os marcadores `nom1` e `nom2` são atribuídos de forma consistente com a ordem de primeira aparição.
- **Dado** um documento com `NOME` e `ENDERECO` detectados, **quando** apenas `NOME` é selecionado pelo operador, **então** o endereço permanece inalterado no texto de saída.
- **Dado** duas entidades adjacentes ou parcialmente sobrepostas, **quando** ambas selecionadas, **então** o sistema aplica as substituições sem corromper ou truncar nenhuma das duas.
- **Dado** um texto acentuado com múltiplos parágrafos, **quando** mascarado, **então** acentuação, quebras de parágrafo e ordem são preservadas fora dos trechos substituídos.
- **Dado** o texto de saída gerado, **quando** inspecionado, **então** nenhum valor original das entidades selecionadas está presente, nem em comentários, nem em metadados.

## Contratos de dados

Entrada: lista de `EntidadeDetectada` (ver especificação 002) e conjunto de tipos selecionados pelo operador.

Saída (`ResultadoAnonimizacao`):

- `texto_anonimizado`: string UTF-8 final.
- `mapa_marcadores`: lista de `{ marcador, tipo }` sem o valor original, usada apenas para o relatório de contagem.
- `contagem_por_tipo`: total de entidades mascaradas por tipo canônico.

## Critérios de aceite

- Substituições aplicadas da direita para a esquerda (ou estratégia equivalente) sem deslocar posições de entidades restantes.
- Nenhuma sobreposição inválida entre marcadores no texto final.
- Testes cobrem: repetição da mesma entidade, múltiplas entidades do mesmo tipo, seleção parcial de tipos, acentuação e sobreposição.
- Nenhum teste, fixture ou snapshot contém dado pessoal real.

## Riscos e não-escopo

- A pseudo-anonimização não é reversível pela ferramenta padrão; qualquer capacidade de reidentificação exige mapa protegido e opt-in explícito, tratado fora desta especificação.
- Marcadores devem permanecer estáveis apenas dentro do escopo de um único documento processado; não há garantia de estabilidade entre documentos diferentes.
