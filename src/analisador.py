import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_LOGS = PASTA_PROJETO / "dados" / "eventos.csv"

MINIMO_FALHAS = 5
JANELA = timedelta(minutes=10)


def carregar_eventos(caminho):
    """Lê os logs e organiza os eventos por horário."""
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        eventos = list(csv.DictReader(arquivo))

    for evento in eventos:
        evento["instante"] = datetime.fromisoformat(
            evento["data_hora"]
        )

    return sorted(eventos, key=lambda evento: evento["instante"])


def detectar_login_suspeito(eventos):
    """Relaciona falhas e sucesso para a mesma conta e IP."""
    falhas_por_origem = defaultdict(list)
    alertas = []

    for evento in eventos:
        if evento["acao"] != "login":
            continue

        chave = (evento["usuario"], evento["ip_origem"])
        instante = evento["instante"]

        # Mantém apenas as falhas dentro da janela de análise.
        falhas_por_origem[chave] = [
            falha
            for falha in falhas_por_origem[chave]
            if instante - falha["instante"] <= JANELA
        ]

        if evento["resultado"] == "falha":
            falhas_por_origem[chave].append(evento)

        elif evento["resultado"] == "sucesso":
            falhas = falhas_por_origem[chave]

            if len(falhas) >= MINIMO_FALHAS:
                alertas.append({
                    "usuario": evento["usuario"],
                    "ip": evento["ip_origem"],
                    "quantidade_falhas": len(falhas),
                    "horario_sucesso": evento["data_hora"],
                    "evidencias": [
                        falha["evento_id"] for falha in falhas
                    ] + [evento["evento_id"]],
                })

            # Evita reutilizar as mesmas falhas após um sucesso.
            falhas_por_origem[chave] = []

    return alertas


def main():
    eventos = carregar_eventos(ARQUIVO_LOGS)
    alertas = detectar_login_suspeito(eventos)

    print("SENTINELA — Triagem de autenticação")
    print(f"Eventos carregados: {len(eventos)}")
    print(f"Alertas encontrados: {len(alertas)}")

    for alerta in alertas:
        print("\n[ALERTA] Falhas de login seguidas de sucesso")
        print(f"Conta: {alerta['usuario']}")
        print(f"IP de origem: {alerta['ip']}")
        print(f"Falhas na janela: {alerta['quantidade_falhas']}")
        print(f"Login bem-sucedido: {alerta['horario_sucesso']}")
        print("Evidências:", ", ".join(alerta["evidencias"]))
        print("Conclusão: atividade suspeita; investigar.")
        print("O alerta não confirma comprometimento da conta.")


if __name__ == "__main__":
    main()
    