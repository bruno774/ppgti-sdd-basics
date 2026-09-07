## 1. Contrato de dados

- [ ] 1.1 Modelar `EventoAuditoria` (id, timestamp, operador_id, canal_entrada, acao, tipos_selecionados, contagem_por_tipo, documento_hash) com validação Pydantic e verificar com teste que campos com formato inválido (ex.: operador_id como texto livre longo) são rejeitados
- [ ] 1.2 Implementar validação/sanitização que rejeita qualquer valor de campo incompatível com o formato esperado antes de persistir, verificando com teste que um evento com um trecho de texto longo no lugar de um campo estruturado é rejeitado

## 2. Registro append-only

- [ ] 2.1 Implementar `registrar_evento(evento)` que adiciona o evento a um armazenamento append-only, verificando com teste que o evento gravado é recuperável
- [ ] 2.2 Verificar com teste que não existe nenhuma função pública de edição ou exclusão de evento já registrado

## 3. Consulta

- [ ] 3.1 Implementar `consultar_eventos(desde=None, ate=None, operador_id=None, canal_entrada=None)` e verificar com teste que cada filtro (isolado e combinado) retorna o subconjunto esperado de eventos
- [ ] 3.2 Verificar com teste que a consulta nunca retorna campos fora do contrato `EventoAuditoria` (sem dado pessoal)

## 4. Validação final

- [ ] 4.1 Rodar `python -m pytest` e `python -m compileall .` e registrar o resultado
- [ ] 4.2 Revisar manualmente cada cenário da spec `auditoria` confirmando que existe teste cobrindo o cenário
