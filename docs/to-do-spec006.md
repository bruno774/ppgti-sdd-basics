# Plano de tarefas — Especificação 006 (Ajuste de categorias pelo operador)

Plano de implementação para a [especificação 006](especificacoes/006-selecao-categorias-operador/spec.md). As tarefas seguem a separação de camadas definida em [AGENTS.md](../AGENTS.md) (extração, detecção, revisão/seleção, mascaramento, auditoria) e devem ser executadas em ordem, cada uma com teste focado antes de avançar para a próxima.

## Fase 0 — Pré-condições

- [ ] 0.1 Confirmar se já existe modelagem de perfis (`operador`, `gestor`, `suporte`) no backend; caso não exista, registrar como dependência bloqueante e abrir/atualizar uma especificação própria de perfis/autorização antes de iniciar a Fase 2 (fora do escopo desta spec, ver "Riscos e não-escopo").
- [ ] 0.2 Confirmar se já existe um modelo de catálogo de entidades persistido (banco/arquivo) ou se o catálogo ainda é apenas a documentação em [docs/requisitos/catalogo-entidades.md](requisitos/catalogo-entidades.md). Se não existir, esta tarefa inclui criar a primeira versão persistida.

## Fase 1 — Domínio: catálogo e seleção de categorias

- [ ] 1.1 Modelar `CategoriaEntidade` (tipo canônico, prefixo de marcador, sensível, origem: `padrao` ou `customizada`) em `src/backend/`, independente de Django, com validação Pydantic.
- [ ] 1.2 Semear o catálogo padrão (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) como dados fixos de origem `padrao`, não removíveis.
- [ ] 1.3 Implementar função de cadastro de categoria customizada com validação de unicidade de `tipo_canonico` e `prefixo_marcador` contra todo o catálogo (padrão + customizadas existentes).
- [ ] 1.4 Implementar função de remoção de categoria que rejeita explicitamente qualquer tentativa de remover uma categoria de origem `padrao`, retornando erro acionável.
- [ ] 1.5 Testes unitários: cadastro válido, cadastro com prefixo conflitante com categoria padrão, cadastro com prefixo conflitante com categoria customizada, tentativa de remoção de categoria padrão (deve falhar), remoção de categoria customizada (deve funcionar, se aplicável ao escopo).

## Fase 2 — Perfis e seleção do operador

- [ ] 2.1 Modelar `SelecaoCategorias` (perfil ativo, categorias selecionadas, categorias disponíveis) conforme contrato da especificação.
- [ ] 2.2 Garantir que toda nova sessão inicia com `perfil = operador` por padrão, sem exigir configuração explícita.
- [ ] 2.3 Implementar troca explícita de perfil (`gestor`, `suporte`) como ação isolada e auditável, sem efeitos colaterais implícitos sobre a seleção de categorias já feita.
- [ ] 2.4 Garantir que `categorias_disponiveis` sempre inclui as categorias padrão, independentemente da seleção atual do operador.
- [ ] 2.5 Testes unitários: sessão nova assume perfil `operador`; troca explícita para `gestor`/`suporte` funciona; ausência de troca nunca ativa esses perfis; lista de categorias disponíveis nunca omite categorias padrão.

## Fase 3 — Integração com detecção e mascaramento

- [ ] 3.1 Conectar `SelecaoCategorias.categorias_selecionadas` à etapa de mascaramento (especificação 003), garantindo que apenas os tipos selecionados sejam substituídos e os demais permaneçam inalterados.
- [ ] 3.2 Validar que a numeração dos marcadores (`prefixo+índice`) considera apenas as categorias selecionadas na execução corrente, sem "reservar" índices para tipos não selecionados.
- [ ] 3.3 Testes de integração: documento com múltiplos tipos detectados, seleção parcial aplicada corretamente; tipos não selecionados permanecem no texto de saída sem alteração.

## Fase 4 — Repetição do processamento sobre o texto de origem

- [ ] 4.1 Modelar `ExecucaoAnonimizacao` (`id_execucao`, `id_origem`, `categorias_selecionadas`) e um mecanismo de retenção do texto de origem por sessão (em memória ou armazenamento temporário protegido), respeitando os limites de confidencialidade de [RNF01](requisitos/requisitos-nao-funcionais.md#rnf01--privacidade-e-segurança).
- [ ] 4.2 Implementar fluxo de "repetir processamento": nova seleção de categorias aplicada sempre sobre `id_origem` (texto original), nunca sobre um resultado já anonimizado de execução anterior.
- [ ] 4.3 Implementar expurgo/expiração do texto de origem retido (ex.: fim de sessão, tempo limite configurável), com erro acionável ao tentar repetir o processamento após a expiração.
- [ ] 4.4 Testes: duas execuções sobre o mesmo `id_origem` com seleções diferentes produzem resultados independentes e corretos; tentativa de repetição após expurgo/expiração retorna erro claro, sem reaproveitar resultado anterior como origem.

## Fase 5 — Auditoria

- [ ] 5.1 Emitir um evento de auditoria por execução (`selecao` e `anonimizacao`), incluindo perfil ativo, canal de entrada, categorias selecionadas e contagem por tipo, conforme [especificação 005](especificacoes/005-auditoria/spec.md).
- [ ] 5.2 Garantir que o cadastro de categoria customizada também gere evento de auditoria (`origem_cadastro`, tipo canônico, prefixo), sem incluir exemplos de texto real usados para justificar a categoria.
- [ ] 5.3 Testes de segurança: nenhum evento de auditoria gerado nesta funcionalidade contém texto original, trechos de documento ou valores de entidades.

## Fase 6 — Interface do operador (frontend)

- [ ] 6.1 Tela/etapa de seleção de categorias antes da submissão, exibindo todas as categorias disponíveis (padrão sempre visíveis) com estado de seleção persistido durante a sessão (RF03.4).
- [ ] 6.2 Ação de "cadastrar nova categoria" restrita à validação de unicidade da Fase 1, com mensagem de erro clara em caso de conflito.
- [ ] 6.3 Ação de "repetir processamento" visível após a conclusão de uma anonimização, reabrindo a tela de seleção de categorias sem exigir novo upload/colagem do conteúdo, enquanto o texto de origem ainda estiver retido na sessão.
- [ ] 6.4 Testes de interface/fluxo: seleção parcial, tentativa de remoção de categoria padrão bloqueada na UI, repetição de processamento com nova seleção.

## Fase 7 — Validação final

- [ ] 7.1 Executar `python -m pytest` e `python -m compileall .` e registrar o resultado.
- [ ] 7.2 Revisar manualmente os critérios de aceite da especificação 006, item a item, confirmando cobertura de teste para cada um.
- [ ] 7.3 Atualizar a especificação 006 (ou abrir uma nova) caso qualquer decisão de implementação diverja do texto atual, mantendo documentação e código coerentes (ver [AGENTS.md](../AGENTS.md)).

## Dependências e bloqueios conhecidos

- A Fase 2 depende de uma definição mínima de autenticação/perfis que hoje não existe implementada no repositório; se essa definição não existir, registrar o bloqueio explicitamente antes de prosseguir, em vez de improvisar um modelo de perfis não especificado.
- A Fase 4 depende de uma decisão de produto sobre por quanto tempo o texto de origem pode ficar retido em sessão para permitir repetição do processamento; até essa decisão existir, usar um limite conservador e documentá-lo como suposição explícita.
