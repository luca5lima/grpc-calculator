# Cliente gRPC - Calculadora

import grpc

import calculadora_pb2
import calculadora_pb2_grpc

ENDERECO = "localhost:50051"
TIMEOUT_SEGUNDOS = 5

def executar(nome, metodo, requisicao):
    # Chama um método RPC e imprime o resultado ou o erro devolvido pelo servidor.
    try:
        resposta = metodo(requisicao, timeout=TIMEOUT_SEGUNDOS)
        print(f"\n{nome}: {resposta.resultado}")
    except grpc.RpcError as erro:
        print(f"\n{nome}: erro ({erro.code().name}) - {erro.details()}")

def main():
    with grpc.insecure_channel(ENDERECO) as canal:
        cliente = calculadora_pb2_grpc.CalculadoraStub(canal)

        operacoes = {
            "1": ("Soma", cliente.Somar),
            "2": ("Subtração", cliente.Subtrair),
            "3": ("Multiplicação", cliente.Multiplicar),
            "4": ("Divisão", cliente.Dividir),
        }

        while True:
            print("\n1 - Soma\n2 - Subtração\n3 - Multiplicação\n4 - Divisão\n0 - Sair")
            opcao = input("Escolha a operação: ").strip()
            if opcao == "0":
                break
            if opcao not in operacoes:
                print("\nOpção inválida.")
                continue

            try:
                a = float(input("Informe o primeiro número: "))
                b = float(input("Informe o segundo número: "))
                c = float(input("Informe o terceiro número: "))
            except ValueError:
                print("\nEntrada inválida. Use números e ponto como separador decimal.")
                continue

            requisicao = calculadora_pb2.OperacaoRequest(
                numero1=a, 
                numero2=b, 
                numero3=c
            )

            nome, metodo = operacoes[opcao]
            executar(nome, metodo, requisicao)

if __name__ == "__main__":
    main()