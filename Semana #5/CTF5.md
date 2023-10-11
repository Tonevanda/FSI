# CTF #5 - Buffer Overflow (Desafio 1)

O zip fornecido para a captura desta flag contém 5 ficheiros:


- `main.c` : um código em C que simula o comportamento do servidor onde está a flag
- `flag.txt` : um ficheiro de texto que contém uma flag placeholder
- `mem.txt` : um ficheiro de texto que contém um desenho em ASCII
- `program` : binário do `main.c` 
- `exploit-example.py` : um script em python que nos conecta ao servidor onde está a flag e envia uma mensagem ou faz o mesmo mas localmente

Além disso, se rodarmos o seguinte comando: 

```
checksec program 
```

Obtemos informação bastante útil para construir o nosso ataque.

```
Arch: i386-32-little
RELRO: No RELRO
Stack: No canary found
NX: NX disabled
PIE: No PIE (0x8048000)
RWX: Has RWX segments
```

Sabendo isto, devemos analisar o `main.c` e concluir se é possível fazer um ataque de **buffer overflow**.

Muito rápido percebemos que sim, pois são criados 2 buffers:

- meme_file[8] : buffer com o nome do ficheiro que será aberto pelo `main.c`
- buffer[32] : buffer que irá lê o input e imprime no terminal

O buffer de leitura só tem 32 bytes de espaço, mas no código é chamada a função **scanf()** que vai ler 40 bytes.<br>
Ora, desta forma, podemos enviar uma mensagem de 32 bytes e, como vão ser lidos 40 bytes, podemos escrever mais 8 bytes na memória e, deste modo, fazer **buffer overflow**.<br>
Como o buffer e o meme_file estão em posições contínuas na memória, os 8 bytes a mais que escrevermos serão escritos no meme_file.<br>
Como o meme_file contém o nome do ficheiro que será aberto pelo `main.c`, se alterarmos este buffer para "flag.txt" então conseguimos obter a flag. 


