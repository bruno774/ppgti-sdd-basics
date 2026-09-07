## 1. Manifesto e permissões mínimas

- [ ] 1.1 Criar `manifest.json` (Manifest V3) em `src/extension/` com `activeTab` e permissão de host restrita ao domínio configurável do backend, e verificar manualmente que nenhuma permissão além do necessário é solicitada
- [ ] 1.2 Escrever teste (unitário ou de configuração) que falha caso o manifesto declare uma permissão de host mais ampla que o domínio configurado

## 2. Captura explícita de campo

- [ ] 2.1 Implementar content script que só captura o conteúdo de um campo quando acionado explicitamente (ex.: clique no ícone da extensão com o campo em foco) e verificar com teste que nenhuma captura ocorre sem essa ação
- [ ] 2.2 Implementar identificação do campo capturado (seletor ofuscado, nunca o conteúdo) para compor o `identificador_origem` do canal `extensao` (capability `entrada-multicanal`)

## 3. Comunicação com o backend

- [ ] 3.1 Implementar envio do conteúdo capturado ao backend configurado, respeitando o contrato do canal `extensao`, e verificar com teste (mock de rede) que o payload enviado está correto
- [ ] 3.2 Implementar tratamento de falha de comunicação com mensagem de erro visível ao operador, verificando com teste que nenhum conteúdo capturado é logado no console em caso de falha

## 4. Seleção de categorias e devolução do resultado

- [ ] 4.1 Implementar exibição das entidades detectadas e do fluxo de seleção de categorias (reaproveitando `selecao-categorias`) na UI da extensão, verificando com teste de interface que a seleção é enviada corretamente ao backend
- [ ] 4.2 Implementar devolução do texto anonimizado ao campo de origem (substituir ou complementar, conforme escolha do operador), verificando com teste que o conteúdo do campo é atualizado corretamente

## 5. Persistência e segurança

- [ ] 5.1 Verificar com teste que nenhum conteúdo capturado é persistido em `localStorage`, `IndexedDB` ou armazenamento sincronizado da extensão além da sessão em memória

## 6. Validação final

- [ ] 6.1 Rodar a suíte de testes de `tests/extension/` (ferramenta a definir conforme a stack de extensão escolhida) e registrar o resultado
- [ ] 6.2 Revisar manualmente cada cenário da spec `extensao-navegador` confirmando que existe teste cobrindo o cenário
