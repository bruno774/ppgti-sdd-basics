## Context

Ver [proposal.md](proposal.md). Nenhuma implementação de auditoria existe hoje. As capabilities `selecao-categorias`, `deteccao-entidades` e `mascaramento-pseudonimizacao` (em desenvolvimento) serão as principais emissoras de eventos, mas o contrato de evento e o mecanismo append-only podem ser definidos e testados de forma independente.

## Goals / Non-Goals

**Goals:**
- Definir o contrato `EventoAuditoria` e um mecanismo de registro append-only testável isoladamente, com uma API de emissão simples para ser chamada pelas demais capabilities.
- Definir a validação de sanitização que impede texto livre não controlado em qualquer campo do evento.

**Non-Goals:**
- Definir o mecanismo de autenticação/autorização de quem pode consultar os registros de auditoria (depende de um sistema de perfis/autenticação ainda não definido no projeto, ver `selecao-categorias-operador/design.md`).
- Definir política de retenção/expurgo de longo prazo dos registros (fica a critério do operador/instituição, fora do escopo técnico inicial).

## Decisions

- **`EventoAuditoria` como modelo Pydantic com campos fechados** (sem campo de texto livre irrestrito): qualquer valor textual (ex.: identificador de operador) é validado contra um formato esperado (ex.: identificador opaco, não nome livre). Alternativa considerada: permitir um campo `detalhes: str` livre para flexibilidade — rejeitada por criar um vetor de vazamento de dado pessoal.
- **Armazenamento append-only implementado como uma lista/tabela sem operação de update ou delete exposta na API pública do módulo**, apenas `registrar_evento` e `consultar_eventos`. Alternativa considerada: permitir soft-delete — rejeitada porque contraria o requisito de imutabilidade pela interface padrão.
- **Sanitização de campos antes de persistir**, rejeitando eventos cujo conteúdo não corresponda ao formato esperado de cada campo (em vez de tentar "limpar" texto livre, que é uma operação frágil e sujeita a falha).

## Risks / Trade-offs

- [Validação de formato pode ser rígida demais e rejeitar eventos legítimos] → Mitigação: definir claramente os formatos esperados por campo nesta change, com testes cobrindo casos válidos e inválidos antes de integrar com as capabilities emissoras.
- [Ausência de controle de acesso à consulta nesta primeira versão] → Mitigação: documentar explicitamente essa lacuna como não-goal e não expor a consulta publicamente até que o controle de acesso exista.
