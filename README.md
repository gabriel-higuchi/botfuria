# FURiA Bot Discord

Este repositório contém o código de um **bot para o Discord** que interage com a API da PandaScore, trazendo informações sobre partidas e jogadores de CS:GO. O bot oferece comandos úteis para acompanhar partidas em tempo real.

### Comandos disponíveis

- `!lineup` – Exibe a escalação de uma partida.
- `!partidas` – Mostra as partidas atuais.
- `!proxima` – Mostra a próxima partida programada.
- `!sugestao` – Dá sugestões de ações no bot.

## Pré-requisitos

- [Node.js](https://nodejs.org/) (versão LTS recomendada)
- [npm](https://www.npmjs.com/)

## Como rodar o bot

1. **Clone o repositório**
    ```git clone https://github.com/gabriel-higuchi/botfuriadiscwhats.git


2. **Instale as dependências**
    ```cd botfuriadiscwhats
    ```npm install


3. **Configure suas chaves**

Crie um arquivo `.env` na raiz do projeto e adicione:
    DISCORD_TOKEN=seu_token_discord_aqui
    PANDASCORE_API_KEY=sua_api_key_pandascore_aqui


4. **Inicie o bot**
    ```npm start


---

# FURiA Bot WhatsApp

Este repositório também contém o código de um **bot para o WhatsApp**, feito com a biblioteca `whatsapp-web.js`, que permite automações e interações com usuários através da interface Web do WhatsApp.

## Pré-requisitos

- [Node.js](https://nodejs.org/) (versão LTS recomendada)
- [npm](https://www.npmjs.com/)
- Biblioteca [`whatsapp-web.js`](https://www.npmjs.com/package/whatsapp-web.js)

## Como rodar o bot

1. **Clone o repositório**

(caso ainda não tenha clonado)
```git clone https://github.com/gabriel-higuchi/botfuriadiscwhats.git


2. **Instale as dependências**

```cd botfuriadiscwhats/FURIA WHATS
```npm install


3. **(Opcional) Configure um número de telefone**

Crie um arquivo `.env` com:
WHATSAPP_NUMBER=seu_numero_de_whatsapp


4. **Rode o bot**

```npm start


Um QR Code será exibido no terminal. Escaneie com o WhatsApp para autenticar a sessão.













