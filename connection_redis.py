from redis import Redis

r = Redis(host='localhost', port=6379, decode_responses=True)
print(r.ping())

capitulos = {
    1: "El mandaloriano",
    2: "El niño",
    3: "El pecado",
    4: "Santuario",
    5: "El pistolero",
    6: "El prisionero",
    7: "El ajuste de cuentas",
    8: "Redención",
    9: "El mariscal",
    10: "La pasajera",
    11: "La heredera",
    12: "El asedio",
    13: "La Jedi",
    14: "La tragedia",
    15: "El creyente",
    16: "El rescate",
    17: "El apóstata",
    18: "Las minas de Mandalore",
    19: "El converso",
    20: "El huérfano",
    21: "El pirata",
    22: "Pistoleros a sueldo",
    23: "Los espías",
    24: "El regreso"
}

for numero, nombre in capitulos.items():
    r.hset(f"capitulo:{numero}", mapping={
        "nombre": nombre,
        "estado": "disponible"
    })

for i in range(1, 25):
    cap = r.hgetall(f"capitulo:{i}")
    print(f"Capítulo {i}: {cap['nombre']} - {cap['estado']}")