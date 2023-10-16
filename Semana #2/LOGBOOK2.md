# Trabalho realizado nas Semanas #2 e #3

## Identificação

- A API do servidor na versão de lançamento da aplicação Anda depende de credenciais hardcoded.

## Catalogação

- Gravidade : 9.8  Critical
- Descoberto em 2018 por ex-aluno da FEUP Gustavo Silva
- Mudando código binário de forma a passar uma verificação e poder fazer chamadas API com permissões ilimitadas
- As credenciais para fazer chamadas API são iguais para todos os users e hardcoded na native library da app

## Exploit

- "Privilege escalation", pois era possível fazer chamadas API com permissões ilimitadas, que utilizadores normais não tinham
- Não existe automação para repetir este exploit


## Ataques

- Este ataque tinha potencial para roubar toda a informação dos utilizadores incluindo morada, NIF, 4 dígitos do cartão de crédito, etc.
- Gustavo Silva, após a descoberta desta vulnerabilidade, relatou aos desenvolvedores, que corrigiram o erro.
- Não existe relatos do mesmo ataque ter sido utilizado antes da vulnerabilidade ter sido corrigida.


### Referências adicionais

- https://gustavosilva.me/blog/2018/10/23/How-I-hacked-Anda-the-public-transportation-app-of-Porto-CVE-2018-13342.html
