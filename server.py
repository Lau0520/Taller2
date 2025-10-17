import os
import grpc
from concurrent import futures
import greeter_pb2_grpc as pb2_grpc
import greeter_pb2 as pb2

def make_greeting(name: str) -> str:
    """Generate the greeting message used by both gRPC and HTTP layers."""
    return f"Hola, {name}! Bienvenido a gRPC con Protocol Buffers."

class Greeter(pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return pb2.HelloReply(message=make_greeting(request.name))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # 👇 Escucha en todas las interfaces (para ngrok y red)
    port = os.getenv("PORT", "50051")
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.start()
    print("✅ Servidor gRPC escuchando en 0.0.0.0:50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
