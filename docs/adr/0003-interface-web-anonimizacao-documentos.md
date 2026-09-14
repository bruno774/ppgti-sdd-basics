# ADR 0003: Interface web simples para anonimização de documentos

- **Status:** aceita
- **Data:** 2026-09-13
- **Decisores:** Bruno Silva

## Contexto

O sistema precisa oferecer um ponto de entrada simples para operadores que trabalham com documentos judiciais ou administrativos. Os canais de entrada previstos no projeto incluem arquivos PDF e DOCX, texto colado diretamente e, posteriormente, captura por extensão de navegador.

Sem uma interface web definida, cada canal poderia receber uma experiência diferente para seleção de categorias, início do processamento e apresentação dos resultados. Isso aumentaria o risco de aplicar anonimização sem confirmação do operador, duplicar regras de negócio no frontend ou expor dados pessoais em mensagens e estatísticas.

A interface também precisa comunicar o resultado do processamento de forma objetiva. Estatísticas agregadas, como quantidade de palavras, estimativa de tokens, termos anonimizados e tempo de processamento, ajudam o operador a acompanhar a execução sem exigir a exibição de valores originais em logs ou relatórios.

## Decisão

Adotar uma interface web simples, organizada em uma única página principal para o fluxo de anonimização. A página será uma camada de apresentação do backend e terá os seguintes elementos:

- **Entrada por arquivo:** controle de upload que aceite PDF pesquisável e DOCX, respeitando validação de formato, limite de tamanho e mensagens de erro definidas para a entrada multicanal.
- **Entrada textual:** campo para colagem ou digitação de texto, sem exigir o envio de um arquivo.
- **Seleção de categorias:** lista de tipos de dados pessoais e sensíveis disponíveis no catálogo, com seleção explícita antes do processamento. Deve contemplar, quando cadastrados no catálogo, nome, endereço, e-mail, RG, CPF, passaporte, outros documentos, doença, religião, cor da pele, gênero e demais categorias extensíveis.
- **Início explícito:** botão para iniciar o processamento somente depois que a entrada e a seleção de categorias forem válidas. A interface não deve iniciar captura, detecção ou anonimização implicitamente.
- **Estatísticas da execução:** área que apresente apenas métricas agregadas, incluindo número de palavras, estimativa de tokens, quantidade de termos anonimizados e tempo de processamento, além de outras métricas operacionais não sensíveis que forem definidas posteriormente.
- **Resultado e estado:** apresentação do resultado textual anonimizado, do estado da execução e de erros acionáveis, sem incluir valores originais em mensagens, estatísticas ou registros de diagnóstico.

A página deve encaminhar as operações para os componentes de entrada, detecção, seleção, mascaramento, validação e auditoria já definidos no backend. A interface não deve implementar regras próprias de reconhecimento de entidades, geração de marcadores ou persistência de mapa de reidentificação.

O catálogo de entidades permanece a fonte de verdade para os tipos exibidos, seus nomes canônicos, prefixos e níveis de sensibilidade. Categorias futuras, como passaporte ou outros documentos, devem ser adicionadas ao catálogo e disponibilizadas pela interface por meio do mesmo mecanismo extensível, sem alterar o fluxo principal da página.

## Regras de segurança e privacidade

- A seleção das categorias ocorre antes da anonimização e deve ser confirmada pelo operador.
- Detecções de baixa confiança e categorias sensíveis devem continuar sujeitas às regras de revisão humana existentes.
- Estatísticas, mensagens de erro e auditoria não podem conter texto bruto, valores de entidades ou dados que permitam reidentificação.
- A estimativa de tokens deve ser identificada como estimativa e associada ao tokenizer ou configuração utilizada quando essa informação for necessária para interpretação.
- O texto de origem deve seguir os limites de retenção e expurgo definidos para a sessão; a página não deve armazená-lo em serviços externos sem autorização explícita.
- O processamento deve preservar a distinção entre texto de origem, detecções aprovadas e resultado anonimizado.

## Alternativas consideradas

### Interfaces separadas para PDF, DOCX e texto colado

Rejeitada nesta fase. Interfaces distintas aumentariam duplicação de código e poderiam produzir comportamentos divergentes para seleção, revisão, estatísticas e auditoria. Uma página única permite reutilizar o mesmo fluxo e diferenciar apenas o controle de entrada.

### Processamento automático assim que o arquivo é selecionado

Rejeitado. O operador precisa escolher explicitamente os tipos de dados que serão anonimizados antes de qualquer substituição, conforme RF03 e a especificação 006. O início explícito também reduz processamento acidental de conteúdo confidencial.

### Exibir uma lista dos termos originais nas estatísticas

Rejeitada. Embora pudesse facilitar a conferência visual, essa opção aumentaria o risco de exposição de dados pessoais. A interface deve exibir contagens e outros agregados; a revisão das detecções deve obedecer ao fluxo autorizado e às proteções próprias dessa etapa.

### Construir uma aplicação frontend independente nesta etapa

Adiada. O projeto já prevê uma camada `src/frontend/` integrada ao backend. Uma aplicação independente poderia ser avaliada posteriormente caso surjam requisitos de distribuição, escalabilidade ou ciclos de implantação distintos, mas não é necessária para definir o fluxo inicial.

## Consequências

### Benefícios

- Oferece um fluxo único e previsível para PDF, DOCX e texto colado.
- Torna obrigatória a escolha do operador antes do processamento.
- Mantém as regras de domínio centralizadas no backend.
- Permite acompanhar volume e duração do processamento sem expor conteúdo pessoal.
- Facilita a futura inclusão de categorias do catálogo sem redesenhar a página.
- Cria uma superfície adequada para integração posterior com a extensão de navegador.

### Custos e riscos

- A página precisa tratar estados de carregamento, erro, validação, baixa confiança e resultados parciais sem vazar conteúdo.
- A estimativa de tokens pode variar conforme tokenizer, versão do modelo e configuração, portanto não deve ser interpretada como medida universal.
- A presença de muitos tipos de entidade pode tornar a seleção extensa; a interface deverá organizar o catálogo sem esconder categorias obrigatórias.
- Uploads e texto colado aumentam a necessidade de limites de tamanho, expurgo de sessão e proteção contra arquivos malformados.

## Relação com requisitos e especificações

- [RF01 — Entrada de documentos](../requisitos/requisitos-funcionais.md#rf01--entrada-de-documentos)
- [RF03 — Seleção e parametrização pelo operador](../requisitos/requisitos-funcionais.md#rf03--seleção-e-parametrização-pelo-operador)
- [RF05 — Saída](../requisitos/requisitos-funcionais.md#rf05--saída)
- [RF06 — Auditoria](../requisitos/requisitos-funcionais.md#rf06--auditoria)
- [Especificação 001 — Entrada multicanal](../especificacoes/001-entrada-multicanal/spec.md)
- [Especificação 005 — Auditoria](../especificacoes/005-auditoria/spec.md)
- [Especificação 006 — Seleção de categorias pelo operador](../especificacoes/006-selecao-categorias-operador/spec.md)

## Critérios para revisar esta decisão

Reavaliar esta ADR quando houver necessidade de múltiplas páginas ou fluxos especializados, integração com autenticação e autorização avançadas, processamento assíncrono de documentos grandes, requisitos de acessibilidade ainda não atendidos ou mudança no contrato de entrada e saída do backend.