# Especificação 002 — Detecção de entidades

## Objetivo

Identificar, no texto normalizado produzido pela entrada multicanal, ocorrências de dados pessoais e sensíveis do [catálogo de entidades](../../requisitos/catalogo-entidades.md), com posição, confiança e origem, sem aplicar qualquer substituição nesta etapa.

## Escopo

Incluído:

- Detecção dos tipos: `NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`.
- Cálculo de confiança por detecção e aplicação de limiar mais rigoroso para tipos sensíveis.
- Suporte a extensão do catálogo por meio de novas regras/modelos, sem alterar o fluxo principal.

Fora de escopo:

- Decisão final sobre quais tipos serão mascarados (cabe ao operador, ver especificação 003).
- Julgamento sobre validade jurídica do conteúdo detectado.

## Cenários

- **Dado** um texto contendo um CPF em formato `000.000.000-00` ou `00000000000`, **quando** processado, **então** o sistema retorna uma detecção do tipo `CPF` com o intervalo correto.
- **Dado** um texto mencionando uma doença específica associada a uma pessoa, **quando** processado, **então** o sistema retorna uma detecção `CID_DOENCA` com confiança e, se abaixo do limiar sensível, marca a detecção para revisão obrigatória.
- **Dado** um texto que cita duas religiões diferentes, **quando** processado, **então** o sistema retorna duas detecções distintas do tipo `RELIGIAO`, permitindo posteriormente marcadores `rel1` e `rel2`.
- **Dado** um texto sem qualquer entidade sensível, **quando** processado, **então** o sistema não gera falsos positivos para os tipos sensíveis (caso de teste negativo).
- **Dado** um trecho ambíguo que apenas menciona um bairro sem renda ou profissão explícita, **quando** processado, **então** o sistema não infere `CLASSE_SOCIAL` automaticamente.
- **Dado** o mesmo texto processado duas vezes com a mesma configuração, **quando** comparado, **então** as detecções são idênticas (determinismo).

## Contratos de dados

Detecção (`EntidadeDetectada`):

- `id`: identificador estável dentro do processamento do documento.
- `tipo`: tipo canônico do [catálogo](../../requisitos/catalogo-entidades.md).
- `inicio`, `fim`: intervalo `[início, fim)` em caracteres, relativo ao texto normalizado.
- `texto`: trecho detectado (mantido apenas em memória durante o processamento, nunca persistido em log).
- `confianca`: valor numérico de 0 a 1.
- `origem`: `regra`, `modelo` ou `combinado`.
- `sensivel`: booleano indicando se o tipo exige revisão obrigatória.

## Critérios de aceite

- Todos os tipos do catálogo possuem ao menos um teste positivo, um negativo e, quando aplicável, um caso ambíguo.
- Tipos sensíveis nunca são aplicados automaticamente sem sinalização de revisão quando abaixo do limiar configurado.
- Duas entidades de tipos diferentes ou do mesmo tipo em posições diferentes nunca compartilham `id`.
- Nenhum valor detectado é gravado em log, métrica ou arquivo de diagnóstico.

## Riscos e não-escopo

- Modelos de NLP podem gerar falsos positivos/negativos; resultados de baixa confiança devem sempre ser apresentados para revisão humana, nunca aplicados silenciosamente.
- Este componente não decide se o conteúdo jurídico é verdadeiro ou correto.
