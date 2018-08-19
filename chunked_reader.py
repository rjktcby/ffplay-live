class ChunkedReader(object):
    def __init__(self, src, chunk_size, consumer):
        self.src = src
        self.chunk_size = chunk_size
        self.consumer = consumer
        self.buffer = b''

    def read(self):
        self.buffer = b''
        for chunk in iter(lambda: self.src.read(self.chunk_size), b''):
            print('read {} bytes, chunk size is {}'.format(
                len(chunk), self.chunk_size))
            if len(chunk) == 0:
                break

            self.buffer += chunk
            while len(self.buffer) >= self.chunk_size:
                self.consumer(self.buffer[:self.chunk_size])
                self.buffer = self.buffer[self.chunk_size:]
