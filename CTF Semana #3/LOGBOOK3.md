# CTF Semana #3 - Wordpress

## Objetivo

- Fazer login como administrador num servidor wordpress utilizando uma CVE com exploit conhecido.

## Primeira Fase - Reconhecimento

Primeiramente, começamos por explorar o site para tentar recolher o máximo de informação pertinente ao site, que nos permitisse encontrar uma vulnerabilidade. Para isso procuramos, especificamente, por plugins instalados, versões dos plugins, versão do próprio Wordpress e possíveis contas criadas no site, em específico a conta admin, já que o nosso objetivo era sermos autenticados como admin. Recolhemos a seguinte informação:

- Versão do Wordpress: 5.8.1
- Plugins instalados: WooCommerce e Booster for WooCommerce
- Versão do WooCommerce: 5.7.1
- Versão do Booster for WooCommerce: 5.4.3
- Contas existentes: Orval Sanford (regular user), admin (the administrator, very useful)

## Segunda Fase - Pesquisa

Agora, com as versões do Wordpress e dos plugins instalados, pesquisamos por vulnerabilidades existentes nestas versões. Depois de procurar por vulnerabilidades para a versão 5.8.1 do Wordpress e 5.7.1 do WooCommerce, encontramos uma vulnerabilidade não desses dois, mas sim do Booster for WooCommerce, para a versão 5.4.3, com uma CVE identificada: CVE-2021-34646.

https://www.exploit-db.com/exploits/50299


## Terceira Fase - O Ataque

Com uma vulnerabilidade identificada e um exploit encontrado pronto para correr, só falta realizar o ataque.  
Para isto foi útil saber que existe uma conta administrativa com username "admin" pois, depois de correr o exploit, só precisamos de tentar dar log in na conta admin com 1 dos 3 possíveis hashes como password. 
O primeiro hash funcionou logo e ganhamos acesso à conta admin. 

## Quarta Fase - Flag

Como estava referido no enunciado, dirigimo-nos à página http://ctf-fsi.fe.up.pt:5001/wp-admin/edit.php, onde imediatamente encontramos a flag: please don't bother me.
