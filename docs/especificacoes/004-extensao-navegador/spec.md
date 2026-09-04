# Especificação 004 — Extensão de navegador

## Objetivo

Permitir que o operador capture o conteúdo de uma caixa de texto em uma página web por meio de uma extensão de navegador, envie esse conteúdo para detecção e anonimização, e opcionalmente devolva o texto anonimizado à mesma caixa de texto.

## Escopo

Incluído:

- Ação explícita do operador (por exemplo, clique em botão da extensão ou item de menu de contexto) para capturar o conteúdo de um campo de texto específico da página.
- Envio do conteúdo capturado ao backend de detecção/anonimização, sob o mesmo contrato de entrada do canal `extensao` (ver especificação 001).
- Exibição, dentro da extensão, das entidades detectadas e da seleção de tipos antes da aplicação (reaproveitando o fluxo de RF03).
- Opção de copiar ou inserir o texto anonimizado de volta na caixa de texto de origem.

Fora de escopo:

- Captura automática ou em segundo plano, sem ação explícita do operador.
- Envio de dados para domínios ou serviços não configurados explicitamente como backend confiável do operador.
- Suporte a todo e qualquer tipo de campo de página (por exemplo editores ricos baseados em `contenteditable` complexos) na primeira versão; o suporte inicial cobre `textarea` e campos de texto simples.

## Cenários

- **Dado** uma página com uma caixa de texto, **quando** o operador aciona a extensão sobre esse campo, **então** a extensão captura apenas o conteúdo daquele campo, sem acessar outras partes da página.
- **Dado** o conteúdo capturado, **quando** enviado ao backend configurado, **então** a extensão exibe as entidades detectadas e permite ao operador selecionar os tipos a anonimizar antes de prosseguir.
- **Dado** um texto anonimizado retornado pelo backend, **quando** o operador confirma a devolução, **então** a extensão substitui ou complementa o conteúdo da caixa de texto original, conforme escolha do operador.
- **Dado** o operador sem permissão concedida para o domínio atual, **quando** tenta acionar a extensão, **então** a extensão solicita a permissão de forma explícita, sem falhar silenciosamente.
- **Dado** uma falha de comunicação com o backend, **quando** ocorre, **então** a extensão exibe um erro claro ao operador, sem expor o conteúdo capturado em console ou log persistente.

## Contratos de dados

- Reaproveita `DocumentoOrigem` (especificação 001) com `canal = "extensao"` e `identificador_origem` referente ao campo capturado (por exemplo um seletor ofuscado, nunca o conteúdo).
- Comunicação entre a extensão e o backend deve ocorrer por um endpoint configurável pelo operador, com validação de origem (CORS/CSP) e sem armazenamento de conteúdo no lado da extensão além da sessão em memória.

## Critérios de aceite

- A extensão nunca envia conteúdo de página sem ação explícita do operador.
- O manifesto da extensão solicita apenas as permissões mínimas necessárias (acesso à aba ativa e ao domínio autorizado).
- Nenhum conteúdo capturado é persistido em `localStorage`, `IndexedDB` ou logs do navegador além da sessão em memória necessária para exibir o resultado.
- Testes cobrem: captura de campo simples, ausência de permissão, falha de rede e devolução do texto anonimizado ao campo de origem.

## Riscos e não-escopo

- Extensões de navegador têm superfície de ataque própria (permissões excessivas, injeção de conteúdo); revisar o manifesto e o código de conteúdo (`content script`) quanto ao princípio de mínimo privilégio.
- Esta especificação não cobre integração com editores de texto ricos de terceiros sem requisito explícito adicional.
