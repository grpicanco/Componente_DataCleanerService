import os
import tempfile
import urllib.parse
import ast

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session

import script as sp
from components.DataCleanerServiceComponent import ClearServiceComponent

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

        # Codificar a lista de dicionários como uma string de consulta (query string)
        dados_codificados = urllib.parse.urlencode({'dados': corrigido, 'colunas': colunas})

        return redirect(url_for('main.tela_3', dados_corrigidos=dados_codificados))

    df_json = session.get('df_json')
    if df_json:
        df = pd.read_json(df_json)
        df = df.to_html(index=False, classes='table table-bordered')
    else:
        df = 'Sem dados'

    return render_template('tela_2.html', tabela=df)


@main_blueprint.route('/tela3')
def tela_3():
    # Obter os dados corrigidos da requisição anterior
    dados_corrigidos_json = request.args.get('dados_corrigidos')
    # Decodificar a string de consulta para obter os dados como uma lista de dicionários
    dados_decodificados = urllib.parse.parse_qs(dados_corrigidos_json)
    colunas = ast.literal_eval(dados_decodificados['colunas'][0])
    dados_corrigidos = ast.literal_eval(dados_decodificados['dados'][0])
    tabela_errada = []
    tabela_corrigida = []
    for item in dados_corrigidos:
        item['correto'] = [[index, value, 'correto'] for index, value in item['correto']]
        item['errado'] = [[index, value, 'errado'] for index, value in item['errado']]
        item['corrigido'] = [[index, value, 'corrigido'] for index, value in item['corrigido']]
        item['nao_corrigido'] = [[index, value, 'errado'] for index, value in item['nao_corrigido']]
        valores = item['correto'] + item['errado']
        tabela_errada.append(sp.ordena_dados(valores))
        valores = item['correto'] + item['corrigido'] + item['nao_corrigido']
        tabela_corrigida.append(sp.ordena_dados(valores))

    # Transformar os dados em um dicionário com as colunas como chaves
    tabela_errada_dict = list(map(list, zip(*tabela_errada)))
    tabela_corrigida_dict = list(map(list, zip(*tabela_corrigida)))

    # Cria dataframe Partir dos dicionarios.
    df_errada = pd.DataFrame(tabela_errada_dict, columns=colunas)
    df_corrigida = pd.DataFrame(tabela_corrigida_dict, columns=colunas)

    # Definir a função para formatar as células com a classe desejada

    # Aplicar a formatação às células do dataframe
    df_estilizado_errada = df_errada.applymap(lambda valor: formatar_celula(valor[1], valor[2]))
    df_estilizado_corrigido = df_corrigida.applymap(lambda valor: formatar_celula(valor[1], valor[2]))

    # Converter o dataframe estilizado em uma tabela HTML
    tabela_html_errada = df_estilizado_errada.to_html(index=False, escape=False)
    tabela_html_corrigido = df_estilizado_corrigido.to_html(index=False, escape=False)

    # Remover a classe "dataframe" e substituí-la por "table table-bordered table-dark"
    tabela_html_errada = tabela_html_errada.replace('class="dataframe"', 'class="table table-bordered niceTable"')
    tabela_html_corrigido = tabela_html_corrigido.replace('class="dataframe"', 'class="table table-bordered niceTable"')

    # Remover células vazias
    tabela_html_errada = tabela_html_errada.replace('<td><td', '<td').replace('</td></td>', '</td>')
    tabela_html_corrigido = tabela_html_corrigido.replace('<td><td', '<td').replace('</td></td>', '</td>')

    return render_template('tela_3.html', tabela_errada=tabela_html_errada, tabela_corrigida=tabela_html_corrigido)


@main_blueprint.route('/tela4')
def tela_4():
    # Obter os dados da requisição anterior (caso necessário)
    # Realizar as operações necessárias para gerar o arquivo a ser baixado
    # (por exemplo, criar um novo arquivo com os dados corrigidos)
    return render_template('tela_4.html')


def formatar_celula(valor, classe):
    return f'<td class="{classe}">{valor}</td>'