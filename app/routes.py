import os
import tempfile

from flask import Blueprint, render_template, request, redirect, url_for, session
import pandas as pd
from components.ClearServiceComponent import ClearServiceComponent
import script as sp

main_blueprint = Blueprint('main', __name__)

componente = ClearServiceComponent()


@main_blueprint.route('/', methods=['GET', 'POST'])
def tela_1():
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        nome_arquivo = arquivo.filename
        temp_dir = tempfile.gettempdir()
        caminho_temporario = os.path.join(temp_dir, nome_arquivo)
        arquivo.save(caminho_temporario)

        df = sp.ler_tabela(caminho_temporario)
        session['df_json'] = df.to_json()
        return redirect(url_for('main.tela_2'))
    return render_template('tela_1.html')


@main_blueprint.route('/tela2', methods=['GET', 'POST'])
def tela_2():
    if request.method == 'POST':

        df_json = session.get('df_json')
        df = pd.read_json(df_json)
        regras = {
            0: ["RG001"],  # Id
            1: ['RG006'],  # Nome
            2: ['RG002'],  # Sexo
            3: ['RG001'],  # Altura(cm)
            4: ['RG004']  # Dt nascimento
        }
        acao = {
            0: ['AC001', 'AC002'],
            1: ['AC003'],
            2: ['AC004', 'AC005'],
            3: ['AC006', 'AC009', 'AC007'],
            4: ['AC008']
        }
        corrigido = []
        lista_dados, colunas = sp.obter_lista_colunas(df)
        item = 0
        for dado in lista_dados:
            dado = componente.corrigir_dados(dados=dado, cod_regras=regras.get(item),
                                             cod_acao_de_correcao=acao.get(item))
            corrigido.append(dado.json())
            item += 1
        return redirect(url_for('main.tela_3', dados_corrigidos=corrigido, colunas=colunas))

    df_json = session.get('df_json')
    if df_json:
        df = pd.read_json(df_json)
        df = df.to_html(index=False, classes='table table-bordered table-dark')
    else:
        df = 'Sem dados'

    return render_template('tela_2.html', tabela=df)


@main_blueprint.route('/tela3')
def tela_3():
    # Obter os dados corrigidos da requisição anterior
    dados_corrigidos = request.args.get('dados_corrigidos')
    colunas = request.args.get('colunas')
    for item in dados_corrigidos:
        coluna = 0
        for item in dados_corrigidos:
            item['correto'] = [[index, value, 'correto'] for index, value in item['correto']]
            item['errado'] = [[index, value, 'errado'] for index, value in item['errado']]
            valores = item['correto'] + item['errado']
            valores = sp.ordena_dados(valores)
    return render_template('tela_3.html', dados_corrigidos=dados_corrigidos)


@main_blueprint.route('/tela4')
def tela_4():
    # Obter os dados da requisição anterior (caso necessário)
    # Realizar as operações necessárias para gerar o arquivo a ser baixado
    # (por exemplo, criar um novo arquivo com os dados corrigidos)
    return render_template('tela_4.html')
