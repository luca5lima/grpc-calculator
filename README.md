# 🧮 gRPC Calculator

Calculadora distribuída em **Python** com **gRPC** e **Protocol Buffers**. O servidor expõe as operações de **soma, subtração, multiplicação e divisão de três números**, e o cliente as consome por chamadas remotas (RPC) sobre HTTP/2.

Projeto desenvolvido como prática da disciplina de **Sistemas Distribuídos** (UFC) para estudar comunicação entre processos com gRPC.

---

## 📌 Sumário

- [Visão geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Contrato do serviço (.proto)](#-contrato-do-serviço-proto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e execução](#-instalação-e-execução)
  - [Linux / macOS](#linux--macos)
  - [Windows (PowerShell)](#windows-powershell)
  - [Windows (Prompt de Comando)](#windows-prompt-de-comando-cmd)
- [Exemplo de saída](#-exemplo-de-saída)
- [Regras das operações](#-regras-das-operações)
- [Solução de problemas](#-solução-de-problemas)
- [Conceitos praticados](#-conceitos-praticados)
- [Próximos passos](#-próximos-passos)
- [Autor](#-autor)

---

## 🔎 Visão geral

```
┌──────────────┐   Protocol Buffers sobre HTTP/2   ┌──────────────┐
│   Cliente    │ ────────────────────────────────▶ │   Servidor   │
│ (cliente.py) │ ◀──────────────────────────────── │ (servidor.py)│
└──────────────┘          localhost:50051          └──────────────┘
```

1. O cliente chama um método do *stub* gerado (ex.: `Somar`).
2. A requisição é serializada em Protocol Buffers e enviada via HTTP/2.
3. O servidor desserializa, executa a operação e serializa a resposta.
4. O cliente recebe o resultado como se tivesse chamado uma função local.

## 🛠 Tecnologias

- [Python 3.9+](https://www.python.org/)
- [gRPC](https://grpc.io/) (`grpcio`)
- [Protocol Buffers](https://protobuf.dev/) (`grpcio-tools`)

## 📁 Estrutura do projeto

```
grpc-calculator/
├── calculadora.proto            # Contrato do serviço (mensagens e métodos RPC)
├── calculadora_pb2.py           # Gerado: classes das mensagens
├── calculadora_pb2_grpc.py      # Gerado: stubs de cliente e servidor
├── servidor.py                  # Implementação do servidor gRPC
├── cliente.py                   # Cliente que consome o serviço
├── .gitignore
└── README.md
```

> Os arquivos `*_pb2.py` e `*_pb2_grpc.py` são **gerados automaticamente** a partir do `.proto` (veja o passo 4 da instalação).

## 📜 Contrato do serviço (.proto)

```proto
syntax = "proto3";

package calculadora;

service Calculadora {
  rpc Somar        (OperacaoRequest) returns (OperacaoResponse);
  rpc Subtrair     (OperacaoRequest) returns (OperacaoResponse);
  rpc Multiplicar  (OperacaoRequest) returns (OperacaoResponse);
  rpc Dividir      (OperacaoRequest) returns (OperacaoResponse);
}

message OperacaoRequest {
  double numero1 = 1;
  double numero2 = 2;
  double numero3 = 3;
}

message OperacaoResponse {
  double resultado = 1;
}
```

## ✅ Pré-requisitos

- **Python 3.9 ou superior** instalado e disponível no terminal
- **pip** (já vem com o Python)
- **Git** (para clonar o repositório)

Verifique as versões:

```bash
python --version      # no Windows
python3 --version     # no Linux/macOS
pip --version
```

## 🚀 Instalação e execução

### Linux / macOS

```bash
# 1. Clone o repositório e entre na pasta
git clone https://github.com/luca5lima/grpc-calculator.git
cd grpc-calculator

# 2. Crie o ambiente virtual
python3 -m venv venv

# 3. Ative o ambiente virtual e instale as dependências
source venv/bin/activate
pip install grpcio grpcio-tools

# 4. Gere os arquivos gRPC a partir do .proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto

# 5. Inicie o servidor (Terminal 1)
python3 servidor.py

# 6. Em OUTRO terminal (com o venv ativado), execute o cliente
source venv/bin/activate
python3 cliente.py
```

### Windows (PowerShell)

```powershell
# 1. Clone o repositório e entre na pasta
git clone https://github.com/luca5lima/grpc-calculator.git
cd grpc-calculator

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual e instale as dependências
venv\Scripts\Activate.ps1
pip install grpcio grpcio-tools

# 4. Gere os arquivos gRPC a partir do .proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto

# 5. Inicie o servidor (Terminal 1)
python servidor.py

# 6. Em OUTRO terminal, ative o venv novamente e execute o cliente
venv\Scripts\Activate.ps1
python cliente.py
```

> ⚠️ Se o PowerShell bloquear a ativação do venv com um erro sobre *execution policy*, libere apenas para a sessão atual:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```
> Depois rode `venv\Scripts\Activate.ps1` novamente.

### Windows (Prompt de Comando – CMD)

```cmd
:: 1. Clone o repositório e entre na pasta
git clone https://github.com/luca5lima/grpc-calculator.git
cd grpc-calculator

:: 2. Crie o ambiente virtual
python -m venv venv

:: 3. Ative o ambiente virtual e instale as dependências
venv\Scripts\activate.bat
pip install grpcio grpcio-tools

:: 4. Gere os arquivos gRPC a partir do .proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto

:: 5. Inicie o servidor (Terminal 1)
python servidor.py

:: 6. Em OUTRO terminal, ative o venv novamente e execute o cliente
venv\Scripts\activate.bat
python cliente.py
```

> 💡 **Dica:** o servidor precisa ficar rodando enquanto o cliente é executado. Por isso são necessários **dois terminais abertos**. Para encerrar o servidor, use `Ctrl + C`.

## 🖥 Exemplo de saída

**Terminal do servidor:**

```
Servidor gRPC iniciado na porta 50051
Pressione Ctrl+C para encerrar.
```

**Terminal do cliente:** o cliente é interativo. Ele exibe um menu, pede os três números e mostra o resultado da operação escolhida. O menu se repete até você digitar `0`.

Exemplo de divisão por zero (`10`, `0` e `5`), tratada pelo servidor:

```
Escolha a operação: 4
Informe o primeiro número: 10
Informe o segundo número: 0
Informe o terceiro número: 5

Divisão: erro (INVALID_ARGUMENT) - Divisão por zero não é permitida
```

> Se você digitar algo que não é número (por exemplo, `abc`), o cliente avisa *"Entrada inválida. Use números e ponto como separador decimal."* e volta ao menu. Use ponto, e não vírgula, nos decimais (`2.5`).

## 📐 Regras das operações

Com os números `a`, `b` e `c`, as operações são aplicadas da esquerda para a direita:

| Operação      | Cálculo        |
|---------------|----------------|
| Soma          | `a + b + c`    |
| Subtração     | `a - b - c`    |
| Multiplicação | `a * b * c`    |
| Divisão       | `a / b / c`    |

**Tratamento de erros:** se `b` ou `c` forem `0` na divisão, o servidor retorna o status gRPC `INVALID_ARGUMENT` com a mensagem *"Divisão por zero não é permitida"*, e o cliente trata a exceção `grpc.RpcError`.

## 🧯 Solução de problemas

| Problema | Causa provável | Solução |
|----------|----------------|---------|
| `ModuleNotFoundError: calculadora_pb2` | Arquivos gRPC não foram gerados | Execute o comando do passo 4 na pasta do projeto |
| `ModuleNotFoundError: grpc` | Dependências não instaladas ou venv inativo | Ative o venv e rode `pip install grpcio grpcio-tools` |
| `failed to connect to all addresses` | Servidor não está rodando | Inicie o `servidor.py` antes do cliente |
| `Address already in use` / porta ocupada | Outra instância na porta 50051 | Encerre o processo anterior ou mude a porta no servidor e no cliente |
| `python` não reconhecido (Windows) | Python fora do PATH | Reinstale marcando *"Add Python to PATH"* ou use `py -m venv venv` |
| Erro de *execution policy* no PowerShell | Política bloqueia scripts | Use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` ou use o CMD |

## 📚 Conceitos praticados

- Chamada remota de procedimentos (RPC)
- Definição de contratos com Protocol Buffers (`.proto`)
- Geração automática de código (stubs de cliente e servidor)
- Comunicação cliente-servidor sobre HTTP/2
- Comunicação unária (*unary*) do gRPC
- Tratamento de erros com códigos de status gRPC
- Servidor concorrente com `ThreadPoolExecutor`
- Cliente interativo com menu, validação de entrada e *timeout* nas chamadas

## 🔭 Próximos passos

- [x] Menu interativo no cliente (entrada de números via terminal)
- [ ] Testes automatizados com `pytest`
- [ ] Comunicação segura com TLS
- [ ] Containerização com Docker
- [ ] Variação com *streaming* (ex.: histórico de operações)

## 👨‍💻 Autor

**Lucas Lima Cavalcante**
GitHub: [@luca5lima](https://github.com/luca5lima) · LinkedIn: [Lucas Lima](https://linkedin.com/in/lucas-lima-c)