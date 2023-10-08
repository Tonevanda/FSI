# Semana  #3- Environment Variable and Set-UID Lab


## Task 1: Manipulating Environment Variables


Com esta task, descobrimos como printar as environment variables no terminal com a ajuda de dois comandos, printenv e env.
Além disso, aprendemos 2 comandos da bash que servem para dar set e unset de environment variables, export e unset. Com export, podemos criar as nossas próprias environment variables da seguinte forma:

```
export VARIAVEL=VALOR_DESEJADO
``` 

## Task 2: Passing Environment Variables from Parent Process to Child Process


Após compilar o ficheiro **myprintenv.c** com o **printenv()** no child process e rodar e, posteriormente, repetir o processo, mas comentar o **printenv()** do child process e descomentar o do parent process, quando comparamos os ficheiros de output de ambos com o comando **diff**, notamos que são iguais o que nos diz que, depois de dar **fork()**, o child process herda as environment variables do parent process.


## Task 3: Environment Variables and execve()


Depois de compilar e rodar o programa **myenv.c** pela primeira vez, com o terceiro parâmetro da função **execve()** em NULL, nada acontece, mas, se trocarmos NULL por environ, que é um array de pointers para o ***environment***, onde estão as environment variables, o programa imprime, de facto, as environment variables.
Com isto, podemos concluir que, se o ***environment*** não for passado como parâmetro para a função **execve()**, o novo programa não tem acesso às environment variables do programa que o chamou.


## Task 4: Environment Variables and system()


De facto, tal como referido na task 4, o excerto de código providenciado no guião, através da função **system()** imprime as environment variables no terminal, pois, na própria implementação da função **system()**, é chamado **execve()** e passado o environment como parâmetro.


## Task 5: Environment Variable and Set-UID Programs


Depois de compilar o programa, mudar o owner e tornar o programa um Set-UID program com os comandos explicitados no guião, só resta usar o **export** command para dar set às environment variables, neste caso, o **PATH**, o **LD_LIBRARY_PATH** e também qualquer outra variável que queiramos criar.
Após rodar o programa descobrimos algo interessante. A variável **PATH** e as que nós criamos foram imprimidas no terminal ou seja, foram herdadas pelo child process. Pelo contrário, a variável **LD_LIBRARY_PATH** não estava presente ou seja, não foi herdada pelo Set-UID program's process.


