from flask import Flask, jsonify
from redis import Redis

app = Flask(__name__)
r = Redis(host='localhost', port=6379, decode_responses=True)
print(r.ping())

def cargar_datos():
    if r.exists("capitulo:1"):
        return
    
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

@app.route('/capitulos', methods=['GET'])
def listar_capitulos():
    resultado = []
    for i in range(1, 25):
        cap = r.hgetall(f"capitulo:{i}")

        key_reserva = f"reserva:{i}"

        if cap["estado"] == "reservado" and not r.exists(key_reserva):
            r.hset(f"capitulo:{i}", "estado", "disponible")
            cap["estado"] = "disponible"

        resultado.append({
            "numero": i,
            "nombre": cap.get("nombre"),
            "estado": cap.get("estado")
        })

    return jsonify(resultado)

@app.route('/reservar/<int:id>', methods=['POST'])
def reservar(id):
    key_cap = f"capitulo:{id}"
    key_reserva = f"reserva:{id}"

    cap = r.hgetall(key_cap)

    if not cap:
        return {"error": "No existe"}, 404

    if cap["estado"] != "disponible":
        return {"error": "No disponible"}, 400

    r.set(key_reserva, "reservado", ex=240)

    r.hset(key_cap, "estado", "reservado")

    return {"mensaje": "Capítulo reservado por 4 minutos"}

if __name__ == '__main__':
    cargar_datos()
    app.run(debug=True)