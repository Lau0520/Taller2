# Taller SD - Ejercicio 2: gRPC + Protocol Buffers (Greeter)

## Descripción
Este proyecto implementa un ejemplo de comunicación remota usando **gRPC** y **Protocol Buffers** en Python.  
El cliente envía su nombre al servidor, y este responde con un saludo generado remotamente.

---

##  Estructura del proyecto
```
TALLER SD2/
├── greeter.proto          # contrato (IDL) en formato Protocol Buffers
├── greeter_pb2.py         # generado automáticamente
├── greeter_pb2_grpc.py    # generado automáticamente
├── server.py              # implementación del servidor gRPC
└── client.py              # cliente que invoca el método remoto
```

---

## Paso 1 - Generar los archivos del protocolo (.proto → .py)
Desde la carpeta del proyecto donde está `greeter.proto` se ejecuta:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greeter.proto
```

Esto crea automáticamente los archivos `greeter_pb2.py` y `greeter_pb2_grpc.py`.

---

## Paso 2 - Ejecutar la aplicación en la misma máquina

### Terminal 1 — Servidor
```bash
python server.py
```
Salida:
```
 Servidor gRPC escuchando en :50051 ... (Ctrl+C para detener)
```

### Terminal 2 — Cliente
```bash
python client.py
```
```
¿Cómo te llamas? Laura
 Respuesta del servidor: ¡Hola, Laura! Bienvenido a gRPC con Protocol Buffers.
```

### PASOS CON NGROK

### Terminal 1 — servidor

```bash
python server.py
```
### terminal 2
primero en la terminal donde esta ngrok se coloca: 

```bash
ngrok tcp 50051
```
para poder abrir el puerto y se vera algo asi:
    Servidor gRPC escuchando en 0.0.0.0:50051

### terminal 3

```bash
python client.py 2.tcp.ngrok.io:18844
```
Lo que aparece:

Conectando a: 2.tcp.ngrok.io:18844
¿Cómo te llamas? Laura
Respuesta: Hola, Laura! Bienvenido a gRPC con Protocol Buffers

---

## Despliegue en Render (exponer por Internet)

Render no expone puertos TCP arbitrarios; para publicar fácilmente este proyecto, añadimos una pequeña capa HTTP con FastAPI que llama a la misma lógica de saludo. Así podrás acceder con HTTPS desde cualquier cliente (curl/navegador/Postman) sin necesidad de gRPC.

### Archivos añadidos
- `app.py`: servicio HTTP con FastAPI (`GET /hello`, `POST /hello`).
- `requirements.txt`: dependencias para el runtime.
- `render.yaml`: blueprint para crear el servicio en Render.

El servidor gRPC original (`server.py`) sigue funcionando para uso local/NGROK. Se refactorizó la lógica de saludo en `make_greeting(name)` para reutilizarla en HTTP y gRPC.

### Pasos para desplegar en Render
1) Sube este repo a GitHub/GitLab.
2) Entra a render.com → New → Blueprint → conecta tu repo y selecciona `render.yaml`.
3) Acepta los valores por defecto. Render instalará `requirements.txt` y arrancará con:
   `uvicorn app:app --host 0.0.0.0 --port $PORT`.
4) Cuando el deploy termine, obtendrás una URL pública `https://<tu-servicio>.onrender.com`.

### Probar en producción
- GET:
  `curl "https://<tu-servicio>.onrender.com/hello?name=Laura"`

- POST:
  `curl -X POST "https://<tu-servicio>.onrender.com/hello" -H "Content-Type: application/json" -d '{"name":"Laura"}'`

Respuesta esperada:
```
{"message":"Hola, Laura! Bienvenido a gRPC con Protocol Buffers."}
```

### Nota sobre gRPC nativo en Internet
Si necesitas exponer gRPC nativo públicamente, opciones típicas son:
- Usar NGROK (como ya muestras en esta guía).
- Usar una plataforma que soporte gRPC directamente (p. ej., Cloud Run) o colocar un proxy gRPC-Web (Envoy) delante del servidor.



