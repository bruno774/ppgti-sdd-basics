# Glossário

- **Anonimização**: transformação que impede, de forma irreversível, a reidentificação do titular dos dados. Este projeto não garante anonimização irreversível completa; use este termo com a ressalva registrada na documentação e na interface.
- **Pseudo-anonimização (pseudonimização)**: substituição de um dado pessoal por um marcador ou identificador artificial, mantendo a possibilidade de reidentificação apenas por meio de informação adicional protegida e mantida separada. É a técnica principal desta ferramenta.
- **Mascaramento**: ocultação ou substituição de um valor por outro, sem necessariamente preservar a distinção entre entidades diferentes. Este projeto evita mascaramento genérico (por exemplo `[REDACTED]`) quando isso eliminar a distinção entre entidades.
- **Marcador**: token ASCII estável, tipado, no formato `prefixo + índice`, que substitui uma entidade detectada e selecionada (por exemplo `nom1`, `end1`).
- **Entidade**: ocorrência de um dado pessoal ou sensível detectada no texto, com tipo canônico, intervalo de posição, confiança e origem.
- **Tipo sensível**: categoria de dado pessoal sensível conforme a LGPD (por exemplo saúde, crença religiosa, orientação sexual, filiação, dado genético), que exige limiar de confiança mais alto e revisão humana.
- **Operador**: pessoa autorizada que usa a ferramenta, escolhe os tipos a anonimizar e revisa detecções antes da aplicação.
- **Canal de entrada**: forma pela qual o conteúdo chega ao sistema — arquivo PDF, arquivo DOCX, texto colado/clipboard ou extensão de navegador.
- **Auditoria**: registro estruturado e não editável das operações realizadas (detecção, seleção, anonimização, exportação), sem conteúdo pessoal, usado para rastreabilidade.
