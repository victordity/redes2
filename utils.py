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



#!/usr/bin
#iFunção para criar maskara dos tamanho do quadro

def maskLength():
  #print(type(n))
  n = 9999
  str1 = '000'
  str2 = '00'
  str3 = '0'
  if n < 10:
    str1 = str1 + str(n)
    print(str1)
    
  elif n < 100:
      str2 = str2 + str(n)
      print(str2)
    
  elif n < 1000:
      str3 = str3 + str(n)
      print(str3)
    
  else:
      print(str(n))
