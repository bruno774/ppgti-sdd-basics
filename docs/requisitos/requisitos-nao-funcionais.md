# Requisitos não funcionais

## RNF01 — Privacidade e segurança

- Tratar todo documento, texto colado ou conteúdo capturado por extensão como confidencial por padrão.
- Não enviar conteúdo do operador a serviços externos (nuvem, modelos remotos, APIs de terceiros) sem opt-in explícito, documentado e visível ao operador no momento do uso.
- Nunca registrar texto bruto, entidades originais ou conteúdo sensível em logs, mensagens de erro, arquivos temporários, métricas ou eventos de auditoria.
- Validar caminhos, extensões de arquivo, tamanho máximo e integridade estrutural antes de processar PDF ou DOCX.
- Remover ou proteger arquivos temporários imediatamente após o processamento.
- Aplicar o princípio de mínimo privilégio na extensão de navegador: solicitar acesso apenas às páginas e campos necessários para a operação explicitamente iniciada pelo operador.
- Revisar dependências de terceiros (parsing de PDF/DOCX, NLP, framework web) quanto a vulnerabilidades conhecidas antes de atualizações relevantes.

## RNF02 — Determinismo e auditabilidade

- A mesma entrada, configuração e versão do sistema deve produzir a mesma detecção e o mesmo mascaramento.
- Toda operação relevante (detecção, seleção, anonimização, exportação) deve ser auditável sem exigir acesso ao conteúdo original.
- O sistema deve permitir diferenciar claramente anonimização, pseudo-anonimização e simples mascaramento na documentação e na interface, evitando prometer garantias que a técnica aplicada não oferece.

## RNF03 — Usabilidade

- A seleção de tipos de entidade pelo operador deve ser possível em poucos passos, com valores padrão sensatos e reversíveis antes da aplicação final.
- Mensagens de erro devem ser claras e acionáveis, sem expor conteúdo confidencial.
- O fluxo de extensão de navegador deve deixar explícito ao operador qual caixa de texto será capturada antes de qualquer envio de dados.

## RNF04 — Desempenho

- O processamento de um documento dentro dos limites de tamanho suportados deve ser concluído em tempo compatível com uso interativo (segundos, não minutos), sem bloquear a interface do operador.
- A extensão de navegador não deve travar a página host durante a captura ou o retorno do texto anonimizado.

## RNF05 — Portabilidade e formatos

- A saída padrão é texto UTF-8, sem metadados ocultos, macros ou valores originais embutidos.
- Marcadores de pseudo-anonimização devem ser ASCII, estáveis e facilmente reconhecíveis por ferramentas externas de processamento de texto.

## RNF06 — Manutenibilidade

- Separar claramente as camadas de extração, detecção, revisão do operador, mascaramento, exportação e auditoria.
- Permitir a extensão do catálogo de entidades e dos canais de entrada sem alterar o fluxo principal.
- Manter cobertura de testes para cada tipo de entidade, cada canal de entrada, casos negativos, acentuação, sobreposição e seleção parcial de tipos.

## RNF07 — Conformidade

- Alinhar o tratamento de dados pessoais e sensíveis aos princípios da LGPD (Lei nº 13.709/2018), em especial necessidade, finalidade, minimização e segurança, sem que este projeto substitua avaliação jurídica formal de conformidade.
