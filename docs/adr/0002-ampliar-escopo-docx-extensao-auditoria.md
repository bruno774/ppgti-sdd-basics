# ADR 0002: Ampliar escopo para DOCX, texto/clipboard, extensão de navegador e auditoria

- **Status:** aceita
- **Data:** 2026-09-03
- **Decisores:** equipe do projeto

## Contexto

O escopo original ([ADR 0001](0001-stack-python-pydantic-spacy-django.md)) cobria apenas PDF e TXT como entrada, marcadores no formato `[TIPO_001]` e não previa extensão de navegador nem auditoria formal. O projeto foi ampliado para:

- aceitar PDF, DOCX, texto colado/clipboard e captura via extensão de navegador;
- usar marcadores de pseudo-anonimização curtos e em minúsculas (`nom1`, `end1`, `rel1`, `rel2`, ...);
- permitir parametrização explícita, pelo operador, das categorias de dados sensíveis a anonimizar, incluindo `COR_PELE` como novo tipo;
- registrar auditoria íntegra e não editável das operações, sem dados pessoais.

## Decisão

Manter a base definida na ADR 0001 (Python, Pydantic, Django, pytest) e adicionar:

- **python-docx:** extração de texto de arquivos DOCX, preservando parágrafos. Falhas de parsing devem gerar erro acionável, sem expor conteúdo do arquivo.
- **Extensão de navegador (WebExtensions API, Manifest V3):** implementada em JavaScript/TypeScript, com `content script` de captura mínima e comunicação com o backend via endpoint HTTP configurável pelo operador. Vive em `src/extension/`.
- **Marcadores de pseudo-anonimização:** trocar o formato `[TIPO_001]` por `prefixo + índice` em minúsculas (ver [catálogo de entidades](../requisitos/catalogo-entidades.md)), mais compacto e adequado a reprocessamento por ferramentas externas de texto simples.
- **Módulo de auditoria:** camada própria no backend Django, com modelo de dados append-only (`EventoAuditoria`), validado por Pydantic antes da persistência, garantindo que nenhum campo aceite texto livre não sanitizado.

## Organização esperada (atualizada)

```text
docs/
├── adr/                      # Decisões arquiteturais
├── requisitos/                # Requisitos funcionais, não funcionais, catálogo e glossário
└── especificacoes/            # Especificações SDD por funcionalidade

src/
├── backend/                   # Django, domínio, extração (PDF/DOCX), detecção, mascaramento, auditoria
├── frontend/                  # Interface Django de revisão e seleção do operador
└── extension/                 # Extensão de navegador (captura e devolução de texto)

tests/
├── backend/
├── frontend/
└── extension/
```

## Alternativas consideradas

### Manter marcadores `[TIPO_001]`

Mais explícito visualmente, mas o produto passou a exigir marcadores curtos e discretos (`nom1`, `rel1`, `rel2`), mais próximos de um pseudônimo textual natural. Optou-se por trocar o formato, documentando a migração nesta ADR.

### Extensão de navegador como aplicação separada fora deste repositório

Manter tudo em um único repositório simplifica o versionamento conjunto de contrato de API entre backend e extensão nesta fase inicial. Uma separação futura pode ser reavaliada se o ciclo de release da extensão divergir do backend.

### OCR habilitado por padrão para PDFs digitalizados

Rejeitado: aumentaria a superfície de processamento e o risco de exposição de dados sem necessidade comprovada; permanece como capacidade futura, opcional e explícita.

## Consequências

### Benefícios

- Cobertura de mais canais de entrada sem duplicar a lógica de detecção/mascaramento (contrato único `DocumentoOrigem`).
- Marcadores mais compactos e mais fáceis de reintegrar em texto corrido.
- Auditoria formal aumenta a rastreabilidade sem novo risco de exposição de dados pessoais.

### Custos e riscos

- Extensão de navegador introduz uma nova superfície de segurança (permissões de navegador, comunicação cross-origin) que exige revisão própria.
- Suporte a DOCX adiciona nova dependência de parsing a manter atualizada.
- Migração do formato de marcador (`[TIPO_001]` → `tipo1`) exige atualizar exemplos, testes e documentação já existentes.

## Critérios para revisar esta decisão

Reavaliar quando houver métricas de uso real da extensão de navegador, avaliação de segurança do fluxo cross-origin, e cobertura de testes de auditoria e dos novos canais de entrada.
