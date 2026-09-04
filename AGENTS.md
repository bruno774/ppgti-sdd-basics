# AGENTS.md

## Descricao do projeto

Este repositorio constroi uma ferramenta de pseudo-anonimização de textos juridicos e administrativos. A entrada pode chegar por quatro canais: arquivo PDF pesquisavel, arquivo DOCX, texto colado diretamente (campo de entrada ou clipboard) ou captura feita por uma extensao de navegador a partir de uma caixa de texto de uma pagina web. A saida e sempre texto pronto para processamento por ferramentas externas.

O sistema deve preservar o sentido semantico do documento. Cada ocorrencia anonimizada continua sendo uma entidade distinta, sem revelar o valor original. Anonimização e tratada como transformacao controlada, parametrizavel pelo operador e auditavel; nao existe reidentificacao automatica pela ferramenta padrao.

## Documentacao de referencia

Antes de implementar qualquer funcionalidade, consulte:

- [docs/requisitos/requisitos-funcionais.md](docs/requisitos/requisitos-funcionais.md) e [docs/requisitos/requisitos-nao-funcionais.md](docs/requisitos/requisitos-nao-funcionais.md);
- [docs/requisitos/catalogo-entidades.md](docs/requisitos/catalogo-entidades.md) — tipos canonicos e prefixos de marcador;
- [docs/requisitos/glossario.md](docs/requisitos/glossario.md);
- [docs/especificacoes/](docs/especificacoes/README.md) — especificacoes SDD por funcionalidade (entrada multicanal, deteccao, mascaramento, extensao de navegador, auditoria);
- [docs/adr/](docs/adr/README.md) — decisoes arquiteturais.

Qualquer alteracao de comportamento relevante deve manter essa documentacao coerente com o codigo; atualize a especificacao ou a ADR correspondente quando o comportamento mudar.

## Objetivos do produto

- Extrair texto de PDFs pesquisaveis e de arquivos DOCX; aceitar texto colado/clipboard; aceitar captura de uma extensao de navegador.
- Detectar entidades pessoais e sensiveis com tipo, trecho, posicao, confianca e origem.
- Permitir a selecao, pelo operador, dos tipos de entidade que serao anonimizados antes de qualquer substituicao.
- Substituir cada entidade selecionada por um marcador de pseudo-anonimização consistente e semanticamente util, no formato `prefixo + indice` (por exemplo `nom1`, `end1`, `rel1`, `rel2`), conforme o catalogo de entidades.
- Manter entidades diferentes distinguiveis, inclusive quando pertencem ao mesmo tipo.
- Preservar acentuacao, estrutura textual relevante, paragrafos e ordem do documento sempre que possivel.
- Exportar somente texto anonimizado para integracao com ferramentas externas, sem mapa de reidentificacao embutido.
- Registrar cada operacao relevante (deteccao, selecao, anonimizacao, exportacao) em auditoria integra, sem dados pessoais.
- Evitar que valores originais aparecam em logs, mensagens de erro, arquivos temporarios, registros de auditoria ou resultados de depuracao.

## Comandos (requisitos funcionais)

Como ainda nao existe uma CLI ou API implementada, os comandos abaixo definem o contrato esperado para a futura aplicacao. Nao trate estes exemplos como comandos disponiveis ate que sejam implementados e testados.

### Inspecionar entidades

```text
anonimizador detectar --entrada documento.pdf --saida entidades.json
```

Aceita `--entrada` como PDF, DOCX ou arquivo de texto; retorna, para cada entidade detectada, ao menos: `id`, `tipo`, `inicio`, `fim`, `texto` e `confianca`. O valor original deve ser protegido quando o arquivo for destinado a compartilhamento; uma opcao explicita e documentada pode permitir sua visualizacao apenas ao operador autorizado.

### Anonimizar por tipos escolhidos

```text
anonimizador anonimizar --entrada documento.docx --tipos NOME,CPF,ENDERECO --saida documento_anonimizado.txt
```

Aplica mascaramento somente aos tipos selecionados, usando marcadores `prefixo+indice` (ver [catalogo de entidades](docs/requisitos/catalogo-entidades.md)). Entidades nao selecionadas permanecem inalteradas. O resultado primario e texto UTF-8, sem metadados ocultos ou valores originais embutidos.

### Validar resultado

```text
anonimizador validar --entrada documento_anonimizado.txt
```

Verifica se o arquivo e legivel, se os marcadores seguem o esquema definido, se nao ha sobreposicao invalida e se entidades selecionadas nao permaneceram expostas de forma evidente.

### Consultar auditoria

```text
anonimizador auditoria listar --desde 2026-01-01 --operador op-123
```

Retorna eventos de auditoria (deteccao, selecao, anonimizacao, exportacao) sem qualquer dado pessoal, conforme [especificacao 005](docs/especificacoes/005-auditoria/spec.md).

### Requisitos funcionais

Ver a lista completa e numerada em [docs/requisitos/requisitos-funcionais.md](docs/requisitos/requisitos-funcionais.md). Resumo:

1. Aceitar PDF pesquisavel, DOCX, texto colado/clipboard e captura via extensao de navegador como entradas.
2. Informar claramente quando um PDF nao possuir camada de texto utilizavel; OCR e capacidade separada e explicitamente configurada.
3. Identificar, no minimo, `NOME`, `CPF`, `RG`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`, `ENDERECO`, `EMAIL` e `TELEFONE`.
4. Permitir extensao do catalogo de entidades sem alterar o fluxo principal.
5. Permitir ao operador escolher tipos antes da substituicao, e aprovar/rejeitar deteccoes sensiveis.
6. Representar cada entidade como unidade independente, com identificador estavel durante o processamento.
7. Preservar o contexto semantico por meio de marcadores tipados curtos, por exemplo `nom1` e `cpf1`.
8. Garantir que duas pessoas ou dois documentos diferentes nao sejam confundidos por compartilharem o mesmo tipo.
9. Processar entidades da direita para a esquerda ou usar estrategia equivalente, evitando deslocamento de posicoes.
10. Produzir relatorio de contagem por tipo sem incluir dados pessoais.
11. Retornar erros acionaveis para formato invalido, arquivo ausente, PDF/DOCX protegido ou texto ilegivel.
12. Ser deterministico quando receber a mesma entrada, configuracao e versao do modelo.
13. Registrar em auditoria integra e nao editavel cada operacao relevante, sem dados pessoais.
14. Permitir que a extensao de navegador capture uma caixa de texto somente mediante acao explicita do operador, e devolva o texto anonimizado a mesma caixa quando solicitado.

## Modelo de entidade e saida

Cada deteccao deve ter tipo canonico, intervalo de caracteres, confianca, identificador e origem. O sistema deve manter separadas deteccao, revisao do operador, aplicacao do mascaramento e auditoria.

O formato padrao de saida e texto UTF-8. Marcadores devem ser ASCII, estaveis, em minusculas, no formato `prefixo+indice` (por exemplo `nom1`, `end1`, `rel1`, `rel2`), conforme [docs/requisitos/catalogo-entidades.md](docs/requisitos/catalogo-entidades.md). O mapeamento entre marcador e valor original deve ficar fora da saida anonimizada e somente existir se houver requisito de reidentificacao autorizado, com protecao adequada.

Exemplo:

```text
Requerente: nom1, CPF: cpf1.
Contato: ema1, telefone tel1.
```

Nao usar um marcador generico unico como `[REDACTED]` quando isso eliminar a capacidade de diferenciar entidades ou prejudicar o sentido do texto.

## Privacidade e seguranca

- Tratar todo documento, texto colado ou conteudo capturado por extensao como confidencial.
- Nao enviar documentos ou conteudo capturado a servicos externos sem opt-in explicito e documentado.
- Nao registrar texto bruto, entidades originais, CPF, RG ou conteudo sensivel em logs, erros ou eventos de auditoria.
- Remover ou proteger arquivos temporarios apos o processamento.
- Validar caminhos, extensoes e limites de tamanho antes da leitura de PDF/DOCX.
- Aplicar minimo privilegio nas permissoes solicitadas pela extensao de navegador.
- Manter dependencias atualizadas e revisar riscos de parsing de PDF/DOCX.
- Nao prometer anonimização perfeita: baixa confianca deve ser apresentada para revisao humana, especialmente para tipos sensiveis (`CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `COR_PELE`, `CLASSE_SOCIAL`).
- Diferenciar anonimização, pseudonimização e simples mascaramento na documentacao e na interface.

## Convencoes de codigo

- Usar Python 3.11 ou versao minima definida pelo projeto para o backend/frontend Django; usar JavaScript/TypeScript para a extensao de navegador.
- Usar nomes de variaveis, funcoes e classes descritivos; evitar nomes de uma letra.
- Preferir type hints, funcoes pequenas e responsabilidades unicas.
- Manter separadas as camadas de extracao (multicanal), deteccao, revisao, substituicao, exportacao e auditoria.
- Usar tipos canonicos em maiusculas no catalogo de entidades e prefixos de marcador em minusculas.
- Preservar offsets como intervalos `[inicio, fim)` e documentar qualquer conversao de indice.
- Ordenar substituicoes por posicao decrescente ou construir a saida por segmentos.
- Nao incluir dados pessoais reais em testes, fixtures, exemplos ou snapshots.
- Usar testes para cada tipo de entidade, cada canal de entrada, casos negativos, acentuacao, sobreposicao e escolha parcial de tipos.
- Manter mensagens de erro uteis, mas sem ecoar o conteudo confidencial.
- Evitar comentarios que apenas repitam o codigo; documentar somente decisoes nao obvias.

## Estrutura de pastas

```text
docs/
├── adr/                      # Decisoes arquiteturais
├── requisitos/                # Requisitos funcionais, nao funcionais, catalogo de entidades e glossario
└── especificacoes/            # Especificacoes SDD por funcionalidade

src/
├── backend/                   # Extracao, deteccao, mascaramento, auditoria e API/Django
├── frontend/                  # Interface de revisao e selecao do operador
└── extension/                 # Extensao de navegador (captura e devolucao de texto)

tests/
├── backend/
├── frontend/
└── extension/
```

## Testes e qualidade

Toda alteracao que afete deteccao, selecao, mascaramento ou auditoria deve incluir teste focado. A validacao minima esperada e:

```text
python -m pytest
python -m compileall .
```

Quando os comandos ou dependencias ainda nao existirem, registrar essa limitacao em vez de criar resultados ficticios. Testes de integracao devem cobrir PDF, DOCX, texto colado e captura via extensao; testes de seguranca devem confirmar que valores originais nao aparecem na saida, nos logs, nos erros nem nos registros de auditoria.

## Nao escopo

- Decidir se o conteudo juridico e verdadeiro, valido ou juridicamente correto.
- Substituir revisao humana em deteccoes de baixa confianca, especialmente tipos sensiveis.
- Fazer classificacao juridica, analise de merito ou recomendacao legal.
- Garantir OCR perfeito para PDFs digitalizados sem uma capacidade especifica.
- Indexar, vender, compartilhar ou armazenar documentos para finalidades nao autorizadas.
- Criar um sistema geral de gestao documental, workflow processual ou assinatura digital.
- Recuperar a identidade original a partir do texto anonimizado pela ferramenta padrao.
- Expandir para imagens, planilhas ou formatos adicionais sem requisito explicito.

## Orientacoes para agentes

Antes de editar, localizar a especificacao ou requisito que controla o comportamento solicitado (ver [docs/especificacoes/](docs/especificacoes/README.md) e [docs/requisitos/](docs/requisitos/requisitos-funcionais.md)) e formular uma hipotese verificavel. Fazer a menor alteracao coerente com as convencoes acima. Depois da primeira edicao, executar imediatamente o teste ou comando de validacao mais especifico disponivel.

Nao inventar dependencias, formatos de API ou garantias de privacidade. Quando uma decisao de produto estiver indefinida, preservar os dados, sinalizar a incerteza e pedir revisao do operador. Nunca fazer commit ou reverter alteracoes de outros contribuidores sem solicitacao explicita.
