# Semana  #3- Environment Variable and Set-UID Lab


## Task 1: Manipulating Environment Variables


Com esta task, descobrimos como printar as environment variable no terminal com a ajuda de dois comandos, printenv e env.
Além disso, aprendemos 2 comandos da bash que servem para dar set e unset de environment variables, export e unset. Com export, podemos criar as nossas próprias environment variables da seguinte forma:

```
export VARIAVEL=VALOR_DESEJADO
``` 

## Task 2: Passing Environment Variables from Parent Process to Child Process


Após compilar o ficheiro **myprintenv.c** com o **printenv()** no child process e rodar e, posteriormente, repetir o processo mas comentar o **printenv()** do child process e descomentar o do parent process, quando comparamos os ficheiros de output de ambos com o comando **diff**, notamos que são iguais, o que nos diz que, depois de dar **fork()**, o child process herda as environment variables do parent process.


## Task 3: Environment Variables and execve()
