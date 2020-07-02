# Este modulo acrescenta funcionalidades de segurança que podem
# ser importadas e usadas na plataforma para verificar estabilidade dos dados

import hashlib
import re

#Necessita ser implementado
#Usar RegEx
def cpf_valido(cpf:str) -> bool:
    pass

def cnpj_valido(cnpj:str) -> bool:
    pass

def email_valido(email:str) -> bool: 
    '''
    Verifica se a cadeia de caracteres passada como entrada
    consiste em um formato válido do tipo ...@gmail.com
    Retorna o valor lógico True em caso de sucesso, e 
    False em caso de erro  
    '''
    padrao = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    if re.search(padrao, email):
        return True
    return False

#Necessário implementar BD para testar função
def verificar_email(email:str, lista_email:object) -> bool:
    '''
    Verifica se o email informado está presente na base de dados (Objeto retornado pela Consulta Peewee)
    Retorna um valor Lógico True caso o email corresponda a lista de email salvos, 
    caso contrário retorna False
    '''
    for i in lista_email:
        if i == email:
            return True
    return False

def gerar_senha(senha:str) -> str: #Testada e funcional
    '''
    Retorna o hash da senha passada como entrada para eventual gravação na base de dados
    '''
    gerador = hashlib.sha512()
    gerador.update(senha.encode("utf-8"))
    return gerador.hexdigest()

def verificar_senha(senha:str, padrao_hash:str) -> bool: #Testada e Funcional
    '''
    Verifica se a senha informada confere com o hash passado (Pegar hash da base de dados)

    Retorna True caso sejam compatíveis, caso contrário retorna False
    '''
    senha = gerar_senha(senha)
    return senha == padrao_hash

if __name__ == "__main__":
    senha = gerar_senha(input("Digite uma senha: "))
    print("Hash:", senha)
