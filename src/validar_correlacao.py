from datetime import timedelta

from analisador import (
    ARQUIVO_LOGS,
    carregar_eventos,
    detectar_login_suspeito,
)
from correlacionar import correlacionar


def verificar(descricao, obtido, esperado):
    if obtido != esperado:
        raise AssertionError(
            f"{descricao}: esperado {esperado}, obtido {obtido}"
        )

    print(f"OK — {descricao}")


def main():
    eventos = carregar_eventos(ARQUIVO_LOGS)
    alertas = detectar_login_suspeito(eventos)

    verificar("Base contém um alerta de autenticação", len(alertas), 1)
    alerta = alertas[0]

    relacionados = correlacionar(eventos, alerta)
    verificar(
        "Cenário original relaciona as três evidências",
        [evento["evento_id"] for evento in relacionados],
        ["EVT016", "EVT017", "EVT018"],
    )

    # Outra conta não deve ser associada ao login investigado.
    outra_conta = [evento.copy() for evento in eventos]

    for evento in outra_conta:
        if evento["evento_id"] in {"EVT016", "EVT017", "EVT018"}:
            evento["usuario"] = "outra.conta"

    verificar(
        "Atividades de outra conta são excluídas",
        len(correlacionar(outra_conta, alerta)),
        0,
    )

    # Move as atividades para além dos 30 minutos após o login.
    fora_da_janela = [evento.copy() for evento in eventos]

    for evento in fora_da_janela:
        if evento["evento_id"] in {"EVT016", "EVT017", "EVT018"}:
            evento["instante"] += timedelta(hours=1)
            evento["data_hora"] = evento["instante"].isoformat()

    verificar(
        "Atividades fora da janela são excluídas",
        len(correlacionar(fora_da_janela, alerta)),
        0,
    )

    abaixo_do_limite = [evento.copy() for evento in eventos]

    for evento in abaixo_do_limite:
        if evento["evento_id"] == "EVT017":
            evento["quantidade"] = "999"

    verificar(
        "Consulta de 999 registros é excluída",
        [
            evento["evento_id"]
            for evento in correlacionar(abaixo_do_limite, alerta)
        ],
        ["EVT016", "EVT018"],
    )

    print("\nValidação concluída: 5 verificações passaram.")

    # Exercício: os mesmos eventos podem ter contexto legítimo.
    contexto_simulado = {
        "chamado": "CHG-LAB-001",
        "acesso_confirmado": True,
        "privilegio_autorizado": True,
        "exportacao_autorizada": True,
    }

    print("\nEXERCÍCIO — Atividade autorizada")
    print("Contexto fictício fornecido para discussão:")
    print(contexto_simulado)

    print(
        "\nA regra continua encontrando as mesmas três atividades:",
        len(correlacionar(eventos, alerta)),
    )
    print(
        "Ela não consulta chamados nem verifica autorizações."
    )
    print(
        "O analista deve validar o chamado, a identidade, os horários "
        "e o escopo da autorização antes de encerrar o alerta."
    )


if __name__ == "__main__":
    main()
    