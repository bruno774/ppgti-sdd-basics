# ADR 0001: Adotar Python, Pydantic, pypdf, spaCy e Django

- **Status:** proposta
- **Data:** 2026-08-24
- **Decisores:** equipe do projeto

> **Nota:** o escopo de entrada e o formato do marcador de pseudo-anonimização descritos aqui foram ampliados/alterados pela [ADR 0002](0002-ampliar-escopo-docx-extensao-auditoria.md) (DOCX, texto/clipboard, extensão de navegador, marcadores `prefixo+indice` e auditoria).

## Contexto

O sistema precisa processar documentos jurídicos e administrativos em PDF ou TXT, detectar entidades pessoais e sensíveis, permitir a revisão e a escolha dos tipos pelo operador e gerar texto anonimizado para ferramentas externas.

A arquitetura deve favorecer contratos explícitos entre extração, detecção, revisão, mascaramento e exportação. Também deve permitir validação rigorosa de entradas, preservar offsets e reduzir o risco de exposição de dados pessoais em logs, erros e artefatos temporários.

## Decisão

Adotar Python como linguagem principal e organizar o sistema em camadas com responsabilidades separadas:

- **Python:** linguagem da aplicação, da detecção, das regras de mascaramento e dos testes.
- **Pydantic:** modelos tipados e validação de contratos de entrada e saída, incluindo entidades com `id`, `tipo`, `inicio`, `fim`, `confianca` e `origem`. Os modelos não devem registrar nem expor valores originais por padrão.
- **Django:** framework web da aplicação, responsável pelo backend HTTP, pela interface de operação, pela apresentação de documentos e detecções, pela seleção dos tipos e pela solicitação do mascaramento. A aplicação não deve enviar documentos a serviços externos sem autorização explícita.
- **pypdf:** extração de texto de PDFs pesquisáveis. PDF sem camada de texto deve produzir uma mensagem acionável; OCR não será habilitado implicitamente.
- **spaCy:** biblioteca local de NLP para apoiar o reconhecimento de entidades e o processamento contextual de texto. Modelos e componentes devem ser avaliados por precisão, desempenho, licença e privacidade antes de serem adotados em produção.
- **TXT:** usar as APIs padrão do Python com codificação UTF-8, respeitando limites de tamanho e validação de caminho.
- **Pytest:** framework de testes unitários e de integração, incluindo testes de segurança que confirmem a ausência de valores originais na saída, nos logs e nos erros.

As dependências deverão ser registradas e instaladas por meio de `requirements.txt`, mantidas atualizadas e revisadas quanto a vulnerabilidades e licenças.

## Organização esperada

```text
src/
├── backend/              # Django, domínio, extração, detecção e mascaramento
└── frontend/             # Interface Django de revisão do operador

tests/
├── backend/              # Testes de domínio, API e processamento de arquivos
└── frontend/             # Testes da interface e do fluxo de seleção
```

A camada de domínio deve permanecer independente das views e dos endpoints Django sempre que possível. A saída principal será texto UTF-8 com marcadores tipados, como `[NOME_001]` e `[CPF_001]`; o mapeamento de reidentificação não pertence à saída padrão.

## Alternativas consideradas

### Separar frontend e backend em aplicações diferentes

Uma separação em aplicações web distintas poderia isolar a interface e o processamento, mas aumentaria a complexidade operacional e os pontos de comunicação. Foi escolhido Django como aplicação web única neste estágio, com separação interna entre domínio, endpoints e templates.

### Flask em vez de Django

Flask é uma alternativa madura e simples, mas Django oferece estrutura integrada para interface, rotas, formulários, autenticação e proteção contra requisições indevidas. A troca só deve ocorrer por requisito operacional ou de compatibilidade comprovado.

### Framework JavaScript no frontend

Um frontend JavaScript separado poderia oferecer uma experiência mais rica, porém adicionaria uma aplicação e uma cadeia de dependências adicionais. Django atende ao frontend previsto neste estágio e mantém o processamento sob controle do backend Python.

### Modelos remotos ou serviços externos de detecção

Não serão usados por padrão, pois poderiam enviar documentos confidenciais para fora do ambiente autorizado. Qualquer exceção exige opt-in explícito, documentação, avaliação de risco e aprovação do operador.

## Consequências

### Benefícios

- Contratos de dados centralizados e validados com Pydantic.
- Backend web e interface integrados no ecossistema Django.
- Interface operacional separada da lógica de anonimização.
- Extração de PDF baseada em `pypdf` e processamento NLP local com spaCy.
- Ecossistema Python adequado à extração, processamento de texto e testes.
- Possibilidade de ampliar o catálogo de entidades sem alterar o fluxo principal.

### Custos e riscos

- A aplicação Django concentra mais responsabilidades e exige separação rigorosa entre web e domínio.
- Bibliotecas de parsing de PDF exigem atualização e testes contra arquivos malformados.
- Modelos NLP podem aumentar o consumo de memória e gerar falsos positivos ou falsos negativos.
- Pydantic valida estrutura, mas não garante que uma detecção seja semanticamente correta; baixa confiança continua exigindo revisão humana.
- A escolha de bibliotecas de NLP ou modelos locais ainda depende de testes de precisão, desempenho, licença e privacidade.

## Critérios para revisar esta decisão

Reavaliar a arquitetura quando houver implementação funcional e métricas sobre:

- precisão e cobertura da detecção por tipo de entidade;
- tempo e memória para PDFs e TXTs dentro dos limites suportados;
- segurança no tratamento de documentos e arquivos temporários;
- complexidade operacional de manter o backend e o frontend no Django;
- cobertura de testes e facilidade de auditoria das substituições.
