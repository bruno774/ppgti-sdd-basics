# AGENTS.md

## Descricao do projeto

Este repositorio sera usado para construir uma ferramenta de anonimização de textos juridicos e administrativos. A entrada pode ser um arquivo PDF ou TXT. A ferramenta deve identificar entidades que representem dados pessoais ou dados pessoais sensiveis, permitir que o operador escolha quais tipos serao anonimizados e produzir texto pronto para processamento por ferramentas externas.

O sistema deve preservar o sentido semantico do documento. Cada ocorrencia anonimizada deve continuar sendo processavel como uma entidade distinta, sem revelar o valor original. A solucao deve tratar anonimização como uma transformacao controlada, auditavel e reversivel apenas quando isso estiver explicitamente previsto pelo produto.


## Objetivos do produto

- Extrair texto de PDFs pesquisaveis e ler arquivos TXT.
- Detectar entidades pessoais e sensiveis com tipo, trecho, posicao e confianca.
- Permitir a selecao, pelo operador, dos tipos de entidade que serao anonimizados.
- Substituir cada entidade selecionada por um marcador consistente, seguro e semanticamente util.
- Manter entidades diferentes distinguiveis, inclusive quando pertencem ao mesmo tipo.
- Preservar acentuacao, estrutura textual relevante, paragrafos e ordem do documento sempre que possivel.
- Exportar somente texto anonimizado para integracao com ferramentas externas.
- Evitar que valores originais aparecam em logs, mensagens de erro, arquivos temporarios ou resultados de depuracao.

## Comandos (requisitos funcionais)

Como ainda nao existe uma CLI implementada, os comandos abaixo definem o contrato esperado para a futura aplicacao. Nao trate estes exemplos como comandos disponiveis ate que sejam implementados e testados.

### Inspecionar entidades

```text
anonimizador detectar --entrada documento.pdf --saida entidades.json
```

Deve ler PDF ou TXT e retornar, para cada entidade detectada, ao menos: `id`, `tipo`, `inicio`, `fim`, `texto` e `confianca`. O valor original deve ser protegido quando o arquivo for destinado a compartilhamento; uma opcao explicita e documentada pode permitir sua visualizacao apenas ao operador autorizado.

### Anonimizar por tipos escolhidos

```text
anonimizador anonimizar --entrada documento.txt --tipos NOME,CPF,ENDERECO --saida documento_anonimizado.txt
```

Deve aplicar mascaramento somente aos tipos selecionados. Entidades nao selecionadas devem permanecer inalteradas. O resultado primario deve ser texto UTF-8, sem metadados ocultos ou valores originais embutidos.

### Validar resultado

```text
anonimizador validar --entrada documento_anonimizado.txt
```

Deve verificar se o arquivo e legivel, se os marcadores seguem o esquema definido, se nao ha sobreposicao invalida e se entidades selecionadas nao permaneceram expostas de forma evidente.

### Requisitos funcionais

1. Aceitar PDF pesquisavel e TXT como entradas.
2. Informar claramente quando um PDF nao possuir camada de texto utilizavel; OCR deve ser uma capacidade separada e explicitamente configurada.
3. Identificar, no minimo, `NOME`, `CPF`, `RG`, `CID_DOENCA`, `RELIGIAO`, `GENERO_SEXUAL`, `CLASSE_SOCIAL`, `ENDERECO`, `EMAIL` e `TELEFONE`.
4. Permitir extensao do catalogo de entidades sem alterar o fluxo principal.
5. Permitir ao operador escolher tipos antes da substituicao.
6. Representar cada entidade como unidade independente, com identificador estavel durante o processamento.
7. Preservar o contexto semantico por meio de marcadores tipados, por exemplo `[NOME_001]` e `[CPF_001]`.
8. Garantir que duas pessoas ou dois documentos diferentes nao sejam confundidos por compartilharem o mesmo tipo.
9. Processar entidades da direita para a esquerda ou usar estrategia equivalente, evitando deslocamento de posicoes.
10. Produzir relatorio de contagem por tipo sem incluir dados pessoais.
11. Retornar erros acionaveis para formato invalido, arquivo ausente, PDF protegido ou texto ilegivel.
12. Ser deterministico quando receber a mesma entrada, configuracao e versao do modelo.

## Modelo de entidade e saida

Cada deteccao deve ter tipo canonico, intervalo de caracteres, confianca, identificador e origem. O sistema deve manter separadas deteccao, revisao do operador e aplicacao do mascaramento.

O formato padrao de saida e texto UTF-8. Marcadores devem ser ASCII, estaveis e facilmente reconheciveis por ferramentas externas. O mapeamento entre marcador e valor original deve ficar fora da saida anonimizada e somente existir se houver requisito de reidentificacao autorizado, com protecao adequada.

Exemplo:

```text
Requerente: [NOME_001], CPF: [CPF_001].
Contato: [EMAIL_001], telefone [TELEFONE_001].
```

Nao usar um marcador generico unico como `[REDACTED]` quando isso eliminar a capacidade de diferenciar entidades ou prejudicar o sentido do texto.

## Privacidade e seguranca

- Tratar todo documento de entrada como confidencial.
- Nao enviar documentos a servicos externos sem opt-in explicito e documentado.
- Nao registrar texto bruto, entidades originais, CPF, RG ou conteudo sensivel em logs.
- Remover ou proteger arquivos temporarios apos o processamento.
- Validar caminhos, extensoes e limites de tamanho antes da leitura.
- Manter dependencias atualizadas e revisar riscos de parsing de PDF.
- Nao prometer anonimização perfeita: baixa confianca deve ser apresentada para revisao humana.
- Diferenciar anonimização, pseudonimização e simples mascaramento na documentacao e na interface.

## Convencoes de codigo

- Usar Python 3.11 ou versao minima definida pelo projeto quando a implementacao iniciar.
- Usar nomes de variaveis, funcoes e classes descritivos; evitar nomes de uma letra.
- Preferir type hints, funcoes pequenas e responsabilidades unicas.
- Manter separadas as camadas de extracao, deteccao, revisao, substituicao e exportacao.
- Usar tipos canonicos em maiusculas no catalogo de entidades.
- Preservar offsets como intervalos `[inicio, fim)` e documentar qualquer conversao de indice.
- Ordenar substituicoes por posicao decrescente ou construir a saida por segmentos.
- Nao incluir dados pessoais reais em testes, fixtures, exemplos ou snapshots.
- Usar testes para cada tipo de entidade, casos negativos, acentuacao, sobreposicao e escolha parcial de tipos.
- Manter mensagens de erro uteis, mas sem ecoar o conteudo confidencial.
- Evitar comentarios que apenas repitam o codigo; documentar somente decisoes nao obvias.

## Testes e qualidade

Toda alteracao que afete deteccao, selecao ou mascaramento deve incluir teste focado. A validacao minima esperada e:

```text
python -m pytest
python -m compileall .
```

Quando os comandos ou dependencias ainda nao existirem, registrar essa limitacao em vez de criar resultados ficticios. Testes de integracao devem cobrir PDF e TXT, e testes de seguranca devem confirmar que valores originais nao aparecem na saida, nos logs nem nos erros.

## Nao escopo

- Decidir se o conteudo juridico e verdadeiro, valido ou juridicamente correto.
- Substituir revisao humana em deteccoes de baixa confianca.
- Fazer classificacao juridica, analise de merito ou recomendacao legal.
- Garantir OCR perfeito para PDFs digitalizados sem uma capacidade especifica.
- Indexar, vender, compartilhar ou armazenar documentos para finalidades nao autorizadas.
- Criar um sistema geral de gestao documental, workflow processual ou assinatura digital.
- Recuperar a identidade original a partir do texto anonimizado.
- Expandir para imagens, planilhas ou formatos adicionais sem requisito explicito.

## Orientacoes para agentes

Antes de editar, localizar a camada que controla diretamente o comportamento solicitado e formular uma hipotese verificavel. Fazer a menor alteracao coerente com as convencoes acima. Depois da primeira edicao, executar imediatamente o teste ou comando de validacao mais especifico disponivel.

Nao inventar dependencias, formatos de API ou garantias de privacidade. Quando uma decisao de produto estiver indefinida, preservar os dados, sinalizar a incerteza e pedir revisao do operador. Nunca fazer commit ou reverter alteracoes de outros contribuidores sem solicitacao explicita.
