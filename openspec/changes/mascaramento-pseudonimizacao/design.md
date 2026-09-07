## Context

Ver [proposal.md](proposal.md). As entidades detectadas (`EntidadeDetectada`, capability `deteccao-entidades`) e a seleção de categorias (`SessaoOperador`/`SelecaoCategorias`, capability `selecao-categorias`) já existem ou estão em desenvolvimento. Não existe ainda nenhuma lógica de substituição de texto no repositório.

## Goals / Non-Goals

**Goals:**
- Definir o algoritmo de substituição que preserva offsets (aplicação da direita para a esquerda) e a atribuição estável de índice por entidade única.
- Definir como identificar que duas ocorrências detectadas são "a mesma entidade" (para reaproveitar o índice) versus "entidades diferentes do mesmo tipo".

**Non-Goals:**
- Definir a lógica de detecção em si (capability `deteccao-entidades`).
- Definir a repetição de processamento sobre o texto de origem (tratada na especificação 006 / capability `selecao-categorias`, que consome esta capability).

## Decisions

- **Identidade de entidade por igualdade textual normalizada dentro do mesmo tipo.** Duas detecções do mesmo tipo com o mesmo texto (normalizado por case/espaços) são tratadas como a mesma entidade e recebem o mesmo índice; textos diferentes recebem índices incrementais na ordem de primeira aparição. Alternativa considerada: usar apenas a posição para decidir identidade — rejeitada porque a mesma pessoa citada em posições diferentes precisa do mesmo marcador (RF04.2).
- **Aplicação por reconstrução de segmentos, ordenada por posição decrescente.** O texto final é construído concatenando os segmentos entre as entidades selecionadas (do fim para o início), evitando problemas de deslocamento de índice. Alternativa considerada: usar `str.replace` sequencial — rejeitada por não preservar offsets corretamente quando o mesmo texto aparece mais de uma vez com tratamentos diferentes.
- **Detecção de sobreposição feita antes de qualquer substituição**, validando que os intervalos das entidades selecionadas não se sobrepõem parcialmente; entidades com sobreposição total (duplicata exata) são deduplicadas, e sobreposição parcial gera erro explícito em vez de corromper o texto.

## Risks / Trade-offs

- [Normalização de texto para decidir "mesma entidade" pode juntar entidades que na verdade são diferentes, ex. duas pessoas com nomes muito parecidos] → Mitigação: normalizar apenas case e espaços, não similaridade aproximada; qualquer ambiguidade fica para revisão do operador na etapa de detecção/seleção, fora desta capability.
- [Reconstrução por segmentos pode ser custosa para documentos muito grandes] → Mitigação: medir desempenho com documentos de tamanho máximo suportado (ver RNF04) antes de otimizar prematuramente.
