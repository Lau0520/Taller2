# Taller SD2 – Proyecto en carpeta `Sistemas`

Este repositorio contiene un ejemplo gRPC (con capa HTTP vía FastAPI para Render).

- Documentación completa: `Sistemas/readme2.md`
- Código fuente: carpeta `Sistemas/`
- Despliegue (Render): `render.yaml` en la raíz con `rootDir: Sistemas`

Atajos rápidos
- Servidor gRPC (desde raíz): `python -m Sistemas.server`
- Cliente gRPC (desde raíz): `python -m Sistemas.client`
- HTTP local: `uvicorn Sistemas.app:app --reload --port 8000`

