# Taller SD2 – gRPC + Protocol Buffers + FastAPI (Greeter)

## Descripción
Ejemplo de comunicación remota con gRPC y Protocol Buffers en Python. El cliente envía su nombre al servidor, y este responde con un saludo. Además, se incluye una capa HTTP con FastAPI para exponer el servicio por Internet (Render).

---

## Estructura del proyecto
```
Taller SD2/
├─ Sistemas/
│  ├─ greeter.proto            # Contrato (IDL) Protocol Buffers
│  ├─ greeter_pb2.py           # Generado automáticamente
│  ├─ greeter_pb2_grpc.py      # Generado automáticamente
│  ├─ server.py                # Servidor gRPC
│  ├─ client.py                # Cliente gRPC
│  ├─ app.py                   # Capa HTTP (FastAPI)
│  └─ readme2.md               # Este archivo
└─ render.yaml                 # Blueprint de Render (rootDir: Sistemas)
```

---

## Paso 1 – Generar los .py desde el .proto
Desde la carpeta `Sistemas`:

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greeter.proto
```

Esto crea `greeter_pb2.py` y `greeter_pb2_grpc.py`.
Si falta el comando, instala: `python -m pip install grpcio-tools`.

---

## Paso 2 – Ejecutar localmente (gRPC)

- Opción A (desde la raíz):
  - Servidor: `python -m Sistemas.server`
  - Cliente: `python -m Sistemas.client`

- Opción B (desde la carpeta Sistemas):
  - Servidor: `python server.py`
  - Cliente: `python client.py`

Salida típica del servidor:
```
Servidor gRPC escuchando en 0.0.0.0:50051
```

---

## Paso 3 – Exponer gRPC con NGROK (opcional)
En una terminal: `python -m Sistemas.server`
En otra: `ngrok tcp 50051`
Luego, cliente contra la URL de ngrok, por ejemplo:

```
python -m Sistemas.client 2.tcp.ngrok.io:18844
```

---

## Capa HTTP con FastAPI (para Render)
Para publicar fácilmente en Internet, se incluye `Sistemas/app.py` con rutas:
- GET `/hello?name=TuNombre`
- POST `/hello` con body `{ "name": "TuNombre" }`

Ejecución local:
```
uvicorn Sistemas.app:app --reload --port 8000
# http://localhost:8000/hello?name=Laura
```

---

## Despliegue en Render
Render no expone puertos TCP crudos; por eso se usa FastAPI/HTTP.

1) Sube este repo a GitHub/GitLab.
2) En Render: New → Blueprint → conecta tu repo y selecciona `render.yaml` (raíz, apunta a `rootDir: Sistemas`).
3) Render instalará `Sistemas/requirements.txt` y arrancará:
   `uvicorn app:app --host 0.0.0.0 --port $PORT` (dentro de `Sistemas`).
4) Al terminar, tendrás una URL pública `https://<tu-servicio>.onrender.com`.

Probar en producción:
```
curl "https://<tu-servicio>.onrender.com/hello?name=Laura"
curl -X POST "https://<tu-servicio>.onrender.com/hello" -H "Content-Type: application/json" -d '{"name":"Laura"}'
```

Respuesta esperada:
```
{"message":"Hola, Laura! Bienvenido a gRPC con Protocol Buffers."}
```

---

## Notas
- Si necesitas gRPC nativo público, usa NGROK o una plataforma que soporte gRPC (p. ej., Cloud Run), o un proxy gRPC‑Web (Envoy).
- El servidor gRPC respeta la variable de entorno `PORT` si está definida.
