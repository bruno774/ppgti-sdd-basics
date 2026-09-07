## Purpose

Permite capturar, mediante ação explícita do operador, o conteúdo de uma caixa de texto em uma página web, enviá-lo para detecção/anonimização, e devolver o texto anonimizado ao mesmo campo, com permissões mínimas de navegador.

## ADDED Requirements

### Requirement: Captura mediante ação explícita
A extensão SHALL capturar o conteúdo de um campo de texto da página somente mediante ação explícita do operador sobre esse campo, e SHALL nunca capturar conteúdo de forma automática ou em segundo plano.

#### Scenario: Captura acionada pelo operador
- **WHEN** o operador aciona a extensão sobre uma caixa de texto específica da página
- **THEN** a extensão captura apenas o conteúdo daquele campo, sem acessar outras partes da página

#### Scenario: Nenhuma captura sem ação explícita
- **WHEN** a página é carregada ou o operador navega sem acionar a extensão
- **THEN** nenhum conteúdo é capturado ou enviado

### Requirement: Seleção de categorias antes da anonimização
A extensão SHALL exibir as entidades detectadas no conteúdo capturado e SHALL permitir ao operador selecionar as categorias a anonimizar antes de aplicar qualquer substituição, reaproveitando o fluxo de seleção da capability `selecao-categorias`.

#### Scenario: Seleção de categorias no fluxo da extensão
- **WHEN** o conteúdo capturado é enviado ao backend e as entidades são detectadas
- **THEN** a extensão exibe as entidades e aguarda a seleção de categorias do operador antes de solicitar a anonimização

### Requirement: Devolução do texto anonimizado ao campo de origem
A extensão SHALL permitir devolver o texto anonimizado ao campo de origem, substituindo ou complementando o conteúdo conforme escolha do operador.

#### Scenario: Devolução ao campo original
- **WHEN** o operador confirma a devolução do texto anonimizado
- **THEN** a extensão substitui ou complementa o conteúdo do campo de origem, conforme a escolha do operador

### Requirement: Permissões mínimas e ausência de persistência
A extensão SHALL solicitar no manifesto apenas as permissões mínimas necessárias (aba ativa e domínio autorizado), e SHALL não persistir o conteúdo capturado em `localStorage`, `IndexedDB` ou logs do navegador além da sessão em memória necessária para exibir o resultado.

#### Scenario: Permissão ausente para o domínio atual
- **WHEN** o operador aciona a extensão em um domínio sem permissão concedida
- **THEN** a extensão solicita a permissão explicitamente, sem falhar silenciosamente

#### Scenario: Falha de comunicação com o backend
- **WHEN** ocorre uma falha de comunicação entre a extensão e o backend configurado
- **THEN** a extensão exibe um erro claro ao operador, sem expor o conteúdo capturado em console ou log persistente
