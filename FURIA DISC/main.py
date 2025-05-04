import discord
from discord.ext import commands
from Infos_pandascore import (
    lineup as get_lineup, 
    exibir_partidas_furia_masculina as get_partidas, 
    exibir_proxima_partida_furia,
    get_player_stats_from_match as get_player_stats, 
    fetch_matches as get_matches
)
from datetime import datetime
import csv


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')

@bot.command()
async def lineup(ctx):
    lineup = get_lineup()
    embed = discord.Embed(
        title="📋 Lineup Atual da FURIA",
        description=lineup,
        color=discord.Color.blurple()
    )
    await ctx.send(embed=embed)

@bot.command()
async def partidas(ctx):
    global ultimas_partidas_cache
    ultimas_partidas_cache = get_matches()
    partidas = get_partidas()
    
    embed = discord.Embed(
        title="📊 Últimas 3 Partidas da FURIA",
        description=partidas,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def proxima(ctx):
    proxima = exibir_proxima_partida_furia()
    embed = discord.Embed(
        title="🕒 Próxima Partida da FURIA",
        description=proxima,
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

@bot.command()
async def sugestao(ctx, *, texto: str = None):
    if texto:
        with open('sugestoes.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([str(datetime.now()), texto])
        embed = discord.Embed(
            title="✅ Sugestão Enviada",
            description=f"Sua sugestão foi enviada com sucesso: {texto}",
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="❌ Sugestão não enviada",
            description="Por favor, envie sua sugestão após o comando.",
            color=discord.Color.red()
        )
    await ctx.send(embed=embed)

@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="🆘 Comandos Disponíveis",
        description="Aqui estão os comandos que você pode usar com o bot:",
        color=discord.Color.purple()
    )
    embed.add_field(name="!lineup", value="Exibe o lineup atual da FURIA", inline=False)
    embed.add_field(name="!partidas", value="Exibe as últimas 3 partidas da FURIA", inline=False)
    embed.add_field(name="!proxima", value="Exibe a próxima partida da FURIA", inline=False)
    embed.add_field(name="!sugestao [mensagem]", value="Envia uma sugestão ou crítica", inline=False)
    embed.add_field(name="!ajuda", value="Mostra esta mensagem de ajuda", inline=False)
    await ctx.send(embed=embed)



# Substitua pelo seu token real
bot.run('KEY_DISCORD')


