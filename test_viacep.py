import pytest
import requests


@pytest.fixture(scope='session')
def api_client():
    client = requests.Session()
    yield client
    client.close()


@pytest.fixture(scope='function')
def base_url():
    return "https://viacep.com.br/ws/"


class TestViaCEPCheckout:
    
    def test_cep_valido_endereco_existente(self, api_client, base_url):
        cep = "01310100"
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert "logradouro" in data
        assert "bairro" in data
        assert "localidade" in data
        assert data["logradouro"] != ""
        assert data["bairro"] != ""
        assert data["localidade"] != ""

    def test_cep_formato_correto_nao_existe(self, api_client, base_url):
        cep = "99999999"
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert "erro" in data
        error_value = data["erro"]
        assert error_value is True or error_value == "true"

    def test_cep_formato_invalido_com_letras(self, api_client, base_url):
        cep = "ABC12345"
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()
            assert "erro" in data
            assert data.get("erro") is True or data.get("erro") == "true"

    def test_cep_quantidade_incorreta_digitos(self, api_client, base_url):
        cep = "123"
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.json()
            assert "erro" in data
            assert data.get("erro") is True or data.get("erro") == "true"

    def test_cep_vazio(self, api_client, base_url):
        cep = ""
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code in [400, 404]

    def test_cep_valido_estrutura_resposta(self, api_client, base_url):
        cep = "20040020"
        url = f"{base_url}{cep}/json/"
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data.get("erro") != True
        campos_esperados = ["cep", "logradouro", "bairro", "localidade", "uf", "complemento"]
        for campo in campos_esperados:
            assert campo in data
        assert data["cep"] != ""
        assert data["uf"] != ""
        assert data["localidade"] != ""
