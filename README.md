# SENTINELA — Triagem de eventos de segurança

Protótipo em Python para identificar falhas de autenticação seguidas
de sucesso, correlacionar atividades sensíveis e gerar um relatório
para apoiar a investigação.

**Autor:** Paulo Henrique de Oliveira

Case independente com empresa, contas e dados fictícios.
Não utiliza dados ou sistemas da Vivo.

## Problema

Uma operadora fictícia identifica tentativas de login malsucedidas,
seguidas de acesso bem-sucedido, concessão de privilégio, consulta
em massa e criação de uma exportação.

O desafio é organizar as evidências e apoiar a decisão de resposta,
considerando o risco e o impacto operacional.

## Funcionalidades

- Leitura de eventos de um arquivo CSV.
- Detecção de pelo menos 5 falhas de login nos 10 minutos
  anteriores a um sucesso, para a mesma conta e IP.
- Correlação de atividades da mesma conta nos 30 minutos
  posteriores ao login suspeito.
- Identificação de concessão de privilégio, consulta de pelo menos
  1.000 registros por evento e criação de exportação.
- Prioridade alta quando os três tipos de atividade estão presentes.
- Relatório Markdown com evidências e ações propostas.
- Registro do hash SHA-256 do arquivo analisado.

Os limites são parâmetros do laboratório e precisam de avaliação
antes de qualquer aplicação operacional.

## Tecnologias

- Python.
- Bibliotecas padrão: csv, collections, datetime, pathlib e hashlib.
- Sem dependências externas nesta versão.

## Estrutura

| Caminho | Finalidade |
|---|---|
| dados/eventos.csv | Eventos simulados |
| src/analisador.py | Detecção de autenticação suspeita |
| src/correlacionar.py | Correlação de atividades |
| src/gerar_relatorio.py | Geração do relatório |
| src/validar_regra.py | Validação da regra de autenticação |
| src/validar_correlacao.py | Validação da correlação |
| relatorios/ | Relatórios gerados |
| docs/ | Documentação complementar |

## Como executar no Windows PowerShell

Ambiente utilizado no desenvolvimento: Python 3.14.5.

Abra o terminal na pasta principal do projeto.

Crie o ambiente virtual, caso ainda não exista:

```powershell
python -m venv .venv
```

Execute a detecção:

```powershell
.\.venv\Scripts\python.exe .\src\analisador.py
```

Execute a correlação:

```powershell
.\.venv\Scripts\python.exe .\src\correlacionar.py
```

Gere o relatório:

```powershell
.\.venv\Scripts\python.exe .\src\gerar_relatorio.py
```

O relatório será salvo em relatorios, com um nome baseado
na data e hora de geração em UTC.

## Validações

```powershell
.\.venv\Scripts\python.exe .\src\validar_regra.py
.\.venv\Scripts\python.exe .\src\validar_correlacao.py
```

Foram executadas 3 verificações da regra de autenticação
e 5 verificações da correlação e de sua base de entrada.

Também há um exercício de atividade autorizada que demonstra
a necessidade de conferir o contexto do alerta.

Essas verificações não medem precisão ou taxa de falsos positivos
em um ambiente real.

## Resultado da base simulada

- 18 eventos analisados.
- 1 alerta de autenticação.
- 12 falhas anteriores ao login bem-sucedido.
- 3 atividades posteriores relacionadas.
- Prioridade de triagem alta.

A consulta e a exportação registram 4.800 registros cada.
Esses volumes não devem ser somados como clientes únicos.

## Decisão e resposta

O relatório propõe preservação de evidências, confirmação do acesso,
verificação de autorizações, investigação de transferências
e avaliação de contenção direcionada.

As decisões dependem de avaliação humana e dos responsáveis
pela resposta e pelo serviço.

## Limitações

- Analisa um CSV local; não monitora em tempo real.
- Não bloqueia contas nem envia informações a terceiros.
- Não utiliza inteligência artificial.
- Não consulta chamados ou autorizações.
- Não calcula se um IP é habitual.
- Correlação por conta e tempo não comprova uma mesma sessão.
- Não verifica automaticamente a ordem entre as três atividades
  posteriores; verifica sua presença na janela.
- A detecção inicial exige falhas e sucesso no mesmo IP.
- A análise das atividades depende da existência do alerta de login.
- A entrada deve seguir o formato do CSV fornecido;
  o tratamento de arquivos inválidos ainda é limitado.
- O hash permite comparar arquivos, mas não comprova autenticidade.
- A criação da exportação não confirma transferência ou vazamento.

## Melhorias propostas

- Ampliar os testes de limites e de qualidade dos dados.
- Identificar ator, conta beneficiária e sessão em campos separados.
- Validar a ordem das atividades quando exigida pela regra.
- Detectar atividades sensíveis independentemente do alerta de login.
- Comparar acessos com um histórico de comportamento.
- Avaliar integração com gestão de incidentes e autorizações.
