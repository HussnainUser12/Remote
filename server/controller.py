import socket

# Replace with your dynamic DNS hostname or IP address
admin_ip = 'hussnainmonitor.zapto.org'

def send_command_to_client(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((admin_ip, 9090))  # Connect to the client's IP (admin_ip is now used here)
        s.send(command.encode())  # Send the command to the client
        s.close()  # Close the connection after sending the command
        print(f"[✅] Command '{command}' sent to client.")
    except Exception as e:
        print(f"[❌] Error sending command to client: {e}")

if __name__ == "__main__":
    # Example usage: sending 'lock' command to client
    send_command_to_client("lock")
