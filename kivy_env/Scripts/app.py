from flask import Flask, jsonify, request, json
from datetime import datetime

app = Flask(__name__)

def am_pm_to_24h(datetime_str):
    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M:%S %p") #Formato AM/OM
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    
@app.route('/api/agendar', methods=['POST'])
def agendar_consulta():
    dados = request.get_json()
    nome = dados.get('nome')
    data_hora_am_pm = dados.get('data_hora')

    if nome and data_hora_am_pm:
        data_hora_24h = am_pm_to_24h(data_hora_am_pm)
        if data_hora_24h:
            #Aqui salva os dados no seu banco de dados ou arquivos JSON
            #Exemplo simples de salvar em um arquivo JSON
            try:
                with open('agendamentos.json', 'r') as arquivo:
                    agendamentos = json.load(arquivo)
            except FileNotFoundError:
                agendamentos = []

            agendamentos.append({
                'nome': nome,
                'data': data_hora_24h
            })

            with open('agendamentos.json', 'w') as arquivo:
                json.dump(agendamentos, arquivo, indent=4)

            return jsonify({'message': 'Agendamento realizado com sucesso!'})
        else:
            return jsonify({'message': 'Formato de data e hora inválido'}), 400
    else:
        return jsonify({'message': 'Nome e data e hora são obrigatórios'}), 400

if __name__ == '__main__':
    app.run(debug=True)