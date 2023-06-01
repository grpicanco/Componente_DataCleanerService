import requests


class Regra:
    def __init__(self, ulr, data_criacao, data_modificacao, codigo, titulo, descricao, tipo, script):
        self._url = ulr
        self._data_criacao = data_criacao
        self._data_modificacao = data_modificacao
        self._codigo = codigo
        self._titulo = titulo
        self._descricao = descricao
        self._tipo = tipo
        self._script = script

    def __str__(self):
        return f'{self._codigo}: {self._titulo}'


class Componente:
    def __init__(self):
        self._regras = {}

    def listar_regras(self):
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
        regra = self._regras.get(codigo)
        if regra:
            return regra
        else:
            raise Exception(f'Regra com código {codigo} não encontrada.')

    def criar_regra(self):
        pass

    def excluir_regra(self):
        pass
