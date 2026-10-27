# Cliente gRPC

import grpc

import calculadora_pb2
import calculadora_pb2_grpc

with grpc.insecure_channel("localhost:50051") as canal:
    cliente = calculadora_pb2_grpc.CalculadoraStub(canal)

    requisicao = calculadora_pb2.OperacaoRequest(
        numero1=30,
        numero2=20
    )

    resposta_soma = cliente.Somar(requisicao)

    print("Soma:", resposta_soma.resultado)