# Relatório Final - Aula 4

Autor: Bruno dos Santos F. Silva
Data: 06/09/2026

## Escopo da atividade

A atividade desta aula teve como foco a consolidação do fluxo de Spec-Driven Development (SDD) aplicado a um problema real e independente do conteúdo visto em sala de aula: a construção de uma solução para pseudo-anonimização de documentos jurídicos e administrativos, com entrada em PDF, DOCX, texto direto e captura via extensão de navegador, e saída em texto com marcadores sem dados pessoais expostos.

Os princípios centrais do SDD foram aplicados para estruturar a análise e a mudança de escopo antes da implementação: (1) definir claramente o problema e os limites do produto; (2) escrever requisitos e cenários de uso antes do código; (3) separar especificação, design e tarefas executáveis; (4) validar comportamento com critérios observáveis e testes; (5) manter documentação e implementação coerentes; (6) preservar privacidade e segurança em todo o ciclo de desenvolvimento.

No contexto do projeto, a atividade não ficou restrita apenas ao que foi discutido em aula. O escopo foi ampliado para um domínio real e relevante de negócio, com especificações que cobrem entrada multicanal, seleção de categorias de anonimizacao pelo operador, detecção, pseudo-anonimização, auditoria e integração com extensão de navegador. Esse ajuste foi necessário para alinhar o repositório a um cenário de software aplicável em produção e com requisitos de confidencialidade.

## Etapa 1

O escopo detalhado das funcionalidades adicionais escolhidas para especificação no projeto está disponível em [/docs/escopo.md].

Esse documento aprofunda duas funcionalidades-chave do projeto: a seleção de categorias pelo operador antes da anonimização e a substituição por marcadores de pseudo-anonimização. Ele também articula a justificativa para tratar essas capacidades como especificações de negócio e não como simples implementações pontuais.

## Etapa 2

A etapa 2 focou na construção das especificações no projeto com OpenSpec, como principal mecanismo para organizar e versionar a mudança de escopo de forma disciplinada.

As especificações criadas e estruturadas no repositório estão localizadas em:

- openspec/changes/
  - selecao-categorias-operador/ (1)
  - entrada-multicanal/ (2)
  - deteccao-entidades/ (3)
  - mascaramento-pseudonimizacao/ (4)
  - extensao-navegador/ (5)
  - auditoria-operacoes/ (6)

Cada mudança contém a proposta, o design e a definição das tarefas, permitindo separar as capacidades em artefatos de escopo menores e verificáveis. Não achei necessário alterar os planos propostos para 3 funcionalidades iniciais em análise (1, 2, 4), todas apresentavam propostas mais completas do que pensava inicialmente para o caso, em especial quanto aos testes de validação e auditoria.

A adoção do OpenSpec foi motivada por três fatores principais:

1. Adequação a projetos existentes: ele funciona bem em repositórios que já possuem documentação, requisitos e alguma estrutura de código, permitindo evoluir sem perder o contexto do projeto.
2. Maior simplicidade de pipeline: o fluxo de proposta → especificação → design → tarefas é mais direto e compreensível do que um modelo genérico de documentação dispersa.
3. Experimentação inicial dos estudos: o OpenSpec facilita a criação de mudanças em etapas e a validação em um contexto de pesquisa e aprendizado, sem exigir uma organização rígida de produto antes da maturação do escopo.


## Etapa 3

A etapa 3 consolidou as tarefas implementadas no plano de tarefas de implementação da capability de entrada multicanal e mascaramento em integração com a seleção de categorias e a auditoria posterior. Nesta etapa, o projeto avançou com a implementação efetiva dos contratos e testes, validando o comportamento antes de expandir para as próximas camadas.

As funcionalidades implementadas e os arquivos correspondentes foram:

- Entrada multicanal: [src/backend/entrada_multicanal.py](src/backend/entrada_multicanal.py)
- Catalogo de categorias e regras de unicidade: [src/backend/categorias.py](src/backend/categorias.py)
- Seleção de categorias do operador e sessão: [src/backend/selecao.py](src/backend/selecao.py)
- Mascaramento por marcador e contagem por tipo: [src/backend/mascaramento.py](src/backend/mascaramento.py)
- Testes de entrada multicanal: [tests/backend/test_entrada_multicanal.py](tests/backend/test_entrada_multicanal.py)
- Testes de mascaramento: [tests/backend/test_mascaramento.py](tests/backend/test_mascaramento.py)
- Testes de catálogo e seleção: [tests/backend/test_categorias.py](tests/backend/test_categorias.py) e [tests/backend/test_selecao.py](tests/backend/test_selecao.py)

Apesar as instrucoes, um erro persistiu e foi identificado quando o adaptador de PDF tentava acessar o arquivo físico em disco mesmo quando o objeto vinha de um caminho inexistente no contexto de teste, gerando `FileNotFoundError` em vez de retornar um contrato coerente de documento. A correção preservou o texto extraído e calculou o tamanho com fallback seguro em bytes.

As falhas encontradas aparentemente estavam relacionadas ao modelo mais simples e com menor janela de contexto usado para essa etapa da experimentacao com o SDD.

## Etapa 4

A transição de planejamento para implementação deve ser bloqueada por um checkpoint humano obrigatório. Essa regra foi incorporada ao contrato de governança do projeto, em [AGENTS.md](AGENTS.md) e [CLAUDE.md](CLAUDE.md), como garantia de controle antes do início da execução real.

A justificativa central é que a etapa de planejamento define escopo, requisitos, riscos e decisões de arquitetura, mas a implementação pode introduzir mudanças de alto impacto mesmo quando o plano parece estável. O checkpoint humano atua como ponto de validação antes da transição, reduzindo risco de divergência entre documentação, código e intenção do produto.

Em termos práticos, esse checkpoint exige apresentação de um relatório de conformidade com escopo, requisitos atendidos, riscos, dependências, diff estrutural e incertezas pendentes, além de confirmação explícita do desenvolvedor antes do avanço para a execução. Essa disciplina torna o processo mais previsível, auditável e coerente com a abordagem SDD adotada pelo projeto.

## Etapa 5

Nao realizado a tempo

## Etapa 6

Projeto publicado em https://github.com/bruno774/ppgti-sdd-basics (repositorio publico) como continuacao do projeto iniciado na aula 2.