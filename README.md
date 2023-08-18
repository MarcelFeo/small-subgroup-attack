# Experimento de Ataque de Subgrupo em Curvas Elípticas

Este código Python implementa um experimento que simula o ataque de subgrupo em curvas elípticas, como descrito no artigo "A Small Subgroup Attack on Bitcoin Address
Generation". O objetivo é demonstrar como um atacante pode explorar a vulnerabilidade de um subgrupo na geração de chaves públicas de Bitcoin para derivar chaves privadas correspondentes.

## Etapas Principais

### Parâmetros da Curva Elíptica

- A curva elíptica usada é secp256k1, a mesma usada no Bitcoin.
- Os parâmetros da curva (p, n, a, b, Gx, Gy) são definidos.

### Geração de Chaves

- Função `generate_private_key()` gera uma chave privada aleatória dentro do intervalo [1, n-1].
- A chave privada é usada para gerar uma chave pública correspondente usando ECDSA.

### Geração de Endereço Bitcoin

- A chave pública é usada para calcular um hash SHA-256 e um hash RIPEMD-160.
- Um endereço Bitcoin é criado concatenando o prefixo '0x00', o hash RIPEMD-160 e um checksum.
- O endereço é codificado usando Base58 para representação legível.

### Verificação na Blockchain

- O código verifica se um endereço Bitcoin tem saldo na blockchain usando a API do Blockchain.info.

### Ataque de Subgrupo

- O código gera um número de chaves privadas e suas chaves públicas correspondentes.
- Para cada par de chaves, verifica se o endereço Bitcoin correspondente tem saldo na blockchain.
- Os endereços com saldo são armazenados como parte do ataque de subgrupo.

### Saída do Experimento

- A saída exibe as chaves privadas, chaves públicas e endereços Bitcoin atacados.

## Observações

- O ataque de subgrupo aproveita a vulnerabilidade de subgrupos na geração de chaves públicas, permitindo que um atacante comprometa chaves privadas.
- É importante notar que esse código é apenas um experimento didático e não deve ser utilizado para fins maliciosos.
- Lembre-se de que o uso adequado de técnicas de criptografia e segurança cibernética é essencial para proteger informações confidenciais e sistemas.
