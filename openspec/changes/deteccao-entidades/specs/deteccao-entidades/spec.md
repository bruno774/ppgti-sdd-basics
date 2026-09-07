## Purpose

Identifica entidades pessoais e sensíveis no texto normalizado, com tipo canônico, posição, confiança e origem, para que o operador possa revisar e selecionar quais serão anonimizadas antes de qualquer substituição.

## ADDED Requirements

### Requirement: Detecção de entidades do catálogo
O sistema SHALL identificar, no texto normalizado, ocorrências dos tipos do catálogo vigente (`NOME`, `CPF`, `RG`, `ENDERECO`, `EMAIL`, `TELEFONE`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL` e categorias customizadas), retornando para cada ocorrência tipo canônico, intervalo `[início, fim)`, confiança e origem.

#### Scenario: Detecção de CPF em formatos comuns
- **WHEN** o texto contém um CPF nos formatos `000.000.000-00` ou `00000000000`
- **THEN** o sistema retorna uma detecção do tipo `CPF` com o intervalo de posição correto

#### Scenario: Detecção não gera falso positivo para tipo sensível ausente
- **WHEN** o texto não contém nenhuma menção a doença, religião, gênero, cor/raça ou classe social
- **THEN** o sistema não retorna nenhuma detecção para esses tipos sensíveis

### Requirement: Limiar de confiança e revisão obrigatória para tipos sensíveis
O sistema SHALL aplicar um limiar de confiança mais rigoroso aos tipos sensíveis (`CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) e SHALL sinalizar toda detecção desses tipos como pendente de revisão obrigatória do operador, independentemente da confiança calculada.

#### Scenario: Detecção sensível sinalizada para revisão
- **WHEN** o sistema detecta uma entidade de tipo sensível, com qualquer nível de confiança
- **THEN** a detecção é retornada com a marcação `sensivel = true`, indicando revisão obrigatória antes de qualquer aplicação

#### Scenario: Duas entidades sensíveis distintas do mesmo tipo
- **WHEN** o texto cita duas religiões diferentes associadas a pessoas diferentes
- **THEN** o sistema retorna duas detecções distintas do tipo `RELIGIAO`, cada uma com seu próprio intervalo de posição

### Requirement: Ausência de inferência por estereótipo
O sistema SHALL rejeitar a atribuição de um tipo sensível a um trecho de texto quando a única evidência for nome próprio, localização geográfica ou associação indireta, sem menção textual explícita ao atributo sensível.

#### Scenario: Menção a bairro sem renda ou profissão explícita
- **WHEN** o texto apenas menciona um bairro, sem qualquer menção explícita a renda, profissão ou classe social
- **THEN** o sistema não gera uma detecção de `CLASSE_SOCIAL` para esse trecho

### Requirement: Determinismo da detecção
O sistema SHALL produzir exatamente as mesmas detecções para a mesma entrada, configuração de catálogo e versão do componente de detecção.

#### Scenario: Reprocessamento do mesmo texto produz o mesmo resultado
- **WHEN** o mesmo texto é processado duas vezes com a mesma configuração e versão
- **THEN** o conjunto de detecções retornado é idêntico nas duas execuções

### Requirement: Extensibilidade sem alteração do fluxo principal
O sistema SHALL permitir a inclusão de novos tipos de entidade no catálogo (ver capability `selecao-categorias`) sem exigir alteração do fluxo principal de extração, revisão ou mascaramento.

#### Scenario: Novo tipo customizado passa a ser detectável
- **WHEN** uma nova categoria customizada é cadastrada no catálogo com uma regra de detecção associada
- **THEN** o sistema passa a retornar detecções desse novo tipo sem exigir mudança na etapa de entrada ou de mascaramento
