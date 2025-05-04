const qrcode = require('qrcode-terminal');
const { Client } = require('whatsapp-web.js');
const axios = require('axios'); // Para fazer requisições HTTP

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('⚠️ Escaneie o QR Code com seu WhatsApp');
});

client.on('ready', () => {
    console.log('✅ Bot está pronto e conectado!');
});

client.on('message', async (message) => {
    console.log(`📩 Mensagem recebida de ${message.from}: ${message.body}`);


    if (message.body === '!ajuda') {
        message.reply(
            '🆘 Comandos disponíveis:\n' +
            '!ajuda - Mostra esta mensagem\n' +
            '!lineup - Exibe a lineup do time (ex: !lineup FURIA)\n' +
            '!partidas - Exibe as últimas 3 partidas\n' +
            '!proxima - Exibe a próxima partida\n' 
        );
    }

    if (message.body.startsWith('!lineup')) {
        const teamName = message.body.split(' ')[1] || 'FURIA';
        try {
            const response = await axios.get(`http://localhost:5000/lineup?team_name=${teamName}`);
            message.reply(response.data.response);
        } catch (error) {
            message.reply('❌ Erro ao buscar lineup.');
        }
    }

    if (message.body === '!partidas') {
        try {
            const response = await axios.get('http://localhost:5000/last_matches');
            message.reply(response.data.response);
        } catch (error) {
            message.reply('❌ Erro ao buscar as últimas partidas.');
        }
    }

    if (message.body === '!proxima') {
        try {
            const response = await axios.get('http://localhost:5000/next_match');
            message.reply(response.data.response);
        } catch (error) {
            message.reply('❌ Erro ao buscar a próxima partida.');
        }
    }

    if (message.body.startsWith('!sugestao')) {
        const sugestaoTexto = message.body.replace('!sugestao', '').trim();
    
        if (sugestaoTexto.length === 0) {
            message.reply('❌ Por favor, escreva sua sugestão após o comando.');
            return;
        }
    
        try {
            const response = await axios.post('http://localhost:5000/sugestao', {
                autor: message.from, // ou um nome amigável se tiver
                mensagem: sugestaoTexto
            });
    
            message.reply(response.data.response);
        } catch (error) {
            console.error(error);
            message.reply('❌ Erro ao enviar a sugestão.');
        }
    }
    


});

client.initialize();
