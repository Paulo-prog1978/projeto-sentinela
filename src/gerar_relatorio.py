from datetime import datetime, timezone
from hashlib import sha256

from analisador import (
    ARQUIVO_LOGS,
    PASTA_PROJETO,
    carregar_eventos,
    detectar_login_suspeito,
)
from correlacionar import correlacionar


def main():
    # Confere se a fonte permaneceu igual durante a leitura.
    hash_antes = sha256(ARQUIVO_LOGS.read_bytes()).hexdigest()
    eventos = carregar_eventos(ARQUIVO_LOGS)
    hash_depois = sha256(ARQUIVO_LOGS.read_bytes()).hexdigest()

    if hash_antes != hash_depois:
        raise RuntimeError(
            "O arquivo de logs mudou durante a leitura. Execute novamente."
        )

    alertas = detectar_login_suspeito(eventos)
    gerado_em = datetime.now(timezone.utc)

    linhas = [
        "# SENTINELA — Relatório de triagem",
        "",
        "Case independente com empresa e dados fictícios.",
        "",
        f"Gerado em UTC: {gerado_em.isoformat()}",
        f"Fonte: dados/{ARQUIVO_LOGS.name}",
        f"SHA-256 da fonte: {hash_depois}",
        f"Eventos analisados: {len(eventos)}",
        f"Alertas de autenticação: {len(alertas)}",
        "",
        "## Critérios do laboratório",
        "",
        "- Pelo menos 5 falhas de login em até 10 minutos antes do sucesso.",
        "- Falhas e sucesso associados à mesma conta e ao mesmo IP.",
        "- Correlação de atividades nos 30 minutos após o login.",
        "- Consulta em massa: pelo menos 1.000 registros por evento.",
        "",
    ]

    for numero, alerta in enumerate(alertas, start=1):
        relacionados = correlacionar(eventos, alerta)
        acoes = {evento["acao"] for evento in relacionados}

        conjunto_prioritario = {
            "concessao_privilegio",
            "consulta_clientes",
            "criacao_exportacao",
        }

        prioridade = (
            "ALTA"
            if conjunto_prioritario.issubset(acoes)
            else "A AVALIAR"
        )

        linhas.extend([
            f"## Caso {numero} — {alerta['usuario']}",
            "",
            f"- Prioridade de triagem: {prioridade}",
            f"- IP do login: {alerta['ip']}",
            f"- Login bem-sucedido: {alerta['horario_sucesso']}",
            f"- Falhas anteriores na janela: {alerta['quantidade_falhas']}",
            "",
            "### Evidências de autenticação",
            "",
            ", ".join(alerta["evidencias"]),
            "",
            "### Atividades posteriores relacionadas",
            "",
        ])

        for evento in relacionados:
            linhas.append(
                f"- {evento['evento_id']} | {evento['data_hora']} | "
                f"{evento['acao']} | quantidade: {evento['quantidade']} | "
                f"IP: {evento['ip_origem']} | {evento['detalhe']}"
            )

        linhas.extend([
            "",
            "### Avaliação inicial",
            "",
            "A sequência exige investigação prioritária. "
            "Comprometimento da conta e transferência externa "
            "de dados ainda não estão confirmados.",
            "",
            "### Próximas ações propostas",
            "",
            "- Preservar os registros originais e documentar a coleta.",
            "- Confirmar o acesso com o prestador por canal confiável.",
            "- Identificar o executor e a autorização do privilégio.",
            "- Verificar a justificativa da consulta e da exportação.",
            "- Buscar evidências de download ou transferência.",
            "- Avaliar a revogação de sessões e a suspensão temporária "
            "do acesso com o responsável pela resposta, considerando "
            "o risco de continuidade da atividade e o impacto operacional.",
            "",
            "### Limites da análise",
            "",
            "- Correlação por conta e tempo não comprova uma mesma sessão.",
            "- A origem incomum consta no cenário; não foi calculada "
            "a partir de um histórico de acessos.",
            "- A concessão de privilégio identifica a conta beneficiária; "
            "o executor permanece desconhecido.",
            "- O hash permite comparar versões do arquivo; "
            "não comprova a autenticidade dos registros.",
            "",
        ])
    linhas.extend([
        "## Matriz de resposta proposta",
        "",
        "As ações abaixo são recomendações para avaliação humana. "
        "O SENTINELA não executa bloqueios nem envia alertas.",
        "",
        "| Ação | Responsável proposto | Critério e cuidado |",
        "|---|---|---|",
        "| Registrar o caso e preservar logs | Analista de segurança | "
        "Documentar origem, horários, evidências e decisões. |",
        "| Confirmar o acesso por canal confiável | Segurança e gestor "
        "do prestador | Conferir identidade e atividade sem depender "
        "apenas da conta suspeita. |",
        "| Verificar a concessão de privilégio | Equipe de identidades "
        "e acessos | Identificar executor, autorização e necessidade. |",
        "| Avaliar revogação de sessões e suspensão temporária | "
        "Responsável pela resposta e equipe de identidades | "
        "Considerar evidências de uso indevido e dependências "
        "operacionais; registrar a decisão. |",
        "| Investigar download ou transferência | Segurança e "
        "responsáveis pelos sistemas | Verificar destino, volume "
        "e registros disponíveis. |",
        "| Recuperar o acesso | Segurança, identidades e gestor "
        "do serviço | Tratar a causa identificada e restaurar "
        "somente as permissões necessárias. |",
        "",
        "Preservação e contenção podem ocorrer em paralelo. "
        "A coleta completa não deve atrasar a interrupção "
        "de uma atividade indevida em andamento.",
        "",
        "## Critérios para a decisão humana",
        "",
        "- Se o prestador negar o acesso: reforçar a suspeita "
        "e priorizar a avaliação de contenção.",
        "- Se houver autorização: verificar se corresponde à conta, "
        "horário, permissão, ação e volume observados.",
        "- Se a atividade for confirmada como legítima: documentar "
        "as evidências e a justificativa de encerramento.",
        "- Se houver transferência externa confirmada: ampliar "
        "a avaliação de impacto e envolver privacidade e jurídico "
        "quando houver possível exposição de dados pessoais.",
        "- Se faltarem registros: manter a incerteza explícita; "
        "ausência de registro não comprova ausência de transferência.",
        "",
        "## Limite operacional do protótipo",
        "",
        "Este protótipo lê um arquivo CSV local e produz um relatório. "
        "Não realiza monitoramento em tempo real, não consulta chamados, "
        "não bloqueia contas e não encaminha dados a terceiros.",
        "",
    ])
    
    pasta_saida = PASTA_PROJETO / "relatorios"
    pasta_saida.mkdir(exist_ok=True)

    nome = gerado_em.strftime("triagem_%Y%m%dT%H%M%S_%fZ.md")
    destino = pasta_saida / nome
    destino.write_text("\n".join(linhas), encoding="utf-8")

    print(f"Relatório salvo em: {destino}")
    print(f"Alertas documentados: {len(alertas)}")


if __name__ == "__main__":
    main()
    