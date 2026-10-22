from datetime import datetime, timedelta

from analisador import detectar_login_suspeito


def montar_cenario(numero_falhas, minuto_sucesso):
    inicio = datetime.fromisoformat("2026-10-21T08:00:00-03:00")
    eventos = []

    for numero in range(numero_falhas):
        eventos.append({
            "evento_id": f"TESTE{numero + 1:03}",
            "usuario": "conta.teste",
            "ip_origem": "192.0.2.50",
            "acao": "login",
            "resultado": "falha",
            "instante": inicio + timedelta(seconds=numero),
        })

    sucesso = inicio + timedelta(minutes=minuto_sucesso)

    eventos.append({
        "evento_id": "SUCESSO001",
        "usuario": "conta.teste",
        "ip_origem": "192.0.2.50",
        "acao": "login",
        "resultado": "sucesso",
        "instante": sucesso,
        "data_hora": sucesso.isoformat(),
    })

    return eventos


cenarios = [
    ("4 falhas: abaixo do limite", 4, 1, 0),
    ("5 falhas: limite atingido", 5, 1, 1),
    ("5 falhas antigas: fora da janela", 5, 11, 0),
]

for descricao, falhas, minuto, esperado in cenarios:
    eventos = montar_cenario(falhas, minuto)
    quantidade = len(detectar_login_suspeito(eventos))

    assert quantidade == esperado, (
        f"{descricao}: esperado {esperado}, obtido {quantidade}"
    )

    print(f"OK — {descricao}")

print("\nValidação concluída: 3 cenários passaram.")

