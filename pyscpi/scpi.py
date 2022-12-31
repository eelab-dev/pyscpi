import socket


class Instrument:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def write(self, cmd):
        self.s.sendall(str.encode(cmd + '\n'))

    def read(self):
        return self.s.recv(1024).decode('utf-8')

    def read_bytes(self):
        return self.s.recv(1024)

    def close(self):
        self.s.close()

    def query(self, cmd):
        self.write(cmd)
        return self.read()
