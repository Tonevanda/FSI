# CTF Semana 12 - Find my TLS

flag{<frame_start>-<frame_end>-<selected_cipher_suite>-<total_encrypted_appdata_exchanged>-<size_of_encrypted_message>}, onde:

- <frame_start> e <frame_end> são o primeiro e último (respetivamente) números de frame correspondentes ao procedimento de handshake do TLS.
- <selected_cipher_suite> é a ciphersuite escolhida para a conexão TLS (o nome, não o código)
- <total_encrypted_appdata_exchanged> é a soma total do tamanho dos dados cifrados trocados neste canal, até à sua terminação.
- <size_of_encrypted_message> é o tamanho da mensagem cifrada no handshake que concluí o procedimento de handshake.

- frame_start = 
- frame_end = 
- selected_cipher_suite
- total_encrypted_appdata_exchanged
- size_of_encrypted_message

## Selected Cipher Suite

Clicando num pacote `Server Hello`, se formos ao parâmetro `Handshake Protocol: Server Hello` conseguimos ver que há um campo chamado `ciphersuite`:

![image](images/ciphersuite.png)

Portanto, <selected_cipher_suite> é **TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384**.

## Total Encrypted AppData Exchanged

Podemos filtrar os pacotes do **Wireshark** para só ver os pacotes de transmissão de AppData.<br>
Fazemos isso escrevendo **tls.record.content_type == 23** na barra de filtros do **Wireshark**.
Se selecionarmos todos os pacotes, formos a **Statistics->Conversations** conseguimos ver o número total de bytes transmitidos:

![image](images/totaldatasent.png)

Portanto, <total_encrypted_appdata_exchanged> é **264000** bytes.

## Size of Encrypted Message

Temos de voltar a detetar os pacotes de **handshake**, pois o tamanho da mensagem encriptada no **handshake** está no último pacote que conclui o **handshake**.

Após encontrar esse pacote, que é o último pacote diretamente antes do primeiro pacote de **Application Data**, podemos ver o campo **length**

![image](images/sizeofmessage.png)

Como podemos ver, <size_of_encrypted_message> é 49.