# Catálogo de entidades e marcadores

Este catálogo define os tipos canônicos de dados pessoais e sensíveis reconhecidos pela ferramenta, o prefixo do marcador de pseudo-anonimização e observações sobre risco de inferência indevida.

O marcador de cada ocorrência é formado por `prefixo` + `índice sequencial` **por tipo e por documento**, sem separador, em minúsculas, por exemplo `nom1`, `nom2`, `end1`, `rel1`, `rel2`. Duas entidades diferentes do mesmo tipo nunca compartilham o mesmo índice; a mesma entidade repetida no documento deve reutilizar o índice já atribuído a ela, preservando a distinção entre pessoas, locais ou registros diferentes.

| Tipo canônico | Prefixo do marcador | Exemplo | Observações |
|---|---|---|---|
| `NOME` | `nom` | `nom1` | Nome de pessoa física, inclui variações e apelidos referentes à mesma pessoa. |
| `CPF` | `cpf` | `cpf1` | Considerar formatos com e sem pontuação. |
| `RG` | `rg` | `rg1` | Considerar variação por órgão emissor/UF quando identificável. |
| `ENDERECO` | `end` | `end1` | Logradouro, número, complemento, CEP; manter distinção entre endereços diferentes. |
| `EMAIL` | `ema` | `ema1` | Validar formato antes de mascarar. |
| `TELEFONE` | `tel` | `tel1` | Incluir DDD/DDI quando presente. |
| `CID_DOENCA` | `cid` | `cid1` | Dado sensível de saúde; exige limiar de confiança elevado e revisão humana. |
| `RELIGIAO` | `rel` | `rel1`, `rel2` | Dado sensível; nunca inferir apenas por nome próprio, comunidade ou estereótipo. Religiões diferentes citadas no mesmo documento recebem índices diferentes (`rel1`, `rel2`, ...). |
| `GENERO_SEXUAL` | `gen` | `gen1` | Dado sensível; exige evidência textual explícita, não inferência por nome ou pronome isolado. |
| `COR_PELE` | `cor` | `cor1` | Dado sensível de raça/cor; exige evidência textual explícita e revisão humana obrigatória. |
| `CLASSE_SOCIAL` | `cls` | `cls1` | Dado sensível; evitar inferência por bairro, profissão ou renda presumida sem menção direta. |

## Extensibilidade

Novos tipos podem ser adicionados ao catálogo sem alterar o fluxo principal de detecção, seleção ou mascaramento, desde que:

- recebam um tipo canônico em maiúsculas e um prefixo de marcador único, curto e ainda não utilizado;
- definam nível de sensibilidade (`comum` ou `sensível`) e, se sensível, limiar mínimo de confiança;
- possuam testes cobrindo caso positivo, negativo e ambíguo antes de entrarem em uso.

## Regras gerais de sensibilidade

- Tipos sensíveis (`CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) exigem confiança mínima mais alta que tipos comuns e devem ser sinalizados para revisão do operador antes da aplicação, mesmo quando o tipo estiver selecionado para anonimização.
- Nenhum tipo sensível deve ser inferido exclusivamente por estereótipo, nome próprio, localização geográfica ou associação indireta; é necessária evidência textual explícita no trecho analisado.
- O operador pode selecionar qualquer subconjunto do catálogo antes da anonimização; tipos não selecionados permanecem no texto sem alteração.
