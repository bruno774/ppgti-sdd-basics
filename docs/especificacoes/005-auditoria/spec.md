# Especificação 005 — Auditoria de operações

## Objetivo

Registrar de forma íntegra e não editável cada operação relevante realizada pelo sistema (detecção, seleção de tipos, aplicação de mascaramento e exportação), permitindo rastreabilidade sem expor dados pessoais.

## Escopo

Incluído:

- Registro de eventos de auditoria para: início de processamento, detecção concluída, seleção de tipos confirmada pelo operador, aplicação de mascaramento e exportação do resultado.
- Consulta ao histórico de auditoria por período, operador ou canal de entrada.
- Garantia de imutabilidade dos registros já gravados através da interface padrão da aplicação.

Fora de escopo:

- Armazenamento de texto original, entidades detectadas em valor bruto, ou qualquer conteúdo que permita reidentificação.
- Auditoria de conteúdo jurídico ou de mérito do documento (não é objetivo desta ferramenta avaliar validade jurídica).

## Cenários

- **Dado** um processamento de documento concluído, **quando** a anonimização é aplicada, **então** um registro de auditoria é criado com data/hora, operador, canal de entrada, tipos selecionados e contagem por tipo.
- **Dado** um registro de auditoria já gravado, **quando** qualquer usuário tenta alterá-lo pela interface padrão, **então** a operação é recusada.
- **Dado** um conjunto de registros de auditoria, **quando** consultado por período ou operador, **então** o sistema retorna apenas os campos definidos no contrato, sem dado pessoal.
- **Dado** uma tentativa de gravar um evento de auditoria contendo um trecho do texto original por engano, **quando** validado, **então** o sistema rejeita ou sanitiza o campo antes de persistir (validação de contrato).

## Contratos de dados

Registro de auditoria (`EventoAuditoria`):

- `id`: identificador único do evento.
- `timestamp`: data/hora UTC do evento.
- `operador_id`: identificador do operador autenticado (nunca nome livre não controlado).
- `canal_entrada`: um de `pdf`, `docx`, `texto`, `extensao`.
- `acao`: um de `deteccao`, `selecao`, `anonimizacao`, `exportacao`.
- `tipos_selecionados`: lista de tipos canônicos do catálogo.
- `contagem_por_tipo`: mapa tipo → quantidade.
- `documento_hash`: hash não reversível do documento de origem, usado apenas para correlacionar eventos do mesmo processamento, nunca para reidentificação.

## Critérios de aceite

- Nenhum campo do contrato `EventoAuditoria` permite reconstrução do texto original.
- Testes de segurança confirmam que, para qualquer operação, o log resultante não contém o valor de nenhuma entidade detectada.
- Consulta de auditoria funciona por período, operador e canal, com paginação para históricos longos.
- Registros são append-only: não existe endpoint ou ação de interface padrão para edição ou exclusão de um evento já gravado.

## Riscos e não-escopo

- Uma auditoria completa exige também proteção de acesso (quem pode consultar registros); controle de acesso a essa consulta deve seguir o mesmo modelo de autenticação da aplicação principal.
- Retenção e expurgo de registros de auditoria devem seguir política definida pelo operador/instituição, fora do escopo técnico desta especificação inicial.
