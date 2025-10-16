import json
from time import sleep
import requests

class auth():

    def __init__(self, base_url, access_token="", print_error=True):
        self.access_token = access_token
        self.base_url = base_url
        self.print_error = print_error

    def request(self, method="GET", url="", headers=None, params=None, data=None, files=None):

        req_params = params if params != None else {}
        req_headers = headers if headers != None else {}
        req_data = data if data != None else {}
        req_files = files if files != None else {}

        if self.access_token != "" and self.access_token != None:
            req_headers['Authorization'] = f'Bearer {self.access_token}'

        while True:

            match method:
                case "GET":
                    response = requests.get(url=url, params=req_params, headers=req_headers, data=req_data)
                case "PUT":
                    response = requests.put(url=url, params=req_params, headers=req_headers, data=req_data)
                case "POST":
                    response = requests.post(url=url, params=req_params, headers=req_headers, data=req_data, files=req_files)
                case "DELETE":
                    response = requests.delete(url=url, params=req_params, headers=req_headers, data=req_data)
                case "HEAD":
                    response = requests.head(url=url, params=req_params, headers=req_headers, data=req_data)
                case "OPTIONS":
                    response = requests.options(url=url, params=req_params, headers=req_headers, data=req_data)

            if response.status_code == 200 or response.status_code == 201:
                return response
            elif response.status_code != 429:
                if self.print_error:
                    print(f"""Erro no retorno da API do Questor Zen 2
Mensagem: {response.json()['message'] if 'message' in response.json() else ""}
URL: {url}
Metodo: {method}
Parametros: {req_params}
Headers: {req_headers}
Data: {req_data}
Resposta JSON: {response.json()}""")
                break
            else:
                sleep(5)

    def login(self, email, senha):
        """
        Realiza o login na API do Questor Zen 2 e obtém o token de acesso
        """
        #Descrição da função

        url = self.base_url+"/v2/Autenticacao/loginUsuario"

        headers = {'Content-Type': 'application/json'}

        data = json.dumps({
            "email": email,
            "senha": senha
        })

        response = self.request("POST", url=url, headers=headers, data=data)

        if response:

            response_json = response.json()

            if 'accessToken' in response_json['dados']:
                return response_json
            else:
                if self.print_error:
                    print(f"Erro ao obter o token de acesso: {response_json}")
                return {}
        
        else:
            return {}

class qdrive(auth):

    def importar_documento_fiscal(self, file_path):
        """
        Realiza a importação de documentos fiscais, incluindo NF-e, CT-e, CT-e OS, NFC-e, CF-e e seus respectivos eventos
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/v2/QDrive/DocumentosFiscais/Importar"

        files = {'documentos': open(file_path, 'rb')}

        try:
            response = self.request("POST", url=url, files=files)

            if response:
                return response.json()
            else:
                return {}
        finally:
            files['documentos'].close()
        
class edoc(auth):

    def consultar_pastas(self):
        """
        Realiza a consulta de pastas de documentos fiscais
        """
        #Descrição da função

        asct = True #Acesso Só Com Token

        if asct and (self.access_token == "" or self.access_token == None or type(self.access_token) != str):
            print("Token inválido")
            return {}

        url = self.base_url+f"/v2/EDoc/Pastas"

        response = self.request("GET", url=url)

        if response:

            return response.json()
        
        else:
            return {}
