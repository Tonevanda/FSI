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

Alternadamente, podemos simplesmente fazer **make**, pois o `Makefile` já tem as instruções para fazer isto.

Depois de fazer **make**, são criados 4 pares de ficheiros executáveis:

- `stack-L1` e `stack-L1.dbg`
- `stack-L2` e `stack-L2.dbg`
- `stack-L3` e `stack-L3.dbg`
- `stack-L4` e `stack-L4.dbg`

Agora, falta mudar o conteúdo do `badfile`` para conseguirmos dar exploit à vulnerabilidade existente.

## Task 3 

