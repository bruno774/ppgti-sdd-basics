## 1. Contrato de dados

- [ ] 1.1 Modelar `EntidadeDetectada` (id, tipo, inicio, fim, texto, confianca, origem, sensivel) com validação Pydantic e verificar com teste que instâncias válidas e inválidas (offsets negativos, confiança fora de 0-1) são tratadas corretamente
- [ ] 1.2 Definir interface comum de detector (`detectar(texto) -> list[EntidadeDetectada]`) e verificar com teste que um detector de exemplo implementa a interface corretamente

## 2. Detectores por regra (tipos com formato regular)

- [ ] 2.1 Implementar detector de `CPF` (formatos com e sem pontuação) e verificar com teste positivo, negativo e de posição correta
- [ ] 2.2 Implementar detector de `EMAIL` e verificar com teste positivo e negativo
- [ ] 2.3 Implementar detector de `TELEFONE` (com e sem DDD/DDI) e verificar com teste positivo e negativo
- [ ] 2.4 Implementar detector de `RG` e verificar com teste positivo e negativo

## 3. Detectores contextuais (tipos que exigem NLP/heurística)

- [ ] 3.1 Implementar detector de `NOME` e verificar com teste que reconhece nomes de pessoa e não gera falso positivo para palavras comuns capitalizadas
- [ ] 3.2 Implementar detector de `ENDERECO` e verificar com teste positivo e negativo
- [ ] 3.3 Implementar detectores dos tipos sensíveis (`CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`) marcando sempre `sensivel = true`, e verificar com teste que cada um rejeita inferência por estereótipo (caso ambíguo não gera detecção)
- [ ] 3.4 Verificar com teste que duas entidades sensíveis diferentes do mesmo tipo (ex.: duas religiões distintas) geram duas detecções com intervalos de posição distintos

## 4. Orquestração e limiar de confiança

- [ ] 4.1 Implementar orquestrador que executa todos os detectores registrados sobre um texto e agrega os resultados, verificando com teste que a saída combina detecções de múltiplos tipos sem duplicação
- [ ] 4.2 Aplicar limiar de confiança configurável para tipos não sensíveis e garantir que tipos sensíveis sempre retornam `sensivel = true` independentemente da confiança, verificando com teste dedicado
- [ ] 4.3 Verificar com teste de determinismo que duas execuções do orquestrador sobre o mesmo texto e configuração produzem exatamente as mesmas detecções

## 5. Extensibilidade

- [ ] 5.1 Verificar com teste que registrar um novo detector para uma categoria customizada do catálogo (`selecao-categorias`) não exige alterar o orquestrador existente

## 6. Validação final

- [ ] 6.1 Rodar `python -m pytest` e `python -m compileall .` e registrar o resultado
- [ ] 6.2 Revisar manualmente cada cenário da spec `deteccao-entidades` confirmando que existe teste cobrindo o cenário
