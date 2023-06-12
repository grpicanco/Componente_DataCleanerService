import json

import requests


class Regra:
    def __init__(self, ulr=None, data_criacao=None, data_modificacao=None, codigo=None, titulo=None, descricao=None,
                 tipo=None, script=None):
        self._url = ulr
        self._data_criacao = data_criacao
        self._data_modificacao = data_modificacao
        self._codigo = codigo
        self._titulo = titulo
        self._descricao = descricao
        self._tipo = tipo
        self._script = script

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def to_json(self):
        data = {
            'codigo': self._codigo,
            'titulo': self._titulo,
            'descricao': self._descricao,
            'tipo': self._tipo,
            'script': self._script
        }
        return json.dumps(data)

    def __str__(self):
        return f'{self._codigo}: {self._titulo}'


class AcaoDeCorrecao:
    def __init__(self, ulr=None, data_criacao=None, data_modificacao=None, codigo=None, titulo=None, descricao=None,
                 tipo=None, script=None):
        self._url = ulr
        self._data_criacao = data_criacao
        self._data_modificacao = data_modificacao
        self._codigo = codigo
        self._titulo = titulo
        self._descricao = descricao
        self._tipo = tipo
        self._script = script

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    def to_json(self):
        data = {
            'codigo': self._codigo,
            'titulo': self._titulo,
            'descricao': self._descricao,
            'tipo': self._tipo,
            'script': self._script
        }
        return json.dumps(data)

    def __str__(self):
        return f'{self._codigo}: {self._titulo}'


class ClearServiceComponent:
    def __init__(self):
        self._regras = {}
        self._acao_de_correcao = {}

    def listar_regras(self):
        """
        Lista todas as regras disponíveis.

        :return: Lista de regras.
        :raises Exception: Erro na requisição.
        """
        response = requests.get('http://localhost:8000/regras/')
        if response.status_code == 200:
            data = response.json()
            self._regras = {}

            for item in data:
                url = item.get('url')
                data_criacao = item.get('data_criacao')
                data_modificacao = item.get('data_modificacao')
                codigo = item.get('codigo')
                titulo = item.get('titulo')
                descricao = item.get('descricao')
                tipo = item.get('tipo')
                script = item.get('script')

                regra = Regra(url, data_criacao, data_modificacao, codigo, titulo, descricao, tipo, script)
                self._regras[codigo] = regra
            return list(self._regras.values())
        else:
            raise Exception(f'Erro na requisição: {response.status_code}')

    def detalhar_regra(self, codigo: str):
        """
        Detalha uma regra específica pelo código.

        :param codigo: Código da regra a ser detalhada.
        :return: Detalhes da regra.
        :raises Exception: Regra não encontrada.
        """
        if self._regras:
            regra = self._regras.get(codigo)
            if regra:
                return regra
            else:
                raise Exception(f'Regra com código {codigo} não encontrada.')
        else:
            self.listar_regras()
            return self.detalhar_regra(codigo)

    def listar_acao_de_correcao(self):
        """
        Lista todas as ações de correção disponíveis.

        :return: Lista de ações de correção.
        :raises Exception: Erro na requisição.
        """
        response = requests.get('http://localhost:8000/acaodecorrecao/')
        if response.status_code == 200:
            data = response.json()
            self._acao_de_correcao = {}

            for item in data:
                url = item.get('url')
                data_criacao = item.get('data_criacao')
                data_modificacao = item.get('data_modificacao')
                codigo = item.get('codigo')
                titulo = item.get('titulo')
                descricao = item.get('descricao')
                tipo = item.get('tipo')
                script = item.get('script')

                acao_de_correcao = AcaoDeCorrecao(url, data_criacao, data_modificacao, codigo, titulo, descricao, tipo,
                                                  script)
                self._acao_de_correcao[codigo] = acao_de_correcao
            return list(self._acao_de_correcao.values())
        else:
            raise Exception(f'Erro na requisição: {response.status_code}')

    def detalhar_acao_de_correcao(self, codigo):
        """
        Detalha uma ação de correção específica pelo código.

        :param codigo: Código da ação de correção a ser detalhada.
        :return: Detalhes da ação de correção.
        :raises Exception: Ação de correção não encontrada.
        """
        if self._acao_de_correcao:
            acao_de_correcao = self._acao_de_correcao.get(codigo)
            if acao_de_correcao:
                return acao_de_correcao
            else:
                raise Exception(f'Regra com código {codigo} não encontrada.')
        else:
            self.listar_acao_de_correcao()
            return self.detalhar_acao_de_correcao(codigo)

    def corrigir_dados(self, dados, cod_regras, cod_acao_de_correcao):
        """
        Corrige os dados com base nas regras e ações de correção fornecidas.

        :param dados: Dados a serem corrigidos.
        :param cod_regras: Lista de códigos das regras a serem aplicadas.
        :param cod_acao_de_correcao: Lista de códigos das ações de correção a serem aplicadas.
        :return: Resposta da requisição.
        :raises Exception: Erro na requisição.
                """
        regras = []
        acaos = []
        url = 'http://localhost:8000/correcaodedados/'
        headers = {'Content-Type': 'application/json'}
        for item in cod_regras:
            regra = self.detalhar_regra(item)
            regras.append(regra.url)

        for item in cod_acao_de_correcao:
            acao = self.detalhar_acao_de_correcao(item)
            acaos.append(acao.url)

        data = {
            'regras': regras,
            'acao_correcao': acaos,
            'dados': dados
        }
        data = json.dumps(data, separators=(",", ":"))
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response
        else:
            raise f'Erro na requisição: {response.status_code}'
