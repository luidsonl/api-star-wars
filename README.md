# Star Wars API

API for managing Star Wars characters and user favorites. Built with Flask and Google Cloud Firestore.

## Como rodar localmente

Para executar o projeto em sua máquina local, siga os passos abaixo:

### 1. Pré-requisitos

É necessário ter o **Google Cloud SDK** instalado para rodar o emulador do Firestore.

### 2. Configurar o Emulador do Firestore

Inicie o emulador do Firestore em um terminal separado:

```bash
gcloud emulators firestore start
```

> [!NOTE]
> O projeto está configurado no arquivo `dev.sh` para apontar para `127.0.0.1:8700` (porta padrão do emulador).

### 3. Executar a API

Com o emulador rodando, execute o script de desenvolvimento:

```bash
./dev.sh
```

A API estará disponível em `http://localhost:8080`.

---

## Documentação (Swagger)

A API possui documentação interativa utilizando Swagger (OpenAPI).

Para acessar, certifique-se de que a API está rodando e acesse:

**[http://localhost:8080/apidocs/](http://localhost:8080/apidocs/)**

Nesta interface, você pode:
- Visualizar todos os endpoints disponíveis.
- Consultar esquemas de entrada e saída.
- Testar as requisições diretamente pelo navegador.

---

## Como rodar os testes

Os testes são executados utilizando o `pytest`. Para rodá-los, execute o script:

```bash
./test.sh
```

Você também pode passar argumentos adicionais para o pytest, como:

```bash
./test.sh tests/unit # Rodar apenas testes unitários
./test.sh -v         # Modo verboso
```
