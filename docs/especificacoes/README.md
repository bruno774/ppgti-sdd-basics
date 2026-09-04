# Especificações (SDD)

Esta pasta contém as especificações do projeto seguindo uma abordagem de *Spec-Driven Development* (SDD): cada funcionalidade relevante é descrita antes da implementação, em um documento único e verificável, que orienta tanto pessoas quanto agentes de IA.

Cada especificação segue a estrutura:

1. **Objetivo** — o que a funcionalidade entrega e por quê.
2. **Escopo** — o que está e o que não está incluído.
3. **Cenários (dado/quando/então)** — comportamento esperado, incluindo casos negativos.
4. **Contratos de dados** — modelos de entrada/saída relevantes.
5. **Critérios de aceite** — condições verificáveis para considerar a funcionalidade pronta.
6. **Riscos e não-escopo** — limites explícitos e riscos conhecidos.

## Índice

- [001 — Entrada multicanal de documentos](001-entrada-multicanal/spec.md)
- [002 — Detecção de entidades](002-deteccao-entidades/spec.md)
- [003 — Mascaramento por pseudo-anonimização](003-mascaramento-pseudonimizacao/spec.md)
- [004 — Extensão de navegador](004-extensao-navegador/spec.md)
- [005 — Auditoria de operações](005-auditoria/spec.md)
- [006 — Ajuste de categorias de dados pelo operador antes do processamento](006-selecao-categorias-operador/spec.md)

Consulte também [../requisitos/](../requisitos/) para os requisitos funcionais e não funcionais consolidados, e [../adr/](../adr/) para decisões arquiteturais.

Toda especificação nova ou alterada deve ser revisada quanto a: vazamento de dados originais, cobertura de tipos sensíveis, determinismo e rastreabilidade por auditoria, antes de ser aprovada para implementação.
