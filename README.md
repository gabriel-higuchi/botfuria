# FURiA Bot Discord

Este repositório contém o código de um **bot para o Discord** que interage com a API da PandaScore, trazendo informações sobre partidas e jogadores de CS:GO. O bot oferece comandos como:

- `!lineup` – Exibe a escalação de uma partida.
- `!partidas` – Mostra as partidas atuais.
- `!proxima` – Mostra a próxima partida programada.
- `!sugestao` – Dá sugestões de ações no bot.
- `!stats [jogador] [partida]` – Exibe estatísticas de um jogador em uma partida específica.

## Pré-requisitos

Antes de rodar o bot, você precisa ter os seguintes requisitos instalados:

- [Node.js](https://nodejs.org/) (recomendado versão LTS)
- [npm](https://www.npmjs.com/)

## Passos para rodar o código

1. **Clone o repositório:**

   Primeiro, clone o repositório para o seu computador:

   ```bash
   git clone https://github.com/gabriel-higuchi/botfuriadiscwhats.git

2. **instale as dependencias**

    cd botfuriadiscwhats
    npm install

3. **Resgate suas keys**

    Resgate sua key no sites do discord: https://discord.com/developers/docs/intro
    Resgate sua key no sites do pandascore: https://www.pandascore.co/
    substitua nas linhas:
    DISCORD_TOKEN=seu_token_aqui
    PANDASCORE_API_KEY=sua_api_key_aqui

3. **Rode o bot**
    npm start

# FURiA Bot WhatsApp

Este repositório contém o código de um **bot para o WhatsApp** que utiliza a API do WhatsApp para interagir com os usuários. O bot é capaz de realizar diversas funções automatizadas.

## Pré-requisitos

Antes de rodar o bot, você precisa ter os seguintes requisitos instalados:

- [Node.js](https://nodejs.org/) (recomendado versão LTS)
- [npm](https://www.npmjs.com/)
- [WhatsApp Web API](https://www.npmjs.com/package/whatsapp-web.js) ou [WAPI](https://github.com/mukulhase/WebWhatsapp-Wrapper)

## Passos para rodar o código

1. **Clone o repositório:**

   Clone o repositório para o seu computador com o seguinte comando:

   ```bash
   git clone https://github.com/gabriel-higuchi/botfuriadiscwhats.git

WHATSAPP_NUMBER=seu_numero_de_whatsapp_aqui
npm start





