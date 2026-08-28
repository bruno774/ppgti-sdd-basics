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

Repo: https://github.com/bruno774/ppgti-sdd-basics/ (com todos os artefatos solicitados, inclusive o projeto)

No arquivo AGENTS.md, crítico nas definições do projeto, uma trecho relevante está copiado abaixo, definindo o papel dos agentes de IA na interpretação e nos limites em relação ao projeto:

    ## Orientacoes para agentes

    Antes de editar, localizar a camada que controla diretamente o comportamento solicitado e formular uma hipotese verificavel. Fazer a menor alteracao coerente com as convencoes acima. Depois da primeira edicao, executar imediatamente o teste ou comando de validacao mais especifico disponivel.

    Nao inventar dependencias, formatos de API ou garantias de privacidade. Quando uma decisao de produto estiver indefinida, preservar os dados, sinalizar a incerteza e pedir revisao do operador. Nunca fazer commit ou reverter alteracoes de outros contribuidores sem solicitacao explicita.

Trecho do CLAUDE.md:

    # CLAUDE.md

    ## Papel do agente Claude

    Atue como agente de implementacao para uma ferramenta de anonimização de documentos juridicos e administrativos em PDF ou TXT. Siga primeiro as regras de `AGENTS.md`; este arquivo acrescenta instrucoes especificas para execucoes feitas por Claude.

A relevância está na atuação de hierarquia entre os arquivos, onde o AGENTS.md assume o papel descrito principal e o CLAUDE.md com suas instruções específicas, uma estratégia de ampliação de compatibilidade entre assistentes de IA atuais, mantendo o padrão aberto mais aceito com o primeiro arquivo.

Pull request aberto em https://github.com/bruno774/ppgti-sdd-basics/pull/1

MCP disponível em .mcp.json

