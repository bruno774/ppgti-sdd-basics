# Especificação 006 — Ajuste de categorias de dados pelo operador antes do processamento

## História de usuário

> Como **operador** (perfil padrão da ferramenta), quero **ajustar quais categorias de dados pessoais e sensíveis serão anonimizadas antes de submeter o documento para processamento**, para que eu controle exatamente o que é mascarado em cada execução, sem depender de um perfil com privilégios adicionais.

## Objetivo

Permitir que o operador, antes de qualquer chamada de detecção/anonimização, selecione e ajuste o conjunto de categorias (tipos canônicos do catálogo, incluindo eventuais categorias customizadas) que serão efetivamente anonimizadas, e permitir repetir o processamento do mesmo conteúdo com uma seleção de categorias diferente, sem reenviar o documento de origem.

Esta especificação detalha [RF03.1 e RF03.4](../../requisitos/requisitos-funcionais.md#rf03--seleção-e-parametrização-pelo-operador), incorporando as regras de perfis de acesso e de customização do catálogo definidas no PRD.

## Escopo

Incluído:

- Seleção, pelo perfil **operador**, do subconjunto de categorias do catálogo a anonimizar, antes de qualquer substituição ser aplicada.
- Regra de perfis: **operador** é o perfil padrão de qualquer sessão da ferramenta; os perfis **gestor** e **suporte** só se aplicam mediante escolha explícita (troca de perfil), nunca por padrão.
- Adição de novas categorias customizadas ao catálogo (nome, prefixo de marcador, nível de sensibilidade), reaproveitando a extensibilidade prevista em [RF02.3](../../requisitos/requisitos-funcionais.md#rf02--detecção-de-entidades) e no [catálogo de entidades](../../requisitos/catalogo-entidades.md).
- Bloqueio da remoção das categorias padrão do catálogo (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`): elas permanecem sempre disponíveis para seleção, mesmo que o operador nunca as escolha em uma execução específica.
- Repetição do processamento de anonimização sobre o mesmo texto de origem, com uma nova seleção de categorias, sem exigir novo envio/upload do documento.

Fora de escopo:

- Definição completa de permissões dos perfis **gestor** e **suporte** (tratada em especificação própria de perfis/autorização, ainda não elaborada).
- Edição ou remoção de categorias já aplicadas em um documento já exportado (a especificação cobre apenas o ajuste **antes** da submissão e a repetição **sobre o texto de origem ainda disponível na sessão**).
- Persistência de categorias customizadas entre sessões de operadores diferentes (tratada como requisito futuro, fora desta especificação).

## Cenários

### Seleção antes do processamento (perfil padrão)

- **Dado** que o operador inicia uma nova sessão sem escolher explicitamente outro perfil, **quando** o sistema apresenta a tela de seleção de categorias, **então** o perfil ativo é `operador` e a lista de categorias exibida corresponde ao catálogo vigente (padrão + customizadas, se houver).
- **Dado** um documento com entidades detectadas de múltiplos tipos, **quando** o operador desmarca `ENDERECO` e `CID_DOENCA` antes de confirmar, **então** o processamento de anonimização deve ignorar essas categorias e aplicar apenas as demais selecionadas.
- **Dado** um usuário que deseja atuar como `gestor` ou `suporte`, **quando** ele não realiza a troca explícita de perfil, **então** o sistema mantém o perfil `operador` e não concede nenhum comportamento adicional desses outros perfis.

### Customização do catálogo (adição sem remoção)

- **Dado** o operador com necessidade de reconhecer um novo tipo de dado sensível não previsto no catálogo padrão (por exemplo um identificador funcional interno), **quando** ele cadastra uma nova categoria com tipo canônico e prefixo de marcador únicos, **então** essa categoria passa a aparecer na lista de seleção junto às categorias padrão, sem alterar o fluxo principal de detecção/mascaramento (RF02.3).
- **Dado** o catálogo com categorias padrão e customizadas, **quando** o operador (ou qualquer perfil) tenta remover uma categoria padrão da lista de seleção disponível, **então** o sistema rejeita a remoção e mantém a categoria padrão sempre disponível para seleção (podendo apenas deixar de ser **selecionada** em uma execução específica, o que é diferente de removê-la do catálogo).
- **Dado** duas categorias customizadas com o mesmo prefixo de marcador de uma categoria padrão já existente, **quando** o operador tenta cadastrá-la, **então** o sistema rejeita o cadastro por conflito de prefixo, evitando colisão de marcadores (ver [catálogo de entidades](../../requisitos/catalogo-entidades.md)).

### Repetição do processamento com outra seleção

- **Dado** um documento já anonimizado com a seleção `{NOME, CPF}`, **quando** o operador decide repetir o processamento sobre o mesmo texto de origem selecionando agora `{ENDERECO, EMAIL}`, **então** o sistema gera um novo resultado de anonimização a partir do texto original (não do texto já mascarado), aplicando apenas as categorias da nova seleção.
- **Dado** duas execuções de anonimização sobre o mesmo texto de origem com seleções diferentes, **quando** cada execução é concluída, **então** cada uma gera seu próprio evento de auditoria (RF06.1), preservando o histórico de que houve mais de uma execução com parametrizações distintas.
- **Dado** que a sessão do operador expirou ou o texto de origem não está mais disponível em memória/sessão, **quando** o operador tenta repetir o processamento, **então** o sistema informa que é necessário fornecer o conteúdo novamente, em vez de reutilizar um resultado anonimizado anterior como se fosse a origem.

## Contratos de dados

Seleção de categorias (`SelecaoCategorias`):

- `perfil`: perfil ativo no momento da seleção (`operador` por padrão; `gestor` ou `suporte` apenas se explicitamente escolhido).
- `categorias_selecionadas`: lista de tipos canônicos (padrão e/ou customizados) escolhidos para a execução corrente.
- `categorias_disponiveis`: lista completa do catálogo vigente, sempre incluindo todas as categorias padrão, independentemente da seleção atual.

Categoria customizada (`CategoriaCustomizada`), estendendo o [catálogo de entidades](../../requisitos/catalogo-entidades.md):

- `tipo_canonico`: identificador em maiúsculas, único no catálogo.
- `prefixo_marcador`: prefixo em minúsculas, único no catálogo (não pode colidir com prefixos padrão ou de outras categorias customizadas).
- `sensivel`: booleano indicando se exige limiar de confiança elevado e revisão obrigatória.
- `origem_cadastro`: identificador de quem cadastrou a categoria, para fins de auditoria.

Repetição de execução (`ExecucaoAnonimizacao`):

- `id_execucao`: identificador único de cada execução sobre o mesmo texto de origem.
- `id_origem`: identificador estável do texto de origem, permitindo agrupar múltiplas execuções sobre o mesmo conteúdo sem reidentificar seu valor.
- `categorias_selecionadas`: seleção usada nesta execução específica.

## Critérios de aceite

- O perfil `operador` é sempre o perfil inicial de qualquer sessão nova; nenhuma ação implícita ativa os perfis `gestor` ou `suporte`.
- Todas as categorias padrão do catálogo permanecem sempre visíveis e selecionáveis, mesmo após tentativas de remoção.
- Uma categoria customizada só é aceita no catálogo se possuir tipo canônico e prefixo de marcador únicos.
- Repetir o processamento com nova seleção de categorias sempre parte do texto de origem, nunca do resultado anonimizado de uma execução anterior.
- Cada execução (seleção + processamento) gera um evento de auditoria próprio, conforme [especificação 005](005-auditoria/spec.md), sem dados pessoais.
- Testes cobrem: seleção padrão sem troca de perfil, tentativa de remoção de categoria padrão, cadastro de categoria customizada válida e com conflito de prefixo, e repetição de execução com seleções diferentes.

## Riscos e não-escopo

- Esta especificação não define o conjunto de permissões dos perfis `gestor` e `suporte` além da regra de que exigem escolha explícita; uma especificação de perfis/autorização própria deve detalhar o que cada perfil pode fazer além do fluxo do operador.
- Categorias customizadas mal definidas (prefixo ambíguo, tipo genérico demais) podem gerar falsos positivos; a validação de unicidade de prefixo é obrigatória, mas não substitui revisão de qualidade da categoria cadastrada.
- A retenção do texto de origem para permitir repetição do processamento deve respeitar os mesmos limites de confidencialidade e expurgo definidos em [RNF01](../../requisitos/requisitos-nao-funcionais.md#rnf01--privacidade-e-segurança); manter o texto em sessão por tempo indefinido não é aceitável.
