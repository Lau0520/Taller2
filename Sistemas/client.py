import sys
import grpc

try:
    # When running as a package: python -m Sistemas.client
    from . import greeter_pb2 as pb2
    from . import greeter_pb2_grpc as pb2_grpc
except ImportError:
    # When running from within the folder Sistemas
    import greeter_pb2 as pb2
    import greeter_pb2_grpc as pb2_grpc


def run():
    # Si no das argumentos, usa localhost
    target = sys.argv[1] if len(sys.argv) > 1 else "localhost:50051"
    print(f"Conectando a: {target}")
    channel = grpc.insecure_channel(target)
    stub = pb2_grpc.GreeterStub(channel)
    name = input("¿Cómo te llamas? ")
    response = stub.SayHello(pb2.HelloRequest(name=name))
    print("Respuesta del servidor:", response.message)


if __name__ == "__main__":
    run()

