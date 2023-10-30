import socket
import time
import json

class HttpServer:
    def __init__(self, server_host='127.0.0.1', server_port=8000) -> None:
        """Метод инициализации в котором происходит вызов методов для создания сокета и начала прослушивания соединений"""
        self.__create_socket(server_host, server_port)
        try:
            self.__start_listen()
        except Exception as e:
            if self.__socket:
                self.__socket.close()

    def __create_socket(self, server_host: str, server_port: int) -> None:
        """Метод создания сокета"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((server_host, server_port))
        server_socket.listen()
        self.__socket = server_socket

    def __start_listen(self) -> None:
        """Метод который начинает бесконечно прослушивать соединения"""
        while True:
            client_connection, client_address = self.__socket.accept()
            request = client_connection.recv(1024).decode()
            # Если http-метод запроса GET
            if request.startswith('GET'):
                response_json = {
                    "method": "GET",
                    "time": time.time()
                }
                response = f'HTTP/1.0 200 OK\r\nContent-Type: application/json; charset=utf-8\n\n"{response_json}"'
            # Если http-метод запроса POST
            elif request.startswith('POST'):
                data = request.split('\r\n')[-1]
                response_json = {
                    "method": "POST",
                    "data": data,
                    "time": time.time()
                }
                response = f'HTTP/1.0 200 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(json.dumps(response_json))}\r\n\r\n"{json.dumps(response_json)}"'
            # Любой другой http-метод выдаст 405 ошибку
            else:
                response = 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\nAllow: GET, POST\n\n<h1>405 This HTTP-method not allowed!</h1>'
            client_connection.send(response.encode())
            client_connection.close()
        self.__socket.close()


if __name__ == '__main__':
    HttpServer()

