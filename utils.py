import time as t


class Timer:
    '''
    Classe para medir tempo 
    '''
    def __enter__(self):
        self.begin = t.time()
        return self

    def __exit__(self, *args):
        self.duration = t.time() - self.begin




def checksum(data):
    '''
    Retorna o cheksum de uma palavra
    '''
    sum = 0
    # lê 16 bits (2 WORDs)
    for i in range(0, len(data), 2):
        if i < len(data) and (i + 1) < len(data):
            sum += (ord(data[i]) + (ord(data[i + 1]) << 8))
        elif i < len(data) and (i + 1) == len(data):
            sum += ord(data[i])
    addon_carry = (sum & 0xffff) + (sum >> 16)
    result = (~ addon_carry) & 0xffff
    # swap bytes
    result = result >> 8 | ((result & 0x00ff) << 8)
    return result