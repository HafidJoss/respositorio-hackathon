def test_flujo_completo_registro_y_triaje(client):
    resp = client.post("/usuarios", json={"dni": "40404040", "telefono": "+51 940404040"})
    assert resp.status_code == 201
    usuario_id = resp.json()["id"]

    resp = client.get(f"/usuarios/{usuario_id}")
    assert resp.status_code == 200
    assert resp.json()["dni"] == "40404040"

    resp = client.post(
        "/pacientes",
        json={
            "dni": "50505050",
            "nombres": "Marco",
            "apellidos": "Rojas",
            "edad": 40,
            "jurisdiccion_sis": "Ayacucho",
            "usuario_id": usuario_id,
            "tipo_relacion": "titular",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["ya_existia"] is False
    paciente_id = body["id"]

    resp = client.post(
        "/pacientes",
        json={
            "dni": "50505050",
            "nombres": "Marco",
            "apellidos": "Rojas",
            "edad": 40,
            "jurisdiccion_sis": "Ayacucho",
            "usuario_id": usuario_id,
            "tipo_relacion": "tutor_legal",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["ya_existia"] is True
    assert resp.json()["id"] == paciente_id

    resp = client.get("/pacientes", params={"dni": "50505050"})
    assert resp.status_code == 200

    resp = client.post(
        "/triajes",
        json={
            "paciente_id": paciente_id,
            "nombres": "Marco",
            "apellidos": "Rojas",
            "dni": "50505050",
            "edad": 40,
            "peso": 75.0,
            "talla": 1.75,
            "presion_arterial": "150/95",
            "sintomas": ["fiebre", "tos"],
            "nivel_atencion": "moderado",
        },
    )
    assert resp.status_code == 201
    triaje_id = resp.json()["id"]

    resp = client.get(f"/triajes/{triaje_id}")
    assert resp.status_code == 200
    assert resp.json()["nivel_atencion"] == "moderado"

    resp = client.get(f"/pacientes/{paciente_id}/triajes")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get(f"/usuarios/{usuario_id}/pacientes")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    resp = client.get("/sintomas-comunes")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    resp2 = client.post("/usuarios", json={"dni": "60606060", "telefono": "+51 960606060"})
    otro_usuario_id = resp2.json()["id"]
    resp = client.post(
        f"/usuarios/{otro_usuario_id}/pacientes",
        json={"paciente_id": paciente_id, "tipo_relacion": "otro"},
    )
    assert resp.status_code == 201
    assert resp.json()["usuario_id"] == otro_usuario_id


def test_triaje_inexistente_responde_404(client):
    resp = client.get("/triajes/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_triaje_con_paciente_inexistente_responde_404(client):
    resp = client.post(
        "/triajes",
        json={
            "paciente_id": "00000000-0000-0000-0000-000000000000",
            "nombres": "x",
            "apellidos": "y",
            "dni": "00000000",
            "edad": 1,
            "peso": 1,
            "talla": 1,
            "presion_arterial": "110/70",
            "sintomas": [],
            "nivel_atencion": "leve",
        },
    )
    assert resp.status_code == 404


def test_dni_invalido_responde_400(client):
    resp = client.post("/usuarios", json={"dni": "abc", "telefono": "+51 987654321"})
    assert resp.status_code == 400


def test_usuario_inexistente_responde_404(client):
    resp = client.get("/usuarios/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_paciente_no_encontrado_por_dni_responde_404(client):
    resp = client.get("/pacientes", params={"dni": "99999999"})
    assert resp.status_code == 404
