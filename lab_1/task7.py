import socket
import ssl


host = '999.md'
port = 443  


# Create TCP connection to the server and wrap it in SSL for HTTPS
def create_tcp_connection(host, port):
    context = ssl.create_default_context()
    sock = socket.create_connection((host, port))
    ssock = context.wrap_socket(sock, server_hostname=host)
    return ssock

# Function to send HTTP request
def send_http_request(connection):
    request = f"GET /ro/list/transport/cars HTTP/1.1\r\nHost: {host}\r\nUser-Agent: CustomClient/1.0\r\nConnection: close\r\n\r\n"
    connection.send(request.encode())

# Function to receive the response from the server
def receive_response(connection):
    response = b""
    while True:
        data = connection.recv(4096)  # Receive 4KB chunks of data
        if not data:
            break
        response += data
    return response.decode()

# Example usage
if __name__ == "__main__":
    connection = create_tcp_connection(host, port)
    send_http_request(connection)
    response = receive_response(connection)
    print(response)
    connection.close()
