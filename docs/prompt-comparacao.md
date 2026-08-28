
Na experiência de um prompt fraco, resumido e sem contexto ("elabore um método para leitura de arquivos PDF e retorne o seu conteúdo em texto para o método chamador"), o método gerado inclui 3 tratamentos de exceções, num método único e poucos critérios de validação (tamanho, extensão e proteção no PDF). Método simples e direto em 48 linhas.

No prompt mais robusto, com contexto, critérios explícitos e detalhes de implementação, arquitetura e segurança, foi gerado um código com validação de tamanho, assinatura de formato, integridade e legibilidade, identificação de idioma, conteúdo digitalizado e criptografado, sem manter o resultado em arquivo e com os testes implementados.

O modelo usado foi o gpt-5.6 terra, nos testes com modelo mais simples, foi usado o Raptor mini.