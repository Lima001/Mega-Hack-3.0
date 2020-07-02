from funcionalidades.classes import *
from funcionalidades.seguranca import *

db.connect()

#Teste encriptar Senha
#Esperado: Uma senha ilegivel (Um hash)
minha_senha = "#MuitoDificilH@H@"
padrao_hash = gerar_senha(minha_senha)
print("1º Teste: ", padrao_hash, end="\n"*2)

#Teste verificar se Senha bate
#Esperado: True
print("2º Teste: ", verificar_senha(minha_senha, padrao_hash), end="\n"*2)

#Achar email no BD
#Esperado: True
emails = Estabelecimento.select(Estabelecimento.email)
print("3º Teste: ", verificar_email("ItaliaC.Contato@gmail.com",emails), end="\n"*2)

#Verificar se o email esta em formato valido
#Esperado: Depende conforme entrada (True or False)
seu_email = input("Digite um email valido: ")
print("4º Teste: ", email_valido(seu_email), end="\n"*2)

#Verificar cpf valido
#Esperado: Depende da entrada
#Valor de Teste 272.396.372-12 - Esperado True
print("5º Teste Valor Pré-definido: ", cpf_valido("272.396.372-12"))
seu_cpf = input("Digite um cpf valido: ")
print("5º Teste: ", cpf_valido(seu_cpf), end="\n"*2)