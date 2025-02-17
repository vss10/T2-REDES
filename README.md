# Diffie-Hellman Secure Chat

## Descrição

Este projeto implementa um sistema de chat seguro entre clientes e um servidor, utilizando o protocolo de troca de chaves Diffie-Hellman para garantir a segurança na troca de mensagens. O foco está na segurança das comunicações, empregando criptografia simétrica (AES) com chaves derivadas da troca Diffie-Hellman. Os desafios abordados incluem a implementação de um mecanismo seguro de troca de chaves, o gerenciamento de conexões de múltiplos clientes e a criptografia das mensagens trocadas.

## Tecnologias Utilizadas

- **Linguagem de programação**: Python 3
- **Bibliotecas/Frameworks**:
  - `socket`: para comunicação de rede.
  - `threading`: para suportar múltiplas conexões simultâneas.
  - `hashlib`: para derivação de chave usando SHA-256.
  - `pycryptodome`: para criptografia AES.

## Como Executar

### Requisitos

- Python 3.6 ou superior instalado.
- Biblioteca `pycryptodome` instalada.

### Instruções de Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/vss10/T2-REDES.git
   cd T2-REDES
   ```

2. Instale as dependências:
   ```bash
   pip install pycryptodome
   ```

3. Execute o servidor:
   ```bash
   python server.py
   ```

4. Execute o cliente:
   ```bash
   python client.py
   ```

   Ao iniciar o cliente, escolha um nome de usuário e comece a enviar mensagens. Use o comando `/server` no início da mensagem para enviá-la apenas ao servidor.

## Como Testar

1. Inicie o servidor em um terminal:
   ```bash
   python server.py
   ```

2. Inicie dois ou mais clientes em terminais diferentes:
   ```bash
   python client.py
   ```

3. Envie mensagens entre os clientes e observe como elas são exibidas em cada terminal. Teste também mensagens enviadas apenas ao servidor com o comando `/server`.

## Funcionalidades Implementadas

- Troca de chaves segura com Diffie-Hellman.
- Criptografia das mensagens usando AES no modo CBC.
- Suporte a múltiplos clientes simultaneamente.
- Comunicação direta com o servidor ou broadcast para todos os clientes.
- Identificação dos clientes por meio de usernames.

## Possíveis Melhorias Futuras

- Adicionar autenticação de clientes para evitar conexões não autorizadas.
- Suporte para mensagens privadas entre clientes específicos.
- Interface gráfica para melhorar a experiência do usuário.
- Adicionar tempos de expiração para as conexões inativas.
