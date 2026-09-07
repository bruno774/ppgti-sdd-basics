## Context

Ver [proposal.md](proposal.md). Não existe nenhum código de extensão hoje, apenas a pasta reservada `src/extension/` e `tests/extension/`. A extensão consome o backend de detecção/anonimização (capabilities `entrada-multicanal`, `deteccao-entidades`, `selecao-categorias`, `mascaramento-pseudonimizacao`), que também ainda estão em desenvolvimento.

## Goals / Non-Goals

**Goals:**
- Definir a arquitetura mínima da extensão (content script + popup/painel + comunicação com backend) e o modelo de permissões (Manifest V3).
- Definir o contrato de comunicação entre extensão e backend, reaproveitando o canal `extensao` de `entrada-multicanal`.

**Non-Goals:**
- Implementar suporte a editores de texto ricos (`contenteditable` complexos) além de `textarea`/campos de texto simples nesta primeira versão.
- Definir a UI final de seleção de categorias (reaproveita o comportamento já especificado em `selecao-categorias`; esta capability só garante que a extensão invoca esse fluxo).

## Decisions

- **Manifest V3 com `activeTab` e permissão de host apenas para o domínio configurado como backend confiável**, evitando `<all_urls>` ou permissões amplas. Alternativa considerada: permissão ampla de todas as páginas — rejeitada por violar o princípio de mínimo privilégio (RNF01).
- **Captura via content script injetado sob demanda**, não permanente, ativado apenas quando o operador aciona a extensão (por exemplo, item de menu de contexto ou clique no ícone). Alternativa considerada: content script sempre ativo em toda página — rejeitada por aumentar a superfície de captura implícita.
- **Comunicação extensão-backend via HTTP configurável pelo operador**, com validação de origem (CORS) no backend; a extensão não persiste o endpoint de backend fora das configurações padrão do navegador para extensões (sync storage da própria extensão, não do conteúdo capturado).

## Risks / Trade-offs

- [Extensões de navegador têm superfície de ataque própria: permissões excessivas, injeção de conteúdo] → Mitigação: revisão do manifesto e do content script quanto ao mínimo privilégio antes de qualquer publicação; testes automatizados de que a permissão solicitada é a mínima necessária.
- [Falha de rede pode deixar o operador sem feedback] → Mitigação: erro explícito na UI da extensão, nunca falha silenciosa (ver cenário de falha de comunicação).
