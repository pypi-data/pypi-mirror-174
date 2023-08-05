import hashlib
from itertools import takewhile
from itertools import repeat

def raw_line_count(filename):
    file = open(filename, 'rb')
    buffer_generator = takewhile(
        lambda x: x,
        (file.raw.read(1024*1024) for _ in repeat(None)),
    )
    return sum( buffer.count(b'\n') for buffer in buffer_generator )

def compute_sha256(input_file):
    buffer_size = 65536
    sha = hashlib.sha256()
    with open(input_file, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()
