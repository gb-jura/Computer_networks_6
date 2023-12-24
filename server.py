import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Dictionary to store blocked users for each client
block_list = {}

# Sending Messages To All Connected Clients
def broadcast(message, sender=None):
    for client in clients:
        if sender is None or client != sender:
            client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.startswith('/block'):
                parts = message.split(' ')
                if len(parts) == 2:
                    blocked_user = parts[1]
                    block_list.setdefault(client, []).append(blocked_user)
                    client.send(f'Вы заблокировали пользователя {blocked_user}'.encode('ascii'))
                else:
                    client.send('Использование: /block <никнейм>'.encode('ascii'))
            elif message.startswith('/unblock'):
                parts = message.split(' ')
                if len(parts) == 2:
                    blocked_user = parts[1]
                    if blocked_user in block_list.get(client, []):
                        block_list.get(client, []).remove(blocked_user)
                        client.send(f'Вы разблокировали пользователя {blocked_user}'.encode('ascii'))
                    else:
                        client.send(f'Пользователь {blocked_user} не был заблокирован'.encode('ascii'))
                else:
                    client.send('Использование: /unblock <никнейм>'.encode('ascii'))
            else:
                for other_client in clients:
                    if other_client != client and (block_list.get(other_client) is None or client not in block_list.get(other_client)):
                        other_client.send(message.encode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        block_list[client] = []  # Initialize the block list for this client
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), client)
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server if listening...")
receive()