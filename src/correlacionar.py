from datetime import datetime, timedelta

from analisador import (
    ARQUIVO_LOGS,
    carregar_eventos,
    detectar_login_suspeito,
)


JANELA_CORRELACAO = timedelta(minutes=30)
LIMITE_CONSULTA = 1000


def correlacionar(eventos, alerta):
    inicio = datetime.fromisoformat(alerta["horario_sucesso"])
    fim = inicio + JANELA_CORRELACAO
    relacionados = []

    for evento in eventos:
        mesma_conta = evento["usuario"] == alerta["usuario"]
        dentro_da_janela = inicio < evento["instante"] <= fim

        if not (mesma_conta and dentro_da_janela):
            continue

        if evento["resultado"] != "sucesso":
            continue

        acao = evento["acao"]

        if acao == "concessao_privilegio":
            relacionados.append(evento)

        elif acao == "consulta_clientes":
            if int(evento["quantidade"]) >= LIMITE_CONSULTA:
                relacionados.append(evento)

        elif acao == "criacao_exportacao":
            relacionados.append(evento)

    return relacionados


def main():
    eventos = carregar_eventos(ARQUIVO_LOGS)
    alertas = detectar_login_suspeito(eventos)

    print("SENTINELA — Correlação de atividades")
    print(f"Alertas de autenticação: {len(alertas)}")

    for alerta in alertas:
        relacionados = correlacionar(eventos, alerta)

        print(f"\nConta investigada: {alerta['usuario']}")
        print(f"Login suspeito: {alerta['horario_sucesso']}")
        print(f"Eventos posteriores relacionados: {len(relacionados)}")

        for evento in relacionados:
            print(
                f"\n{evento['evento_id']} | "
                f"{evento['data_hora']} | "
                f"{evento['acao']}"
            )
            print(f"IP registrado: {evento['ip_origem']}")
            print(f"Detalhe: {evento['detalhe']}")

        acoes = {evento["acao"] for evento in relacionados}
        sequencia_completa = {
            "concessao_privilegio",
            "consulta_clientes",
            "criacao_exportacao",
        }

        if sequencia_completa.issubset(acoes):
            print("\nPRIORIDADE DE TRIAGEM: ALTA")
            print(
                "Justificativa: login suspeito seguido de privilégio, "
                "consulta em massa e criação de exportação."
            )
        else:
            print("\nAvaliar os eventos encontrados e o contexto da conta.")

        print("\nPendências de investigação:")
        print("- Confirmar o acesso com o prestador por canal confiável.")
        print("- Identificar quem concedeu o privilégio e sua autorização.")
        print("- Verificar a justificativa da consulta e da exportação.")
        print("- Buscar registros de download ou transferência do arquivo.")
        print("\nA transferência externa de dados permanece não confirmada.")


if __name__ == "__main__":
    main()
    