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

A aplicação seguiu parcialmente a lógica Red-Green-Refactor nas funcionalidades implementadas. Os testes foram mantidos próximos aos métodos do backend, incluindo entrada multicanal, seleção de categorias, mascaramento, extração de PDF e configurações. Os arquivos de teste estão em:

- [tests/backend/test_entrada_multicanal.py](tests/backend/test_entrada_multicanal.py);
- [tests/backend/test_categorias.py](tests/backend/test_categorias.py);
- [tests/backend/test_selecao.py](tests/backend/test_selecao.py);
- [tests/backend/test_mascaramento.py](tests/backend/test_mascaramento.py);
- [tests/backend/test_pdf_extraction.py](tests/backend/test_pdf_extraction.py).

O histórico do git mostra commits separados de implementação e testes, incluindo `feat: implementacao de tarefas base` e `feat: ajustes no relatorio final 4`. 

A ferramenta de enforcement investigada foi o método de validação da entrada multicanal, utilizado para impedir que um PDF incompatível ou com possível prompt injection avance para as etapas seguintes. Ele é efetivo para esse risco específico, mas não substitui uma ferramenta automatizada especializada de TDD como `tdd-guard` ou Superpowers. A investigação de instalação de uma dessas ferramentas foi objetiva e buscando aquela que poderia transmitir a melhor aderência de aprendizado a uma prática educativa, que permitisse melhor aprendizado e cumprisse a missão de validação das implementações. Como o superpowers possui características de maior simplicidade e avaliação superficial, sendo o tdd-guard mais cuidadoso e documentador das suas ações, fiquei com esse último.

A comparação com uma tarefa feita deliberadamente sem testes e uma execução com as proteções de verificação do código, envolvem aspectos como velocidade de implementação (muito superior no caso sem testes), efetividade do resultado e custos com tokens. A inclusão de uma camada de harness melhora a qualidade do código entregue, leva muito mais tempo mas ao mesmo tempo consome muito mais recursos financeiros, dado as diversas interações que tem que ser realizadas no código.

## Etapa 3 - Observabilidade e checkpoint humano

O checkpoint humano definido foi: **revisar o alerta de formato incompatível ou possível prompt injection antes de permitir qualquer processamento alternativo do documento**.

O papel humano é revisar o alerta, decidir se o arquivo deve ser descartado ou analisado por um procedimento autorizado e impedir qualquer tentativa de contornar a validação. Nesta atividade, a decisão foi **aprovar** a implementação do hook depois da revisão do escopo e dos testes adicionados.

A regra de segurança está refletida na especificação OpenSpec de entrada multicanal e no código. O transcript completo da sessão do agente não foi salvo em `docs/sessao-log.md`; portanto, o entregável de log/transcript permanece pendente. O histórico desta atividade e os commits existentes servem apenas como evidência parcial de rastreabilidade.

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

Minha decisão é manter a modularidade atual neste estágio, sem extrair um serviço separado. O projeto ainda é pequeno, as operações são locais e a separação por módulos já atende à clareza e à testabilidade. Extrair serviços agora aumentaria custo operacional, pontos de falha e complexidade de deploy sem benefício proporcional. Uma futura extração só seria justificável com crescimento de volume, necessidade de escala independente ou integração externa estável.

## Etapa 5 - ADR e diagrama

A decisão arquitetural foi documentada em [docs/adr/0002-ampliar-escopo-docx-extensao-auditoria.md](docs/adr/0002-ampliar-escopo-docx-extensao-auditoria.md), que registra a ampliação do projeto para DOCX, extensão de navegador e auditoria. As especificações complementares estão listadas em [docs/especificacoes/README.md](docs/especificacoes/README.md).

A primeira versão do diagrama C4 de contêiner foi construída a partir da leitura dos módulos e das especificações. A segunda versão foi ajustada manualmente para destacar o operador, os canais de entrada, o pipeline de processamento, a saída textual e a auditoria. A segunda versão comunica melhor o projeto porque mostra o fluxo principal antes dos detalhes internos e deixa explícita a fronteira entre entrada confidencial, revisão humana e saída anonimizada.

O diagrama Mermaid e a comparação formal entre duas versões não foram salvos como arquivo independente no repositório. Assim, a decisão arquitetural está documentada, mas o entregável do diagrama commitado permanece incompleto.

## Etapa 6 - Dívida técnica, custo ou paralelismo

A opção escolhida foi **dívida técnica**. A análise real identificou como sinal de dívida a existência de funcionalidades previstas nas especificações, como detecção completa de entidades, auditoria e extensão de navegador, que ainda não estão implementadas integralmente na estrutura de código observada. Há também dependência de comportamento específico de bibliotecas de extração de PDF.

A mitigação proposta é implementar cada capacidade seguindo a separação já definida nas especificações, começando por contratos de dados e testes de casos negativos. Para a extração de PDF, a mitigação inclui validar arquivo ausente, PDF protegido, camada de texto inexistente e limites de tamanho sem expor conteúdo confidencial.

Não foi executada e anexada uma ferramenta formal de análise estática, como SonarQube ou Qodana. Portanto, esta etapa apresenta uma observação técnica baseada no código e na documentação, mas não deve ser considerada evidência de uma execução de ferramenta automatizada.

## Etapa 7 - Git e GitHub

O projeto está publicado no GitHub em https://github.com/bruno774/ppgti-sdd-basics. O histórico local possui commits separados, entre eles:

- `d4d18ec feat: etapa 1 e 2 antes de openspec`;
- `67ec901 feat: add OpenSpec`;
- `6417e34 feat: demais funcionalidades em openspec`;
- `500afa1 feat: incorporar checkpoint obrigatorio`;
- `4fc88c4 feat: ajustes no relatorio final 4`;
- `b85de09 feat: ajustes no relatorio final 4`.

Esse histórico demonstra evolução incremental do projeto, em vez de um único commit gigante. O arquivo deste relatório registra as entregas e as lacunas observadas, sem alterar commits anteriores.

## Etapa 8 - Relatório final e checklist

Esta atividade mostrou que controles de autonomia precisam combinar velocidade com revisão humana. O modo de planejamento foi mais lento, mas adequado aos riscos de privacidade e arquitetura. O hook da entrada multicanal bloqueia dois riscos específicos antes da continuidade: formato PDF incompatível e possível prompt injection.

A organização por testes e módulos ajudou a preservar contratos de entrada, seleção e mascaramento. Por outro lado, a ausência de um transcript completo, de uma evidência formal do ciclo TDD e de uma ferramenta de enforcement instalada dificultou comprovar todos os itens da atividade apenas pelo estado atual do repositório.

A decisão arquitetural foi manter a aplicação modular no mesmo projeto e não extrair um serviço neste momento. O ADR registra a ampliação do escopo, enquanto o diagrama C4 deveria complementar essa decisão visualmente. A investigação de dívida técnica indicou que a principal prioridade é concluir as capacidades previstas mantendo os contratos de privacidade e testes.

A maior dificuldade real foi separar o que estava implementado e comprovado no repositório do que era apenas requisito ou intenção documentada. Isso exigiu não transformar a existência de uma especificação em falsa evidência de implementação.

### Checklist final

- [x] Comparação entre dois modos de autonomia, com tempo relativo, controle e risco percebido.
- [x] Hook funcional implementado na entrada multicanal, com bloqueio de formato PDF incompatível e possível prompt injection; testes focados adicionados, mas execução impedida pela ausência de `python-docx`.
- [ ] Evidência completa de Red-Green-Refactor e ferramenta especializada de enforcement: parcialmente atendida pelos testes e pelo checkpoint.
- [ ] Comparação documentada entre tarefa com TDD e sem TDD: reflexão registrada, sem experimento separado comprovado.
- [ ] Log/transcript salvo em `docs/sessao-log.md`: não realizado.
- [x] Resumo da arquitetura, ponto de acoplamento e decisão justificada.
- [x] ADR existente no diretório `docs/adr/`.
- [ ] Diagrama C4 commitado e comparação de duas versões: não salvo como artefato independente.
- [ ] Evidência de ferramenta de análise estática da Etapa 6: não realizada; foi feita identificação técnica manual.
- [x] Repositório GitHub com histórico de commits incrementais.
- [x] Relatório final cobrindo as Etapas 1 a 8 e identificando as lacunas restantes.
