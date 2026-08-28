# Relatório Final - Aula 2

## Etapa 1 (configuração do ambiente)

As ferramentas VSCode, Antigravity e Cursor foram instaladas, ambientes muitos parecidos, mas as flexibilidades de customização e proximidade de uso em relação ao ambiente de trabalho, em especial quanto à integração com modelos onpremise, definiram o VSCode como a escolhida para as etapas seguintes

## Etapa 2 (contexto do projeto)

Seguindo uma ideia de independência dos produtos adotados no momento, adotei uma estratégia de criação do AGENTS.md e do CLAUDE.md com finalidades complementares, o primeiro para orientações gerais e de escopo/restrições, enquanto o segudo ficou para aspectos compatíveis ou necessários ao assistente da Anthropic.

## Etapa 3 (organização do projeto)

Pastas criadas por funcionalidade no projeto, docs/src/tests organizam os artefatos conforme sua finalidade.

## Etapa 4 (boas práticas de prompt)

A funcionalidade escolhida foi a criação de método de extração de texto de um PDF, elemento central da proposta em construção. 

Na experiência de um prompt fraco, resumido e sem contexto ("elabore um método para leitura de arquivos PDF e retorne o seu conteúdo em texto para o método chamador"), o método gerado inclui 3 tratamentos de exceções, num método único e poucos critérios de validação (tamanho, extensão e proteção no PDF). Método simples e direto em 48 linhas.

No prompt mais robusto, com contexto, critérios explícitos e detalhes de implementação, arquitetura e segurança, foi gerado um código com validação de tamanho, assinatura de formato, integridade e legibilidade, identificação de idioma, conteúdo digitalizado e criptografado, sem manter o resultado em arquivo e com os testes implementados.

O modelo usado foi o gpt-5.6 terra, nos testes com modelo mais simples, foi usado o Raptor mini.

## Etapa 5 (integração com github e MCP)

Criado o repositório público em github.com/ppgti-sdd-basics, depois a branch "feature/setup-inicial" e definição de mensagem que orienta os commits futuros.

## Etapa 6 (relatório final)