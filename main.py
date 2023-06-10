# This is a sample Python script.
import os
import subprocess
from typing import List

import pandas as pd
import xlsxwriter

from Componente import *

componente = Componente()


def ler_tabela(path):
    """
    Lê um arquivo de tabela (CSV, Excel, ODT ou ODS) e retorna um DataFrame do pandas.

    :param path: Caminho do arquivo.
    :return: DataFrame do pandas contendo os dados da tabela.
    :raises ValueError: Formato de arquivo inválido. Apenas arquivos CSV, Excel, ODT e ODS são suportados.
    :raises FileNotFoundError: Arquivo não encontrado.
    :raises Exception: Erro ao ler o arquivo.
    """
    try:
        if path.endswith('.csv'):
            # Ler arquivo CSV
            df = pd.read_csv(path, delimiter=',')
        elif path.endswith(('.xls', '.xlsx')):
            # Ler arquivo Excel
            df = pd.read_excel(path)
        elif path.endswith('.odt') or path.endswith('.ods'):
            # Obter o nome do arquivo sem a extensão
            nome_arquivo, extensao = os.path.splitext(path)

            # Converter para CSV usando o LibreOffice
            csv_path = nome_arquivo + '.csv'
            subprocess.call(['soffice', '--headless', '--convert-to', 'csv', '--outdir', '.', path])

            # Ler arquivo CSV convertido usando o pandas
            df = pd.read_csv(csv_path, delimiter=',')

            # Remover o arquivo CSV convertido
            subprocess.call(['rm', csv_path])
        else:
            raise ValueError('Formato de arquivo inválido. Apenas arquivos CSV, Excel, ODT e ODS são suportados.')

        return df
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {path}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

    return None


def obter_lista_colunas(dataframe) -> tuple[List, List]:
    """
    Transforma as colunas do DataFrame em linhas e retorna uma lista dos valores por coluna.

    :param dataframe: DataFrame do pandas.
    :return: Lista de valores por coluna do DataFrame.
    """
    colunas = dataframe.columns.tolist()
    df = dataframe.fillna('-').transpose().values.tolist()
    return df, colunas


def main():
    path = '~//Documentos//Untitled_1.csv'
    df = ler_tabela(path)
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
    lista_dados, colunas = obter_lista_colunas(df)
    item = 0
    for dado in lista_dados:
        dado = componente.corrigir_dados(dados=dado, cod_regras=regras.get(item), cod_acao_de_correcao=acao.get(item))
        corrigido.append(dado.json())
        item += 1
    print(corrigido)
    df = pd.DataFrame(columns=colunas)
    coluna_index = 0
    for item in corrigido:
        for row in item['dados']:
            index, values = row
            if len(df) <= index:
                df.loc[index] = [None] * len(colunas)
            df.iloc[index, coluna_index] = values if values is not None and values != '' else '-'
        coluna_index += 1

    print(type(df))
    nome_arquivo = 'Novo.csv'

    # Escreva o DataFrame no arquivo Excel
    df.to_csv(nome_arquivo, index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
