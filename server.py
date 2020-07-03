from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify
from funcionalidades import gerenciar_bd

app = Flask("__name__")

@app.route("/")
def iniciar():
    return render_template("PÁGINA INICIO")

#Abaixo estão exemplos de como pegar os dados dos forms
#e fazer a chamada da função que opera sobre estes
#Qualquer duvida sobre qual função usar, me chamem

@app.route("/processar_salvar_cliente", methods=["POST"])
def processar_salvar_cliente():
    dados = {}
    dados["cpf"] = request.form["cpf"]
    dados["email"] = request.form["email"]
    dados["nome"] = request.form["nome"]
    dados["senha"] = request.form["senha"]
    dados["telefone"] = request.form["telefone"]
    #dados["imagem"] =
    #dados["idade"] =
    
    #Função que salva o cliente e retorna True ou False dependendo do sucesso da operacao
    if salvar_cliente(dados):
        return "OK"

@app.route("/processar_excluir_cliente")
def processar_excluir_cliente():
    cpf = request.form["cpf"]
    if excluir_cliente(cpf):
        return "OK"

@app.route("/processar_salvar_estabelecimento")
def processar_salvar_estabelecimento():
    dados = {}
    dados["cnpj"] = request.form["cnpj"]
    dados["email"] = request.form["email"]
    dados["nome_ficticio"] = request.form["nome_ficticio"]
    dados["senha"] = request.form["senha"]
    dados["telefone"] = request.form["telefone"]
    dados["local"] = request.form["local"]
    #dados["imagem"] =
    #dados["idade"] =
    
    if salvar_estabelecimento(dados):
        return "OK"