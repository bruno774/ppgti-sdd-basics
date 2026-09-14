# Relatório Final - Aula 6

Bruno dos Santos F. Silva  
E-mail: brunosfs@gmail.com  
11/09/2026  
Repositório: https://github.com/bruno774/ppgti-sdd-basics

## Etapa 1 - Harness mínimo: autonomia e guardrail

A tarefa pequena escolhida foi organizar e implementar o fluxo de entrada multicanal, seleção de categorias e mascaramento, mantendo os contratos documentados no projeto.

A comparação entre os modos de autonomia do agente no modo plan e auto. No modo de planejamento, o agente apresentou primeiro a proposta, os arquivos envolvidos e os riscos. Esse modo levou mais tempo (em torno de 5min com leitura e aprovação), mas proporcionou maior sensação de controle e facilitou a revisão do escopo antes da alteração. No modo de aceitação automática de edições, a execução foi mais rápida (em torno de 1min e 30s), porém o risco percebido foi maior, porque as alterações poderiam avançar antes da conferência detalhada dos contratos e dos testes.

A principal conclusão foi que o modo de planejamento é mais adequado quando a mudança envolve privacidade, mudanças de entidades de negócio ou contratos entre módulos. A aceitação automática seria mais útil para ajustes pequenos e reversíveis, desde que exista uma validação logo depois.

O hook escolhido foi um método de validação inserido na tarefa de entrada multicanal, em [src/backend/entrada_multicanal.py](src/backend/entrada_multicanal.py). Antes de extrair um PDF existente, o método confere o limite de tamanho e a assinatura `%PDF-`, rejeitando arquivos incompatíveis. Depois da extração, ele procura padrões explícitos de prompt injection, como instruções para ignorar instruções anteriores, revelar o system prompt ou executar um jailbreak.

Quando encontra um possível prompt injection, o método lança `PromptInjectionDetectedError`, emitindo um alerta e impedindo a continuação do processamento. A mensagem não reproduz o trecho detectado, preservando a confidencialidade do documento. O comportamento foi coberto em [tests/backend/test_entrada_multicanal.py](tests/backend/test_entrada_multicanal.py), com casos para formato incompatível e conteúdo injetado.

## Etapa 2 - TDD como guard-rail

A aplicação seguiu a lógica Red-Green-Refactor nas funcionalidades implementadas. Os testes foram mantidos próximos aos métodos do backend, incluindo entrada multicanal, seleção de categorias, mascaramento, extração de PDF e configurações. Os arquivos de teste estão em:

- [tests/backend/test_entrada_multicanal.py](tests/backend/test_entrada_multicanal.py);
- [tests/backend/test_categorias.py](tests/backend/test_categorias.py);
- [tests/backend/test_selecao.py](tests/backend/test_selecao.py);
- [tests/backend/test_mascaramento.py](tests/backend/test_mascaramento.py);
- [tests/backend/test_pdf_extraction.py](tests/backend/test_pdf_extraction.py).

O histórico do git mostra commits separados de implementação e testes, incluindo `feat: implementacao de tarefas base` e `feat: ajustes no relatorio final 4`. 

A ferramenta de enforcement investigada foi o método de validação da entrada multicanal, utilizado para impedir que um PDF incompatível ou com possível prompt injection avance para as etapas seguintes. Ele é efetivo para esse risco específico, mas não substitui uma ferramenta automatizada especializada de TDD como `tdd-guard` ou `superpowers`. A investigação de instalação de uma dessas ferramentas foi objetiva e buscando aquela que poderia transmitir a melhor aderência de aprendizado a uma prática educativa, que permitisse melhor aprendizado e cumprisse a missão de validação das implementações. Como o `superpowers` possui características de maior simplicidade e avaliação superficial, sendo o `tdd-guard` mais cuidadoso e documentador das suas ações, fiquei com esse último.

A comparação com uma tarefa feita deliberadamente sem testes e uma execução com as proteções de verificação do código, envolvem aspectos como velocidade de implementação (muito superior no caso sem testes), efetividade do resultado e custos com tokens. A inclusão de uma camada de harness melhora a qualidade do código entregue, leva muito mais tempo mas ao mesmo tempo consome muito mais recursos financeiros, dado as diversas interações que tem que ser realizadas no código.

## Etapa 3 - Observabilidade e checkpoint humano

O checkpoint humano definido foi: **defina um checkpoint humano antes de providenciar a sincronização com o repositório remoto (git push), confirmando ter visto as alterações realizadas e que as mesmas estão de acordo com os requisitos documentados, se não for aprovado, retornar para revisão das specs**.

O papel humano é revisar o código gerado, decidir se corresponde ao esperado e se não infringe nenhuma regra absoluta do escopo ou das orientações descritas. Nesta atividade, a decisão foi **aprovar** a implementação depois da revisão dos artefatos adicionados/alterados diante da conformidade verificada.


## Etapa 4 - Revisão arquitetural com apoio de IA

A arquitetura atual está organizada por responsabilidades no backend:

- `entrada_multicanal.py` trata entradas de texto, PDF e DOCX;
- `categorias.py` mantém o catálogo de tipos e prefixos;
- `selecao.py` representa a escolha do operador;
- `mascaramento.py` aplica marcadores e produz contagens;
- `pdf_extraction.py` e `pdf_binary_extraction.py` concentram a extração de PDF;
- `settings.py` concentra configurações;
- `tests/backend/` mantém os testes correspondentes.

As especificações OpenSpec organizam as capacidades em mudanças separadas para entrada multicanal, detecção, mascaramento, extensão, auditoria e seleção de categorias. Isso reduz o acoplamento conceitual e deixa contratos e critérios de aceite mais visíveis.

O principal ponto de acoplamento é o fluxo entre detecção, seleção e mascaramento: as entidades precisam conservar tipo, identificador e offsets até a substituição. A extração de PDF também exige cuidado porque depende de bibliotecas externas e de condições do arquivo físico.

Minha decisão foi manter a modularidade atual neste estágio, sem extrair um serviço separado. O projeto ainda é pequeno, as operações são locais e a separação por módulos já atende à clareza e à testabilidade. Extrair serviços agora aumentaria custo operacional, pontos de falha e complexidade de deploy sem benefício proporcional. Uma futura extração só seria justificável com crescimento de volume, necessidade de escala independente ou integração externa estável.

## Etapa 5 - ADR e diagrama

A decisão arquitetural foi complementada pela [ADR 0003 — Interface web simples para anonimização de documentos](docs/adr/0003-interface-web-anonimizacao-documentos.md). Ela define uma página web única para upload de PDF ou DOCX, colagem de texto, seleção explícita das categorias a anonimizar, início manual do processamento, apresentação do resultado e estatísticas agregadas, como número de palavras, estimativa de tokens, termos anonimizados e tempo de processamento. A decisão mantém a lógica de entrada, detecção, seleção, mascaramento e auditoria centralizada no backend, evitando duplicação de regras na interface. As especificações complementares estão listadas em [docs/especificacoes/README.md](docs/especificacoes/README.md).

O diagrama Mermaid de nível C4 de containers foi documentado em [docs/arquitetura.md](docs/arquitetura.md), junto com um diagrama complementar do fluxo principal. Ele apresenta o operador, a interface web planejada, o backend de processamento atualmente implementado, a extensão de navegador planejada, a auditoria prevista e os documentos de origem. O documento também registra os módulos reais do backend, as fronteiras de privacidade e as lacunas conhecidas, distinguindo componentes implementados de componentes ainda planejados.

O diagrama construído a partir de um prompt que descreveu o contexto do projeto e passou por revisão humana tende a ilustrar melhor a estrutura, as responsabilidades e as fronteiras arquiteturais. Ainda assim, a qualidade da primeira versão, produzida com um prompt mais simples, foi quase tão boa quanto a segunda, porque o contexto do projeto, seus requisitos e suas ADRs já estavam disponíveis na memória de trabalho do agente. A revisão posterior agregou principalmente precisão na distinção entre o que está implementado e o que permanece planejado, além de melhorar a rastreabilidade para os módulos e documentos existentes.

## Etapa 6 - Dívida técnica, custo ou paralelismo

A opção escolhida foi **B — custo e performance**. A experiência com o `Claude Code` durante a implantação do `tdd-guard` e a execução de uma feature mostrou um custo elevado em relação ao tamanho do trecho trabalhado: a sessão consumiu aproximadamente duas horas, avançou apenas parcialmente nas tarefas e praticamente esgotou a janela de tokens disponível no período, conforme a evidência visual registrada na atividade. O tdd-guard trouxe disciplina Red-Green-Refactor e ajudou a validar os testes, mas a instrumentação, as leituras de contexto, as revisões e as várias interações necessárias para uma alteração pequena produziram um consumo desproporcional.

Esse custo deve ser separado da performance do software em produção. No agente, o problema observado foi principalmente de consumo de contexto, tempo e interações; no sistema implementado, ainda é necessário medir tempo de processamento, memória e comportamento com documentos próximos ao limite suportado.

A estratégia de otimização proposta seria aplicar o TDD-GUARD em ciclos menores e delimitados: primeiro ler apenas a especificação, os módulos diretamente envolvidos e os testes vizinhos; depois escrever um teste focado; implementar a menor mudança necessária; executar somente o teste afetado; e, por fim, rodar a suíte completa uma única vez. Checkpoints curtos, resumos persistidos em documentação e divisão de features maiores em tarefas independentes também reduzem o consumo de tokens sem remover a revisão humana ou a proteção dos testes.


## Etapa 7 - Git e GitHub

O projeto está publicado no GitHub em https://github.com/bruno774/ppgti-sdd-basics. O histórico local possui commits separados, entre eles:
(...)
- `1f1b2c3 feat: implementacao sem testes`;
- `298b3ac feat: TDD incorporado ao projeto e implementação de caso deteccao-entidades`;
- `15acc03 feat: implementar selecao-categorias-operador (tarefas 10-14)`;
- `e04d543 docs: adicionar sessao-log.md com transcrição completa da sessão`;
- `dcc4f21 docs: registrar interface web de anonimização`.

Esse histórico demonstra evolução incremental do projeto, em vez de um único commit gigante. O arquivo deste relatório registra as entregas e as lacunas observadas, sem alterar commits anteriores.

## Etapa 8 - Relatório final e checklist

Na Etapa 1, o modo de planejamento ofereceu mais controle e segurança para mudanças sensíveis, enquanto o modo automático foi mais rápido, e o guardrail da entrada multicanal bloqueou PDF incompatível e possível prompt injection.

Na Etapa 2, a investigação levou à adoção do TDD-GUARD, e a comparação mostrou que trabalhar sem testes é mais rápido, mas o TDD aumenta a confiabilidade e a rastreabilidade ao custo de mais tempo, interações e tokens.

Na Etapa 3, foi definido um checkpoint humano antes do `git push`, assumindo o papel de revisar alterações, requisitos e riscos de privacidade antes de aprovar a sincronização.

Nas Etapas 4 e 5, decidiu-se manter a aplicação modular no mesmo projeto, e o ADR 0003 e o diagrama C4 em [docs/arquitetura.md](docs/arquitetura.md) documentam essa decisão, separando responsabilidades atuais de componentes planejados.

Na Etapa 6, foi investigado o custo de contexto, tempo e tokens do Claude Code com o TDD-GUARD, e o principal aprendizado foi que ciclos menores, testes focados e menos releituras podem preservar a qualidade com maior eficiência. Precisariamos fazer outras análises mais profundas e detalhadas, e as evidências serão cruciais para adotar o modelo certo e os frameworks adequados à capacidade financeira e expectativa do projeto.

Uma dificuldade real foi distinguir o que estava efetivamente implementado e comprovado no repositório do que existia apenas como requisito ou intenção arquitetural, evitando apresentar documentação como evidência de implementação, além da necessidade de revisar código implementado com estilo e capacidades por vezes fora de conhecimento deste autor do trabalho, que permitiu um aprendizado mas também uma certa insegurança na aprovação.

### Checklist final

- [x] Comparação entre dois modos de autonomia, com tempo relativo, controle e risco percebido.
- [x] Hook funcional implementado na entrada multicanal, com bloqueio de formato PDF incompatível e possível prompt injection; testes focados adicionados, com a limitação de execução registrada para a ausência de `python-docx`.
- [ ] Evidência completa de Red-Green-Refactor e ferramenta especializada de enforcement: parcialmente atendida pelos testes e pelo checkpoint.
- [ ] Comparação documentada entre tarefa com TDD e sem TDD: reflexão registrada, sem experimento separado comprovado.
- [x] Log/transcript salvo em [docs/sessao-log.md](docs/sessao-log.md), registrando o setup do TDD-GUARD, a implementação e os resultados da sessão.
- [x] Resumo da arquitetura, ponto de acoplamento e decisão justificada.
- [x] ADR existente no diretório `docs/adr/`.
- [x] Diagrama C4 salvo em [docs/arquitetura.md](docs/arquitetura.md), com comparação qualitativa entre a primeira e a segunda versão; o arquivo ainda está pendente de commit.
- [ ] Evidência de ferramenta de análise estática da Etapa 6: não realizada; foi feita identificação técnica manual.
- [x] Repositório GitHub com histórico de commits incrementais.
- [x] Relatório final cobrindo as Etapas 1 a 8 e identificando as lacunas restantes.
