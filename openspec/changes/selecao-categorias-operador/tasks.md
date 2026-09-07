## 1. Domínio: catálogo e categorias

- [x] 1.1 Modelar `CategoriaEntidade` (tipo canônico, prefixo de marcador, sensível, origem `padrao`/`customizada`) com validação Pydantic e verificar com teste unitário que instâncias inválidas (tipo vazio, prefixo vazio) são rejeitadas
- [x] 1.2 Semear o catálogo padrão (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) e verificar com teste que todas aparecem com origem `padrao`
- [x] 1.3 Implementar função de validação de unicidade de `tipo_canonico`/`prefixo_marcador` contra todo o catálogo e verificar com teste que detecta colisão com categoria padrão e com categoria customizada
- [x] 1.4 Implementar cadastro de categoria customizada usando a validação de unicidade e verificar com teste que cadastro válido é aceito e cadastro conflitante é rejeitado com erro acionável
- [x] 1.5 Implementar remoção de categoria que rejeita explicitamente categorias de origem `padrao` e verificar com teste que a tentativa de remoção de uma categoria padrão falha e a categoria continua disponível

## 2. Perfis e seleção do operador

- [x] 2.1 Modelar `SelecaoCategorias` (perfil ativo, categorias selecionadas, categorias disponíveis) e verificar com teste que a serialização/validação do modelo funciona
- [x] 2.2 Implementar inicialização de sessão com `perfil = operador` por padrão e verificar com teste que uma sessão nova, sem troca explícita, sempre expõe `perfil == "operador"`
- [x] 2.3 Implementar ação de troca explícita de perfil (`gestor`, `suporte`) como evento isolado e verificar com teste que a troca funciona e que a ausência de troca nunca resulta em `gestor`/`suporte`
- [x] 2.4 Garantir que `categorias_disponiveis` sempre inclui as categorias padrão independentemente da seleção atual e verificar com teste que a lista nunca omite uma categoria padrão

## 3. Integração com detecção e mascaramento

- [ ] 3.1 Conectar `categorias_selecionadas` à etapa de mascaramento existente, garantindo que apenas os tipos selecionados sejam substituídos, e verificar com teste de integração que categorias não selecionadas permanecem inalteradas na saída
- [ ] 3.2 Garantir que a numeração dos marcadores (`prefixo+índice`) considera somente as categorias selecionadas na execução corrente e verificar com teste que nenhum índice é "reservado" para tipos não selecionados

## 4. Repetição do processamento sobre o texto de origem

- [ ] 4.1 Modelar `ExecucaoAnonimizacao` (`id_execucao`, `id_origem`, `categorias_selecionadas`) e um mecanismo de retenção do texto de origem por sessão, com expiração configurável, e verificar com teste que o texto retido expira após o limite configurado
- [ ] 4.2 Implementar o fluxo de repetição de processamento a partir de `id_origem` e verificar com teste que duas execuções com seleções diferentes sobre o mesmo `id_origem` produzem resultados independentes e corretos
- [ ] 4.3 Implementar erro acionável ao tentar repetir o processamento após expiração/indisponibilidade do texto de origem e verificar com teste que o sistema não reaproveita um resultado já anonimizado como origem

## 5. Auditoria

- [ ] 5.1 Emitir evento de auditoria por execução (seleção + processamento), incluindo perfil ativo, canal de entrada, categorias selecionadas e contagem por tipo, e verificar com teste que o evento é gravado corretamente
- [ ] 5.2 Emitir evento de auditoria para cadastro de categoria customizada (tipo canônico, prefixo, origem do cadastro) e verificar com teste que nenhum trecho de texto original é incluído no evento
- [ ] 5.3 Escrever teste de segurança dedicado que varre os eventos de auditoria gerados pelos testes das seções 1 a 4 e confirma ausência de qualquer valor de entidade detectada

## 6. Validação final

- [ ] 6.1 Rodar `python -m pytest` e `python -m compileall .` e registrar o resultado no relatório de implementação
- [ ] 6.2 Revisar manualmente cada cenário da spec `selecao-categorias` (ver `specs/selecao-categorias/spec.md`) confirmando que existe teste cobrindo o cenário
- [ ] 6.3 Atualizar `docs/especificacoes/006-selecao-categorias-operador/spec.md` e `docs/to-do-spec006.md` caso alguma decisão de implementação divirja do texto atual, mantendo documentação e código coerentes
