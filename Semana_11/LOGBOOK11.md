# Semana 11 - Public Key Infrastructure

## Setup

Antes de tudo, temos que dar setup do DNS. Para isso, temos que alterar o ficheiro `/etc/hosts`:

```shell
sudo nano /etc/hosts    #Temos que adicionar 10.9.0.80  www.bank32.com
```

## Task 1 - Becoming a Certificate Authority (CA)

Primeiramente, temos de copiar o ficheiro `usr/lib/ssl/openssl.cnf` para o diretório atual:

```shell
cp usr/lib/ssl/openssl.cnf .
```

Depois de descomentar a linha do `unique_subject`, temos de seguir a configuração definida na seção `CA_default` e criar múltiplos sub-diretórios:

```shell
mkdir CA
cd CA
mkdir certs crl
touch index.txt
mkdir newcerts
cat >> serial
1000
```

Agora temos de generar um certificado auto-assinado para a CA:

```shell
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -keyout ca.key -out ca.crt
```

Depois de correr este comando, fomos prompted para inserir vários espaços de informação. Inserimos o seguinte:

    - Pass Phrase: 1234
    - Country Name: PT
    - State or Province Name: Porto
    - Locality Name: Maia
    - Organization Name: FEUP
    - Organization Unit Name: LEIC
    - Common Name: Lavra
    - Email Address: test@gmail.com


Podemos, agora, correr os seguintes comandos para ver o conteúdo desencriptado do certificado e da chave:

```shell
openssl x509 -in ca.crt -text -noout
openssl rsa -in ca.key -text -noout
```

### Questões

1. Que parte do certificado indica que é um certificado CA?

![image](./images/ca_certificate.png)

Aqui conseguimos observar que `CA` está set a `TRUE`, o que quer dizer que este é um certificado **CA**

2. Que parte do certificado indica que é um certificado **auto-assinado**?

![image](./images/auto-signed.png)

Aqui conseguimos ver que tanto o `ISSUER` quanto o `SUBJECT` têm a mesma informação, o que significa que o certificado é **auto-assinado**

3. No algoritmo RSA, temos um expoente público ***e***, um expoente privado ***d***, um módulo ***n*** e dois números secretos ***p*** e ***q***, tal que ***n*** = ***p\*q***. Identifica os valores destes elementos no certificado e na chave.

No ficheiro conseguimos observar os seguintes parâmetros:

    - modulus, que representa o módulo n
    - publicExponent, que representa o expoente público
    - privateExponent, que representa o expoente privado
    - prime1, que representa o número secreto p
    - prime2, que representa o número secreto q

## Task 2 - Generating a Certificate Request for your Web Server

Nesta task, temos que generar um **Certificate Signing Request (CSR)** para o site `www.bank32.com` que adicionamos no [setup](#setup) :

```shell
openssl req -newkey rsa:2048 -sha256 -keyout server.key -out server.csr -subj "/CN=www.bank32.com/O=Bank32 Inc./C=US" -passout pass:1234 -addext "subjectAltName = DNS:www.bank32.com, DNS:www.bank32A.com, DNS:www.bank32B.com"
```

## Task 3 - Generating a Certificate for your server

Primeiro, temos que descomentar a linha `copy_entensions = copy` do ficheiro `openssl.cnf`.

Depois disso, temos que assinar o certificado para o servidor do `www.bank32.com`:

```shell
openssl ca -config openssl.cnf -policy policy_anything -md sha256 -days 3650 -in server.csr -out server.crt -batch -cert ca.crt -keyfile ca.key
```

![image](./images/bank32key.png)


Depois de assinar o certificado, podemos descodificar o conteúdo do certificado e ver se os nomes alternativos estão incluídos:

```shell
openssl x509 -in server.crt -text -noout
```

![image](./images/alternativenames.png)

Como podemos observar, os nomes alternativos estão incluídos.

## Task 4 - Deploying Certificate in an Apache-Based HTTPS Website

Primeiramente, é necessário copiar os ficheiros `server.crt` e `server.key` para a pasta `volumes` e mudar o nome dos ficheiros para `bank32`, com a respetiva extensão.

Depois disso, precisamos de abrir uma shell no container e alterar o ficheiro `/etc/apache2/sites-available/bank32_apache_ssl.conf` :

![image](./images/apachessl.png)

Agora, temos de começar o server. Para isso, corremos o seguinte comando na shell do container:

```shell
service apache2 start
```

![image](./images/apachestart.png)

Agora, podemos aceder ao servidor através do url `www.bank32.com`: 

![image](./images/serverinsecure.png)

Se tentarmos aceder ao servidor através do url `https://www.bank32.com`, obtermos o seguinte resultado : 

![image](./images/httpswarning.png)

Isto é devido à ligação não estar encriptada. Para resolver isso, temos que adicionar o nosso certificado à lista de certificados do FireFox.

Para fazer isso, vamos ao url `about:preferences#privacy` -> Security -> Certificates -> View Certificates -> Authorities -> Import e escolhemos o ficheiro `ca.crt`.

![image](./images/lavraftw.png)

Como podemos observar, o nosso certificado está agora na lista de certificados do FireFox.

Agora, se tentarmos aceder ao servidor pelo url `https://www.bank32.com`, vemos o seguinte:

![image](./images/serversecure.png)

## Task 5 - Launching a Man-In-The-Middle Attack

Primeiro, temos que alterar o ficheiro `/etc/apache2/sites-available/bank32_apache_ssl.conf` de forma a que o `ServerName` seja `example.com` :

![image](./images/example.png)

Depois disso, temos que alterar agora o ficheiro `/etc/hosts` de forma a que o IP que anteriormente apontava para `www.bank32.com` agora aponte para `www.example.com`. Podemos alterar esse ficheiro com o seguinte comando: 

```shell
sudo nano /etc/hosts
```

Agora, após recomeçar o servidor, quando visitamos `www.example.com` observamos o seguinte:

![image](./images/exampletask5.png)

Como podemos ver, o certificado não foi confiado e o browser alerta-nos para um possível risco.

## Task 6 - Launching a Man-In-The-Middle Attack with a Compromised CA

Assumindo que um atacante conseguiu obter posse da chave privada da root **CA**, ele consegue gerar certificados utilizando essa chave privada. Ele consegue fazer isso da seguinte forma:

```shell
openssl req -newkey rsa:2048 -sha256 -keyout example.key -out example.csr -subj "/CN=www.example.com/O=example Inc./C=US" -passout pass:1234

openssl ca -config openssl.cnf -policy policy_anything -md sha256 -days 3650 -in example.csr -out example.crt -batch -cert ca.crt -keyfile ca.key
```

Estes 2 comandos foram utilizados na tarefa 2 para gerar os certificados para o servidor `www.bank32.com`

![image](./images/task6cert.png)

Como podemos ver, conseguimos criar um certificado para uma organização chamada `example Inc.` cujo website é `www.example.com`.

Agora, só precisamos de alterar o ficheiro `/etc/apache2/sites-available/bank32_apache_ssl.conf` de forma a que ele use os ficheiros `example.crt` e `example.key`, que acabamos de criar com o root **CA**.

![image](./images/task6apache.png)

Se tentarmos aceder ao url `www.example.com`, conseguimos ver que a conexão é segura, ou seja, o ataque foi bem sucedido.

![image](./images/task6example.png)