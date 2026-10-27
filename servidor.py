# Servidor gRPC - Calculadora (soma, subtração, multiplicação e divisão de três números)

from concurrent import futures
import grpc

import calculadora_pb2
import calculadora_pb2_grpc

PORTA = 50051

class CalculadoraServicer(
    calculadora_pb2_grpc.CalculadoraServicer
):
    def Somar(self, request, context):
        result = request.numero1 + request.numero2 + request.numero3

        return calculadora_pb2.OperacaoResponse(
            resultado=result
        )

    def Subtrair(self, request, context):
        result = request.numero1 - request.numero2 - request.numero3

        return calculadora_pb2.OperacaoResponse(
            resultado=result
        )

    def Multiplicar(self, request, context):
        result = request.numero1 * request.numero2 * request.numero3

        return calculadora_pb2.OperacaoResponse(
            resultado=result
            )

    def Dividir(self, request, context):
        # Divisão: numero1 / numero2 / numero3.
        # Os divisores (numero2 e numero3) não podem ser zero.
        if request.numero2 == 0 or request.numero3 == 0:
            # abort() encerra a chamada e devolve o erro ao cliente
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Divisão por zero não é permitida",
            )

        result = request.numero1 / request.numero2 / request.numero3
        return calculadora_pb2.OperacaoResponse(
            resultado=result
        )


def servir():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(
        CalculadoraServicer(), server
    )

    server.add_insecure_port(f"localhost:{PORTA}")
    server.start()

    print(f"Servidor gRPC iniciado na porta {PORTA}")
    print("Pressione Ctrl+C para encerrar.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nEncerrando o servidor...")
        server.stop(grace=0)


if __name__ == "__main__":
    servir()