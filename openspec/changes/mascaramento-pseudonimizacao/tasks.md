## 1. Identidade de entidade e atribuição de índice

- [ ] 1.1 Implementar função que normaliza o texto de uma entidade detectada (case/espaços) para decidir identidade e verificar com teste que duas ocorrências do mesmo nome (mesma capitalização variável) são tratadas como a mesma entidade
- [ ] 1.2 Implementar atribuição de índice sequencial por tipo, na ordem de primeira aparição, reaproveitando o índice para entidades repetidas, e verificar com teste que duas entidades diferentes do mesmo tipo recebem índices diferentes

## 2. Validação de sobreposição

- [ ] 2.1 Implementar validação de sobreposição entre entidades selecionadas (deduplicar sobreposição total, rejeitar sobreposição parcial com erro explícito) e verificar com teste cada um dos três casos (sem sobreposição, sobreposição total, sobreposição parcial)

## 3. Aplicação da substituição

- [ ] 3.1 Implementar a substituição de entidades selecionadas por marcadores `prefixo+índice`, usando reconstrução de segmentos por posição decrescente, e verificar com teste que o texto final preserva offsets corretos para múltiplas entidades
- [ ] 3.2 Verificar com teste que categorias não selecionadas permanecem inalteradas no texto de saída
- [ ] 3.3 Verificar com teste que acentuação, pontuação e quebras de parágrafo são preservadas fora dos trechos substituídos

## 4. Segurança e relatório

- [ ] 4.1 Escrever teste de segurança dedicado que confirma que nenhum valor original das entidades selecionadas aparece no texto de saída
- [ ] 4.2 Implementar relatório de contagem de entidades mascaradas por tipo e verificar com teste que a contagem reflete apenas os tipos selecionados

## 5. Validação final

- [ ] 5.1 Rodar `python -m pytest` e `python -m compileall .` e registrar o resultado
- [ ] 5.2 Revisar manualmente cada cenário da spec `mascaramento-pseudonimizacao` confirmando que existe teste cobrindo o cenário
