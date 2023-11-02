import socket
import time


class HttpClient:
    __server_host = ''
    __server_port = 0

    def __init__(self, server_host='127.0.0.1', server_port=8000) -> None:
        self.__server_host = server_host
        self.__server_port = server_port

    def is_connected(self) -> bool:
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_connection.connect((self.__server_host, self.__server_port))
            client_connection.close()
            return True
        except Exception as e:
            return False

    def request_get(self) -> bool:
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_connection.connect((self.__server_host, self.__server_port))
            request = f'GET / HTTP/1.1\r\nHost:{self.__server_host}\r\nTime:{time.time()}\r\n'
            client_connection.send(request.encode())
            response = client_connection.recv(1024)
            client_connection.close()
            if response.decode().startswith('HTTP/1.0 200 OK'):
                return True
            return False
        except Exception as e:
            return False

    def request_post(self) -> bool:
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            content = 'Hello'
            content_len = len(content)
            client_connection.connect((self.__server_host, self.__server_port))
            request = f'POST / HTTP/1.1\r\nHost: {self.__server_host}\r\nAccept: */*\r\nContent-Length: {content_len}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{content}'
            client_connection.send(request.encode())
            response = client_connection.recv(1024)
            client_connection.close()
            if response.decode().startswith('HTTP/1.0 200 OK'):
                return True
            return False
        except Exception as e:
            return False

    def request_put(self) -> bool:
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_connection.connect((self.__server_host, self.__server_port))
            request = f'PUT / HTTP/1.1\r\nHost: {self.__server_host}\r\n\r\n'
            client_connection.send(request.encode())
            response = client_connection.recv(1024)
            client_connection.close()
            if response.decode().startswith('HTTP/1.1 405 Method Not Allowed'):
                return True
            return False
        except Exception as e:
            return False

def test_connection(client: HttpClient) -> None:
    if client.is_connected():
        print('Подключение к серверу: ✅')
    else:
        print('Подключение к серверу: ❌')


def test_get_request(client: HttpClient) -> None:
    if client.request_get():
        print('Отправка GET-запроса: ✅')
    else:
        print('Отправка GET-запроса: ❌')


def test_post_request(client: HttpClient) -> None:
    if client.request_post():
        print('Отправка POST-запроса: ✅')
    else:
        print('Отправка POST-запроса: ❌')

def test_other_request(client: HttpClient) -> None:
    if client.request_put():
        print('405 ошибка при PUT-запросе: ✅')
    else:
        print('405 ошибка при PUT-запросе: ❌')


if __name__ == '__main__':
    client = HttpClient()
    test_connection(client)
    test_get_request(client)
    test_post_request(client)
    test_other_request(client)
