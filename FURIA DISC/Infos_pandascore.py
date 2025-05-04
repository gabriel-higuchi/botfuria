import requests
import datetime
from datetime import datetime
from flask import Flask, jsonify, request

BASE_URL = 'https://api.pandascore.co'
PANDASCORE_TOKEN = 'Seu_token_aqui'
TEAM_NAME = 'FURIA'
CSV_FILE = 'sugestoes.csv'
running_matches = []

def lineup(nome_time='FURIA'):
    url = f'{BASE_URL}/csgo/teams?search[name]={nome_time.lower()}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        teams = response.json()
        if not teams:
            return f"❌ Time '{nome_time}' não encontrado."

        mensagens = []
        for team in teams:
            players = team.get('players', [])
            if not players:
                continue

            nome = team.get('name', 'Sem nome')
            acronym = team.get('acronym', '')
            mensagem = f"🏆 **{nome} ({acronym})**:\n"
            for player in players:
                first = player.get('first_name', '')
                nick = player.get('name', '')
                last = player.get('last_name', '')
                full_name = f"{first} '{nick}' {last}".strip()
                mensagem += f"🎮 {full_name}\n"
                
            mensagens.append(mensagem)

        if not mensagens:
            return f"❌ Nenhuma lineup ativa foi encontrada para '{nome_time}'."

        return "\n---\n".join(mensagens)
    else:
        return f"❌ Erro ao buscar lineup (status {response.status_code})."
    

def get_team_id_by_name(team_name):
    url = f"{BASE_URL}/csgo/teams?search[name]={team_name}"
    headers = {
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        teams = response.json()
        if teams:
            return teams[0]['id']
    return None


def fetch_matches():
    team_id = get_team_id_by_name(TEAM_NAME)
    if not team_id:
        print("❌ Time não encontrado.")
        return []

    url = f"{BASE_URL}/csgo/matches/past?filter[opponent_id]={124530}&page[size]=3"
    headers = {
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Erro ao acessar a API:", response.text)
        return []


def check_for_updated_matches(cached_matches):
    updated_match_list = fetch_matches()
    if not updated_match_list or not cached_matches:
        return []
    
    return [
        updated_match for updated_match in updated_match_list if compare_date(
            updated_match["modified_at"], cached_matches[0]["modified_at"])
    ]


def compare_date(date1, date2):
    date1_dt = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
    date2_dt = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
    return date1_dt > date2_dt


def running_match_message(match):
    default_msg = f"🕹️ **{match['name']}** começou!"
    stream_list = match.get('streams_list', [])
    if stream_list:
        return f"{default_msg} Assista ao vivo em {stream_list[0]['raw_url']}"
    else:
        return default_msg


def finished_match_message(match):
    default_msg = f"🏁 **{match['name']}** terminou! Placar final: {match['results'][0]['score']} - {match['results'][1]['score']}"
    if match["draw"]:
        return default_msg
    else:
        return f"{default_msg}. O time vencedor é {match['winner']['name']}"


def exibir_partidas_furia_masculina():
    url = f"{BASE_URL}/csgo/matches/past?filter[opponent_id]={124530}&page[size]=3"
    headers = {
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }
    message = "\n📝 Detalhes das últimas 3 partidas da FURIA:"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        partidas = response.json()
        for i, match in enumerate(partidas, start=1):
            nome_partida = match.get("name", "N/A")
            data_partida = match.get("begin_at", "N/A")
            if data_partida != "N/A":
                data_formatada = datetime.strptime(data_partida, "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M")
            else:
                data_formatada = "Data não disponível"      
            resultados = match.get("results", [])
            if resultados:
                placar = f"{resultados[0].get('score', 'N/A')} - {resultados[1].get('score', 'N/A')}"
            else:
                placar = "Placar não disponível"    
            vencedor = match.get("winner", {}).get("name", "Não definido")

            # Utilizando f-strings para interpolação correta das variáveis
            message += f"\n📝 Detalhes da partida {i}:"
            message += f"\n📅 {nome_partida}"
            message += f"\n📆 Data: {data_formatada}"
            message += f"\n🏅 Vencedor: {vencedor}\n"
            message += f"⚔️ Placar: {placar}\n"

    else:
        message = "❌ Erro ao acessar as partidas."

    return message


def match_lifecycle_updates():
    cached_matches = fetch_matches()
    if not cached_matches:
        print("⚠️ Nenhuma partida encontrada para iniciar o monitoramento.")
        return
    # Exibe detalhes das últimas 3 partidas e encerra a execução
    print("\nDetalhes das últimas 3 partidas da FURIA:")
    exibir_partidas_furia_masculina()

def exibir_proxima_partida_furia():
    url = f"{BASE_URL}/csgo/matches/upcoming?filter[opponent_id]={124530}&page[size]=1"
    headers = {
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        partidas = response.json()
        
        if partidas:  # Verifica se há alguma partida futura
            match = partidas[0]
            data_partida = match.get("begin_at", "N/A")
            if data_partida != "N/A":
                data_formatada = datetime.strptime(data_partida, "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M")
            else:
                data_formatada = "Data não disponível"
            
            oponente = next((team["opponent"] for team in match["opponents"] if team["opponent"]["id"] != 124530), None)
            nome_oponente = oponente["name"] if oponente else "Oponente Desconhecido"

            message = f"\n📝 Próxima partida da FURIA:"
            message += f"\n⚔️ FURIA vs {nome_oponente}"
            message += f"\n📆 Data: {data_formatada}"
            return message

        else:
            return "⚠️ Nenhuma partida futura encontrada."
    else:
        return f"❌ Erro ao acessar a API: {response.status_code}"


def get_player_stats_from_match(player_id, match_id):
    # Primeiro, obtemos os detalhes da partida para encontrar o player_id
    match_url = f"{BASE_URL}/csgo/matches/{match_id}"
    headers = {
        'Authorization': f'Bearer {PANDASCORE_TOKEN}'
    }

    try:
        # Passo 1: Buscar informações da partida
        match_response = requests.get(match_url, headers=headers)
        match_response.raise_for_status()
        match_data = match_response.json()

        # Passo 2: Procurar o jogador nos times
        player_id = None
        player_nick = None
        
        for opponent in match_data.get('opponents', []):
            team = opponent.get('team', {})
            for player in team.get('players', []):
                if (player_id.lower() in player.get('name', '').lower() or 
                    player_id.lower() in player.get('first_name', '').lower() or
                    player_id.lower() in player.get('last_name', '').lower()):
                    
                    player_id = player.get('id')
                    player_nick = player.get('name')
                    break
            if player_id:
                break

        if not player_id:
            return f"❌ Jogador '{player_id}' não encontrado nesta partida."

        # Passo 3: Buscar estatísticas específicas do jogador
        stats_url = f"{BASE_URL}/csgo/matches/{match_id}/players/{player_id}/stats"
        stats_response = requests.get(stats_url, headers=headers)
        stats_response.raise_for_status()
        stats_data = stats_response.json()

        # Formata a resposta
        return (
            f"📊 Estatísticas de **{player_nick}** na partida:\n"
            f"• Kills: {stats_data.get('kills', 'N/A')}\n"
            f"• Deaths: {stats_data.get('deaths', 'N/A')}\n"
            f"• Assists: {stats_data.get('assists', 'N/A')}\n"
            f"• Headshots: {stats_data.get('headshots', 'N/A')}\n"
            f"• K/D Ratio: {stats_data.get('kd_ratio', 'N/A')}\n"
            f"• Rating: {stats_data.get('rating', 'N/A')}\n"
            f"• ADR: {stats_data.get('adr', 'N/A')}\n"
            f"• KAST: {stats_data.get('kast', 'N/A')}%"
        )

    except requests.exceptions.RequestException as e:
        return f"❌ Erro ao acessar a API: {str(e)}"
    except Exception as e:
        return f"❌ Erro inesperado: {str(e)}"
    

    
app = Flask(__name__)
@app.route('/sugestao', methods=['POST'])
def adicionar_sugestao(autor, mensagem):
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = CSV_FILE.writer(file)
            if file.tell() == 0:
                writer.writerow(["Autor", "Mensagem", "Data"])
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            writer.writerow([autor, mensagem, data_atual])
    except Exception as e:
        print(f"Erro ao gravar no CSV: {e}")



@app.route('/lineup', methods=['GET'])
def get_lineup():
    team_name = request.args.get('team_name', 'FURIA')
    response = lineup(team_name)
    return jsonify({'response': response})

@app.route('/last_matches', methods=['GET'])
def get_last_matches():
    response = exibir_partidas_furia_masculina()
    return jsonify({'response': response})

@app.route('/next_match', methods=['GET'])
def get_next_match():
    response = exibir_proxima_partida_furia()
    return jsonify({'response': response})

@app.route('/player_stats', methods=['GET'])
def get_player_stats():
    player_id = request.args.get('player_id')
    match_id = request.args.get('match_id')
    if player_id and match_id:
        response = get_player_stats_from_match(player_id, match_id)
        return jsonify({'response': response})
    else:
        return jsonify({'response': '❌ Parâmetros inválidos.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    







