import socket


class Instrument:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def write(self, cmd: str) -> None:
        self.s.sendall(str.encode(cmd + '\n'))

    def read(self) -> str:
        return self.s.recv(1024).decode('utf-8')

    def read_raw(self, chunk_size) -> bytes:
        return self.s.recv(1024)

    def close(self) -> None:
        self.s.close()

    def query(self, cmd: str) -> str:
        self.write(cmd)
        return self.read()
