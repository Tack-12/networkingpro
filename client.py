import socket

def start_client():
    # Connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))  # Connect to localhost, port 5555

    try:
        while True:
            # Receive message from the server
            message = client.recv(1024).decode('utf-8')
            print(message)

            # If prompted to send a choice, read user input and send it to the server
            if "Send your choice" in message:
                choice = input("Enter your choice (rock, paper, scissors): ").strip().lower()
                while choice not in ["rock", "paper", "scissors"]:
                    print("Invalid input! Please choose 'rock', 'paper', or 'scissors'.")
                    choice = input("Enter your choice (rock, paper, scissors): ").strip().lower()
                client.send(choice.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Disconnected from the server.")
        client.close()

if __name__ == "__main__":
    start_client()