## Context

Ver [proposal.md](proposal.md). O catálogo de tipos já existe em `src/backend/categorias.py` (capability `selecao-categorias`), incluindo o sinalizador `sensivel` por tipo. A entrada normalizada (`DocumentoOrigem`) vem da capability `entrada-multicanal`. Não existe ainda nenhuma lógica de detecção (regras ou NLP) no repositório.

## Goals / Non-Goals

**Goals:**
- Definir uma estratégia de detecção por tipo que combine regras determinísticas (para tipos com formato regular, como `CPF`, `EMAIL`, `TELEFONE`) e heurísticas/NLP (para tipos que exigem contexto, como `NOME`, `ENDERECO`, tipos sensíveis).
- Garantir que o limiar de confiança e a sinalização de revisão para tipos sensíveis sejam aplicados de forma central, não espalhados por múltiplas implementações de regra.

**Non-Goals:**
- Escolher ou treinar um modelo de NLP específico (fica para uma decisão de implementação dentro das tarefas, respeitando os critérios de determinismo e ausência de inferência por estereótipo da spec).
- Implementar a interface de revisão do operador (capability separada, fora desta change).

## Decisions

- **Detectores organizados por tipo, com uma interface comum** (`detectar(texto) -> list[EntidadeDetectada]`), permitindo adicionar um novo tipo sem alterar o orquestrador principal. Alternativa considerada: um único detector monolítico para todos os tipos — rejeitada por dificultar extensão (RF02.3) e testes isolados por tipo.
- **Tipos com formato regular (`CPF`, `EMAIL`, `TELEFONE`, `RG`) usam expressões regulares determinísticas**, com confiança fixa alta (ex.: 0.95) quando o formato casa exatamente. Alternativa considerada: usar NLP para todos os tipos — rejeitada por adicionar não-determinismo e custo computacional desnecessário para tipos com formato bem definido.
- **Tipos sensíveis sempre retornam `sensivel = true`** no contrato de detecção, independentemente do valor numérico de confiança, e o orquestrador central impede que qualquer chamador trate uma detecção sensível como "aplicável automaticamente". Alternativa considerada: deixar a checagem de sensibilidade a cargo de quem consome a detecção — rejeitada por criar risco de um consumidor futuro esquecer a checagem.
- **Confiança como valor de 0 a 1, sem escala oculta por biblioteca.** Cada detector deve normalizar sua própria saída para esse intervalo antes de retornar `EntidadeDetectada`.

## Risks / Trade-offs

- [Detecção de `NOME` e `ENDERECO` por heurística/NLP pode gerar falsos positivos/negativos] → Mitigação: manter confiança visível no contrato e nunca aplicar automaticamente sem seleção explícita do operador (capability `selecao-categorias`) e, quando sensível, sem revisão.
- [Adicionar spaCy como dependência aumenta o tempo de carregamento/memória] → Mitigação: carregar o modelo de NLP de forma preguiçosa (lazy) e documentar o custo esperado; medir antes de tornar obrigatório para todos os tipos.
- [Regras de formato podem colidir com falsos positivos de outros tipos (ex.: número de telefone parecido com trecho de CPF)] → Mitigação: ordem de prioridade entre detectores e testes de sobreposição dedicados.
