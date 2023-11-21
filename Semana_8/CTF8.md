# CTF Semana 8 - SQL Injection

Após analisar o ficheiro `index.php`, que processa o input do utilizador, chegamos à conclusão que esse input não é sanitizado, o que torna o site vulnerável a ataques de SQL Injection.<br>
Como sabemos que a flag é revelada se dermos log in como admin, tudo o que precisamos fazer é descobrir uma maneira de dar log in como admin, sem saber a password.<br>
Como o site está vulnerável a ataques de SQL Injection, autenticamo-nos com as seguintes credenciais:
    - Username: **admin';#**
    - Password: **a**

O username `admin';#` vai inserir como username na query o nome `admin` e vai, de seguida, comentar o que vier posteriormente na query, através do `#`, que, neste caso, é a password.<br>
Mesmo a password não sendo processada pela query devido ao `#`, como o field **password** é **required**, ou seja, temos que inserir algum valor, então, simplesmente, temos que meter qualquer input nesse field, nós colocamos **a**.

Com isso, obtemos a flag **flag{5f62c33d36bbd8fb2e50343dcf66ee70}**

![image](/images/ctf8.png)
