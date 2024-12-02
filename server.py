import socket
from threading import Thread
from queue import Queue

# Queue to manage matchmaking
match_queue = Queue()

def handle_game(player1, player2):
    try:
        player1.send(b"You're paired! Send your choice (rock, paper, scissors): ")
        choice1 = player1.recv(1024).decode('utf-8').strip().lower()

        player2.send(b"You're paired! Send your choice (rock, paper, scissors): ")
        choice2 = player2.recv(1024).decode('utf-8').strip().lower()

        # Determine the winner
        outcomes = {
            ('rock', 'scissors'): "Player 1 wins!",
            ('scissors', 'paper'): "Player 1 wins!",
            ('paper', 'rock'): "Player 1 wins!",
            ('scissors', 'rock'): "Player 2 wins!",
            ('paper', 'scissors'): "Player 2 wins!",
            ('rock', 'paper'): "Player 2 wins!",
        }
        if choice1 == choice2:
            result = "It's a tie!"
        else:
            result = outcomes.get((choice1, choice2), "Invalid choices!")

        # Send results to both players
        player1.send(f"Player 1 chose {choice1}, Player 2 chose {choice2}. {result}".encode('utf-8'))
        player2.send(f"Player 1 chose {choice1}, Player 2 chose {choice2}. {result}".encode('utf-8'))
    finally:
        player1.close()
        player2.close()

def handle_client(client_socket):
    try:
        client_socket.send(b"Welcome to Rock-Paper-Scissors! Waiting for an opponent...\n")
        match_queue.put(client_socket)  # Add player to matchmaking queue

        # Wait until another player is available
        while match_queue.qsize() < 2:
            pass

        # Pair the first two clients in the queue
        if not match_queue.empty():
            player1 = match_queue.get()
            player2 = match_queue.get()
            Thread(target=handle_game, args=(player1, player2)).start()

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server is running on port 5555...")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()