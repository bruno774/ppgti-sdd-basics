## Purpose

Permite que o operador controle, antes de qualquer processamento de anonimização, quais categorias de dados pessoais e sensíveis serão mascaradas, com um perfil padrão previsível, um catálogo extensível mas protegido contra remoção de categorias padrão, e a possibilidade de repetir o processamento sobre o mesmo texto de origem com outra seleção.

## ADDED Requirements

### Requirement: Perfil padrão da sessão
O sistema SHALL iniciar toda nova sessão com o perfil `operador` ativo, sem exigir configuração explícita, e SHALL exigir uma ação explícita de troca de perfil antes de ativar os perfis `gestor` ou `suporte`.

#### Scenario: Nova sessão sem escolha de perfil
- **WHEN** o operador inicia uma nova sessão sem selecionar explicitamente outro perfil
- **THEN** o sistema mantém o perfil ativo como `operador`

#### Scenario: Perfil elevado nunca é ativado implicitamente
- **WHEN** o usuário realiza qualquer ação disponível ao perfil `operador` sem solicitar troca de perfil
- **THEN** o sistema não concede nenhum comportamento exclusivo dos perfis `gestor` ou `suporte`

#### Scenario: Troca explícita de perfil
- **WHEN** o usuário solicita explicitamente a troca para o perfil `gestor` ou `suporte`
- **THEN** o sistema ativa o perfil solicitado e registra a troca como evento auditável

### Requirement: Seleção de categorias antes do processamento
O sistema SHALL permitir que o operador selecione, antes de qualquer substituição ser aplicada, o subconjunto de categorias do catálogo vigente (padrão e customizadas) que serão anonimizadas, e SHALL preservar sem alteração qualquer entidade de categoria não selecionada.

#### Scenario: Seleção parcial aplicada corretamente
- **WHEN** o operador seleciona apenas algumas categorias entre as detectadas em um documento e confirma o processamento
- **THEN** o sistema mascara somente as entidades das categorias selecionadas e mantém inalteradas as entidades das categorias não selecionadas

#### Scenario: Lista de categorias disponíveis sempre completa
- **WHEN** o sistema apresenta a lista de categorias disponíveis para seleção
- **THEN** a lista inclui todas as categorias padrão do catálogo, independentemente de estarem selecionadas na execução corrente

### Requirement: Catálogo padrão não removível
O sistema SHALL manter permanentemente disponíveis para seleção as categorias padrão do catálogo (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) e SHALL rejeitar qualquer tentativa de removê-las do catálogo.

#### Scenario: Tentativa de remoção de categoria padrão é rejeitada
- **WHEN** qualquer perfil tenta remover uma categoria padrão do catálogo
- **THEN** o sistema rejeita a operação com um erro acionável e mantém a categoria padrão disponível para seleção

#### Scenario: Deixar de selecionar não é remover
- **WHEN** o operador deixa de selecionar uma categoria padrão em uma execução específica
- **THEN** essa categoria permanece no catálogo e disponível para seleção em execuções futuras

### Requirement: Cadastro de categoria customizada
O sistema SHALL permitir o cadastro de novas categorias customizadas com tipo canônico e prefixo de marcador próprios, e SHALL rejeitar o cadastro quando o tipo canônico ou o prefixo de marcador colidir com qualquer categoria já existente no catálogo (padrão ou customizada).

#### Scenario: Cadastro válido de categoria customizada
- **WHEN** um usuário cadastra uma categoria customizada com tipo canônico e prefixo de marcador ainda não usados no catálogo
- **THEN** o sistema adiciona a categoria ao catálogo e ela passa a aparecer na lista de seleção

#### Scenario: Conflito de prefixo com categoria padrão
- **WHEN** um usuário tenta cadastrar uma categoria customizada cujo prefixo de marcador já pertence a uma categoria padrão
- **THEN** o sistema rejeita o cadastro com um erro acionável, sem alterar o catálogo

#### Scenario: Conflito de prefixo com categoria customizada existente
- **WHEN** um usuário tenta cadastrar uma categoria customizada cujo prefixo de marcador já pertence a outra categoria customizada existente
- **THEN** o sistema rejeita o cadastro com um erro acionável, sem alterar o catálogo

### Requirement: Repetição do processamento sobre o texto de origem
O sistema SHALL permitir repetir o processamento de anonimização sobre o texto de origem original, com uma nova seleção de categorias, sem exigir novo envio do conteúdo, e SHALL impedir que uma repetição utilize um resultado já anonimizado como se fosse a origem.

#### Scenario: Repetição com nova seleção de categorias
- **WHEN** o operador solicita repetir o processamento de um texto de origem já processado, selecionando um conjunto diferente de categorias
- **THEN** o sistema gera um novo resultado de anonimização a partir do texto de origem original, aplicando apenas as categorias da nova seleção

#### Scenario: Texto de origem indisponível
- **WHEN** o operador solicita repetir o processamento após o texto de origem ter expirado ou não estar mais disponível na sessão
- **THEN** o sistema informa que é necessário fornecer o conteúdo novamente, sem reutilizar um resultado anonimizado anterior como origem

#### Scenario: Cada execução gera seu próprio evento de auditoria
- **WHEN** duas execuções de anonimização ocorrem sobre o mesmo texto de origem com seleções de categorias diferentes
- **THEN** o sistema registra um evento de auditoria distinto para cada execução, sem dados pessoais
