# Resumos para Segundo Teste de FSI

## Index

- [Symmetric Encryption](#symmetric-encryption)
    - [Block Ciphers](#block-ciphers)
    - [Padding](#padding)
- [MACs and Authenticated Encryption](#macs-and-authenticated-encryption)
    - [Hash Collision](#hash-collision)
    - [Sponge Construction](#sponge-construction)
    - [HMAC Construction](#hmac-construction)
    - [Galois Counter Mode](#galois-counter-mode)
- [Public Key Encryption](#public-key-cryptography)

## Symmetric Encryption

### Block Ciphers

A block cipher is a cryptographic algorithm that operates on fixed-size blocks of data, typically in chunks of 64 or 128 bits. The key feature of a block cipher is its ability to transform a fixed-size block of plaintext into ciphertext under the control of a secret key.

The process involves two main components: encryption and decryption. During encryption, the block cipher takes a block of plaintext and a secret key as input, producing a corresponding block of ciphertext. Decryption is the reverse process, where the ciphertext and the same secret key are used to recover the original plaintext block.

The strength and security of a block cipher depend on its ability to resist various cryptographic attacks, such as brute-force attacks, differential cryptanalysis, and linear cryptanalysis. Popular block ciphers include Advanced Encryption Standard (AES), Triple DES (3DES), and Blowfish.

Block ciphers are widely used in various cryptographic applications, such as securing communications over the internet, encrypting files, and ensuring the confidentiality and integrity of data in various systems.

#### Disadvantages

Block ciphers are considered primitive cryptographic primitives because they operate on fixed-size blocks of data and provide a basic building block for various cryptographic protocols and constructions. However, using a block cipher by itself for certain applications, especially in the context of encrypting large amounts of data or establishing secure communication channels, may not be sufficient for several reasons:

- Block Size Limitations:
    Block ciphers operate on fixed-size blocks, and the block size is often relatively small (e.g., 64 or 128 bits). This can lead to issues when encrypting large messages. If the message is longer than a single block, the encryption needs to be applied iteratively to each block, and this process may introduce vulnerabilities.

- Deterministic Nature:
    Block ciphers are deterministic, meaning that the same plaintext block encrypted with the same key will always produce the same ciphertext. This can be a security concern when encrypting identical blocks in different parts of a message because it may leak information about the structure of the plaintext.

- Electronic Codebook (ECB) Mode Vulnerabilities:   
    Using a block cipher in Electronic Codebook (ECB) mode can be insecure for certain types of data. Identical plaintext blocks will produce identical ciphertext blocks, which may leak information. Patterns in the plaintext may remain visible in the ciphertext, and an attacker can exploit this to gain insights into the message.

- Lack of Authentication:
    Block ciphers, by themselves, do not provide data authentication. An attacker could modify the ciphertext, and without additional mechanisms like message authentication codes (MACs) or authenticated encryption modes, the recipient might decrypt a potentially tampered message.

To address these limitations, block ciphers are often used in combination with other cryptographic techniques and modes of operation. Common constructions include modes like Cipher Block Chaining (CBC) or [Galois/Counter Mode (GCM)](#galois-counter-mode), which provide additional security features like chaining blocks together or integrating authentication.

### Padding 

Padding refers to the addition of extra bits to the plaintext before encryption to ensure that the length of the plaintext is a multiple of the block size. Many block ciphers, such as the Advanced Encryption Standard (AES), operate on fixed-size blocks (e.g., 128 bits). If the length of the plaintext is not a multiple of the block size, padding is applied to fill the gap and create a complete block.

Padding is essential to accommodate messages of varying lengths and to align the data with the block size requirement of the encryption algorithm. The most commonly used padding scheme is PKCS#7 (Public Key Cryptography Standards #7), where the value of each added byte is the number of bytes added. For example, if one byte is required for padding, each added byte would have the value 0x01; if two bytes are needed, each byte would have the value 0x02, and so on.

Here's a simple example of how padding works:

Suppose you have a block cipher with a block size of 128 bits (16 bytes) and a plaintext message of 22 bytes. In this case, you would need to add 6 bytes of padding to make the total length a multiple of 16:

```
Original plaintext (22 bytes):
HELLO, THIS IS A MESSAGE
```

```
After padding (28 bytes):
HELLO, THIS IS A MESSAGE\x06\x06\x06\x06\x06\x06
```

In this example, `\x06` is used to represent the padding bytes, and the value 6 indicates that there are six bytes of padding added. The decryption process involves removing the padding after the ciphertext is decrypted. Padding ensures that the original message can be accurately reconstructed during decryption, even when its length is not an exact multiple of the block size.


## MACs and Authenticated Encryption

### Hash Collision

Collision finding refers to the process of finding two different inputs that produce the same hash value. A hash function takes an input (or message) and produces a fixed-size string of characters, which is typically a hash value. The goal of a good hash function is to produce unique hash values for different inputs, but due to the finite size of the output space, collisions can occur.

Collision finding is particularly important in the field of cryptography and computer security because it can have implications for the integrity and security of systems that rely on hash functions. Here's a brief overview of collision finding in hash functions:

- Hash Function Properties:
    - Deterministic: A hash function is deterministic, meaning that the same input will always produce the same hash value.
    - Fixed Output Size: The hash function produces a fixed-size output, regardless of the input size.

- Collision:
    A collision occurs when two different inputs produce the same hash value. Mathematically, if H is a hash function and x and y are two different inputs such that H(x) = H(y), then x and y form a collision.

- Cryptographic Hash Functions:
    In cryptographic applications, hash functions are required to have certain properties to resist collision finding attempts.
    - Preimage Resistance: Given a hash value, it should be computationally infeasible to find any input that produces that hash value.
    - Second Preimage Resistance: Given an input, it should be computationally infeasible to find another input that produces the same hash value.
    - Collision Resistance: It should be computationally infeasible to find any two different inputs that produce the same hash value.

- Birthday Paradox:
    The birthday paradox is a phenomenon in probability theory that states that the likelihood of two people sharing the same birthday is much higher than one might intuitively expect in a group of only 23 people. This concept is applicable to hash functions, where the likelihood of finding a collision increases more rapidly than linearly with the number of hashed items.

- Cryptanalysis and Attack Techniques:
    Cryptanalysts may use various techniques to find collisions, such as brute force attacks, where they systematically try different inputs until a collision is found, or more sophisticated techniques like birthday attacks.

- Mitigations:
    To enhance security, cryptographic hash functions are designed with larger output sizes and additional complexity to resist collision finding attempts. Commonly used cryptographic hash functions include SHA-256 (part of the SHA-2 family) and SHA-3.

### Sponge Construction

The sponge construction is a framework used in the design of hash functions. It is a versatile construction that allows for the creation of hash functions with specific properties, including being resistant to collision attacks.

#### Internal State and Absorption Phase:
The sponge construction maintains an internal state, which is initially set to a fixed value.
During the absorption phase, the input message is divided into blocks, and each block is XORed with a portion of the internal state. The resulting state is then put through a non-linear function.

#### Permutation Function:

The non-linear function applied to the internal state during the absorption phase is typically a permutation function.
The permutation function is designed to be a one-way function, meaning it is easy to compute in one direction but computationally difficult to reverse.

#### Squeezing Phase:

After the absorption phase, the sponge construction enters the squeezing phase.
In the squeezing phase, the output hash value is obtained by repeatedly extracting portions of the internal state.
The squeezing phase can continue indefinitely to produce as much output as needed.

#### Capacity and Rate:

The sponge construction has two main parameters: the capacity and the rate.
The capacity determines the amount of information that can be absorbed during the absorption phase.
The rate determines the amount of information processed in each step of the construction.
The sum of the capacity and rate equals the size of the internal state.

### HMAC Construction

HMAC, which stands for Hash-based Message Authentication Code, is a construction that provides a way to authenticate the integrity and authenticity of a message using a cryptographic hash function. It is commonly used in various security protocols and applications, such as secure communication over networks. ***How it works***:

#### Inputs

HMAC takes two inputs: a message (or data) to be authenticated and a secret key known only to the sender and the receiver.

#### Hash Function

HMAC uses a cryptographic hash function, denoted as H. This hash function can be any secure hash algorithm, such as SHA-256 or SHA-3.

#### Key Padding

If the length of the secret key is shorter than the block size of the hash function, the key is padded to match the block size. If the key is longer, it is hashed.

#### Inner Padding

The message is padded and processed by the hash function. This involves XORing the padded key with an inner constant (usually denoted as ipad).

```
inner_hash=H((key⊕ipad)∥message)
```

The result, denoted as **inner_hash**, is the hash of the concatenation of the XORed key and the message.

#### Outer Padding

The outer padding involves XORing the padded key with a different inner constant (usually denoted as opad).
```
hmac_output=H((key⊕opad)∥inner_hash)
```

The final HMAC output is the hash of the concatenation of the XORed key and the inner hash.

#### Security Properties

The use of two different constants (ipad and opad) and the key XORing help prevent certain types of attacks, including length extension attacks.<br>
The HMAC construction is designed to provide collision resistance and resist various cryptographic attacks when used with a secure hash function.

#### Use Cases

HMAC is commonly used in network protocols (e.g., TLS, IPsec), authentication systems, and other applications where data integrity and authenticity are critical.

### Galois Counter Mode

Galois Counter Mode (GCM) is a mode of operation for symmetric key cryptographic block ciphers, designed to provide both confidentiality and authenticity. It's commonly used for authenticated encryption with associated data (AEAD), making it suitable for secure communication protocols.

Here are the key components and features of GCM:

#### Block Cipher Usage

GCM operates on a block cipher, typically using the Advanced Encryption Standard (AES) as the underlying block cipher. Other block ciphers could be used as well.

#### Counter Mode

GCM uses a counter mode of operation, where a counter is incremented for each block of plaintext that is processed. This counter is combined with a nonce (number used once) to generate a unique counter value for each block.

### Galois Field Multiplication

GCM employs Galois field multiplication to combine the counter value and the block cipher output. This multiplication is performed in the Galois field GF(2^128).

#### Authentication

GCM provides authentication by incorporating a Galois field authentication tag. This tag is computed based on the ciphertext, additional associated data (AAD), and a secret key.
The authentication tag ensures the integrity and authenticity of both the ciphertext and associated data.

#### Nonce Usage

GCM requires a unique nonce for each encryption operation. The combination of the nonce and the counter ensures that the same key can be safely used for multiple encryption operations, as long as the nonce is unique for each operation.

#### Associated Data (AAD)

GCM allows the inclusion of associated data, which is additional data that is authenticated but not encrypted. This is useful for scenarios where certain information needs to be authenticated but does not need to be kept confidential.
 
#### Efficiency

GCM is known for its efficiency in hardware implementations and its ability to provide both confidentiality and authenticity in a single pass through the data.

#### Limitations

- GCM is not suitable for very short messages (smaller than a block size) because it relies on counter mode, and a small message might reuse counter values.
- GCM may be vulnerable to side-channel attacks if not implemented carefully.

## Public Key Cryptography

