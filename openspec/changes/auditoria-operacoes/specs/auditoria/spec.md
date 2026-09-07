## Purpose

Registra de forma íntegra e não editável cada operação relevante do sistema (detecção, seleção de tipos, anonimização, exportação), permitindo rastreabilidade sem expor dados pessoais.

## ADDED Requirements

### Requirement: Registro de evento por operação relevante
O sistema SHALL registrar um evento de auditoria para cada operação de detecção, seleção de tipos, anonimização ou exportação, contendo identificador do evento, data/hora, identificador do operador, canal de entrada, ação, tipos selecionados e contagem por tipo.

#### Scenario: Anonimização concluída gera evento
- **WHEN** uma anonimização é concluída com uma seleção de tipos
- **THEN** o sistema registra um evento de auditoria com data/hora, operador, canal, tipos selecionados e contagem por tipo

#### Scenario: Cada execução gera seu próprio evento
- **WHEN** duas execuções de anonimização ocorrem sobre o mesmo texto de origem com seleções diferentes
- **THEN** o sistema registra dois eventos de auditoria distintos, um por execução

### Requirement: Ausência de dado pessoal no evento
O sistema SHALL rejeitar ou sanitizar qualquer campo de um evento de auditoria que contenha texto livre não sanitizado capaz de carregar dado pessoal, antes de persistir o evento.

#### Scenario: Tentativa de gravar trecho de texto original é rejeitada
- **WHEN** uma tentativa de gravar um evento de auditoria inclui um trecho do texto original por engano
- **THEN** o sistema rejeita ou sanitiza o campo antes de persistir o evento

### Requirement: Imutabilidade dos registros
O sistema SHALL impedir, pela interface padrão da aplicação, a edição ou exclusão de qualquer evento de auditoria já gravado.

#### Scenario: Tentativa de editar evento já gravado
- **WHEN** qualquer usuário tenta alterar um evento de auditoria já persistido pela interface padrão
- **THEN** a operação é recusada

### Requirement: Consulta por período, operador e canal
O sistema SHALL permitir consultar o histórico de eventos de auditoria filtrando por período, operador ou canal de entrada, retornando apenas os campos definidos no contrato do evento.

#### Scenario: Consulta filtrada por período e operador
- **WHEN** uma consulta de auditoria é feita informando período e operador
- **THEN** o sistema retorna apenas os eventos correspondentes, sem nenhum dado pessoal
