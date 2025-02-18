# Chat Seguro

## Descrição
Este projeto implementa um chat seguro baseado em criptografia AES e troca de chaves Diffie-Hellman. O servidor gerencia as conexões dos clientes e a troca de mensagens criptografadas. O cliente permite que os usuários enviem e recebam mensagens protegidas.

## Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Bibliotecas:**
  - `socket` para comunicação em rede
  - `threading` para manuseio de múltiplas conexões
  - `hashlib` para derivar chaves seguras
  - `os` para geração de IVs aleatórios
  - `tkinter` para a interface gráfica do chat
  - `pycryptodome` para criptografia AES

## Como Executar

### Requisitos
- Python 3 instalado
- Dependências listadas no arquivo `requirements.txt`

### Instruções de Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/vss10/T2-REDES.git
   cd T2-REDES
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o servidor:
   ```bash
   python server.py
   ```

4. Inicie o cliente:
   ```bash
   python client.py
   ```

## Como Testar
- Execute o servidor.
- Abra múltiplas instâncias do cliente e conecte-se.
- Envie mensagens entre os clientes e verifique a criptografia e a troca segura de mensagens.
- Caso a mensagem inicie com `/server` essa mensagem será enviada somente ao servidor.

## Funcionalidades Implementadas
- Troca segura de chaves usando Diffie-Hellman.
- Comunicação criptografada com AES-128 (modo CBC).
- Interface gráfica para interação com o chat.
- Suporte a múltiplos clientes simultâneos.
- Identificação de usuário via username.
- Comunicação direta com o servidor ou broadcast para todos os clientes.

## Possíveis Melhorias Futuras
- Melhorar a segurança com chaves maiores para Diffie-Hellman.
- Implementar autenticação para evitar ataques de intermediário (MITM).
- Adicionar suporte a conexões seguras via TLS.
- Melhorar a interface gráfica com mais funcionalidades (ex: envio de arquivos, emojis).
- Suporte para mensagens privadas entre usuários.
- Adicionar tempo de expiração para contas inativas.

