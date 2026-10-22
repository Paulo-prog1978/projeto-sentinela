# SENTINELA — Relatório de triagem

Case independente com empresa e dados fictícios.

Gerado em UTC: 2026-10-22T01:04:19.242746+00:00
Fonte: dados/eventos.csv
SHA-256 da fonte: aa55473d1f70bd1c5a5eabfcb6572eb0181aef66f392f394bb9b23c5ed018feb
Eventos analisados: 18
Alertas de autenticação: 1

## Critérios do laboratório

- Pelo menos 5 falhas de login em até 10 minutos antes do sucesso.
- Falhas e sucesso associados à mesma conta e ao mesmo IP.
- Correlação de atividades nos 30 minutos após o login.
- Consulta em massa: pelo menos 1.000 registros por evento.

## Caso 1 — prestador.suporte01

- Prioridade de triagem: ALTA
- IP do login: 198.51.100.25
- Login bem-sucedido: 2026-10-21T08:07:00-03:00
- Falhas anteriores na janela: 12

### Evidências de autenticação

EVT003, EVT004, EVT005, EVT006, EVT007, EVT008, EVT009, EVT010, EVT011, EVT012, EVT013, EVT014, EVT015

### Atividades posteriores relacionadas

- EVT016 | 2026-10-21T08:11:00-03:00 | concessao_privilegio | quantidade: 1 | IP: 198.51.100.25 | Conta beneficiaria recebeu perfil exportador de clientes - executor a confirmar
- EVT017 | 2026-10-21T08:15:00-03:00 | consulta_clientes | quantidade: 4800 | IP: 198.51.100.25 | Consulta em lote - autorizacao a verificar
- EVT018 | 2026-10-21T08:18:00-03:00 | criacao_exportacao | quantidade: 4800 | IP: 198.51.100.25 | Arquivo clientes_exportacao.csv criado - transferencia nao confirmada

### Avaliação inicial

A sequência exige investigação prioritária. Comprometimento da conta e transferência externa de dados ainda não estão confirmados.

### Próximas ações propostas

- Preservar os registros originais e documentar a coleta.
- Confirmar o acesso com o prestador por canal confiável.
- Identificar o executor e a autorização do privilégio.
- Verificar a justificativa da consulta e da exportação.
- Buscar evidências de download ou transferência.
- Avaliar a revogação de sessões e a suspensão temporária do acesso com o responsável pela resposta, considerando o risco de continuidade da atividade e o impacto operacional.

### Limites da análise

- Correlação por conta e tempo não comprova uma mesma sessão.
- A origem incomum consta no cenário; não foi calculada a partir de um histórico de acessos.
- A concessão de privilégio identifica a conta beneficiária; o executor permanece desconhecido.
- O hash permite comparar versões do arquivo; não comprova a autenticidade dos registros.

## Matriz de resposta proposta

As ações abaixo são recomendações para avaliação humana. O SENTINELA não executa bloqueios nem envia alertas.

| Ação | Responsável proposto | Critério e cuidado |
|---|---|---|
| Registrar o caso e preservar logs | Analista de segurança | Documentar origem, horários, evidências e decisões. |
| Confirmar o acesso por canal confiável | Segurança e gestor do prestador | Conferir identidade e atividade sem depender apenas da conta suspeita. |
| Verificar a concessão de privilégio | Equipe de identidades e acessos | Identificar executor, autorização e necessidade. |
| Avaliar revogação de sessões e suspensão temporária | Responsável pela resposta e equipe de identidades | Considerar evidências de uso indevido e dependências operacionais; registrar a decisão. |
| Investigar download ou transferência | Segurança e responsáveis pelos sistemas | Verificar destino, volume e registros disponíveis. |
| Recuperar o acesso | Segurança, identidades e gestor do serviço | Tratar a causa identificada e restaurar somente as permissões necessárias. |

Preservação e contenção podem ocorrer em paralelo. A coleta completa não deve atrasar a interrupção de uma atividade indevida em andamento.

## Critérios para a decisão humana

- Se o prestador negar o acesso: reforçar a suspeita e priorizar a avaliação de contenção.
- Se houver autorização: verificar se corresponde à conta, horário, permissão, ação e volume observados.
- Se a atividade for confirmada como legítima: documentar as evidências e a justificativa de encerramento.
- Se houver transferência externa confirmada: ampliar a avaliação de impacto e envolver privacidade e jurídico quando houver possível exposição de dados pessoais.
- Se faltarem registros: manter a incerteza explícita; ausência de registro não comprova ausência de transferência.

## Limite operacional do protótipo

Este protótipo lê um arquivo CSV local e produz um relatório. Não realiza monitoramento em tempo real, não consulta chamados, não bloqueia contas e não encaminha dados a terceiros.
