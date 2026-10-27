# Cliente gRPC - Calculadora

import grpc

import calculadora_pb2
import calculadora_pb2_grpc

ENDERECO = "localhost:50051"
TIMEOUT_SEGUNDOS = 5

def executar(nome, metodo, requisicao):
    """Chama um método RPC e imprime o resultado ou o erro devolvido pelo servidor."""
    try:
        resposta = metodo(requisicao, timeout=TIMEOUT_SEGUNDOS)
        print(f"{nome}: {resposta.resultado}")
    except grpc.RpcError as erro:
        print(f"{nome}: erro ({erro.code().name}) - {erro.details()}")

def main():
    with grpc.insecure_channel(ENDERECO) as canal:
        cliente = calculadora_pb2_grpc.CalculadoraStub(canal)

        requisicao = calculadora_pb2.OperacaoRequest(
            numero1=10,
            numero2=20,
            numero3=0,
        )

        executar("Soma", cliente.Somar, requisicao)
        executar("Subtração", cliente.Subtrair, requisicao)
        executar("Multiplicação", cliente.Multiplicar, requisicao)
        executar("Divisão", cliente.Dividir, requisicao)

if __name__ == "__main__":
    main()