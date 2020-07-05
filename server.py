import os
from playhouse.shortcuts import model_to_dict
from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify, session
from peewee import *
from funcionalidades.gerenciar_bd import *
from funcionalidades.funcoes_reserva import *
from funcionalidades.busca import *

app = Flask("__name__")

app.config["SECRET_KEY"] = '#afashg#'

@app.route("/")
def iniciar():
    return render_template("index.html")

@app.route("/salvar_cliente", methods=["POST"])
def processar_salvar_cliente():
    dados = {}
    dados["cpf"] = request.form["cpf"]
    dados["email"] = request.form["email"]
    dados["nome"] = request.form["nome"]
    dados["senha"] = request.form["senha"]
    dados["telefone"] = request.form["telefone"]
    dados["imagem"] = request.form["imagem"]
    dados["idade"] = int(request.form["idade"])
    
    for k,v in dados.items():
        if v == "":
            dados[k] = None

    if salvar_cliente(dados):
        return redirect(url_for("iniciar"))
    else:
        return "ERRO"

@app.route("/salvar_estabelecimento", methods=["POST"])
def processar_salvar_estabelecimento():
    dados = {}
    dados["cnpj"] = request.form["cnpj"]
    dados["email"] = request.form["email"]
    dados["nome_ficticio"] = request.form["nome_ficticio"]
    dados["senha"] = request.form["senha"]
    dados["telefone"] = request.form["telefone"]
    dados["local"] = request.form["local"]
    dados["imagem"] = request.form["imagem"]
    dados["avaliacao"] = None

    for k,v in dados.items():
        if v == "":
            dados[k] = None
    
    if salvar_estabelecimento(dados):

        dados_agenda = {}

        dias = ""
        partida = int(request.form["selecionarInicio"])
        chegada =  int(request.form["selecionarFim"])+1
        for i in range(partida,chegada):
            dias += str(i)

        dados_agenda["dias"] = dias
        dados_agenda["hora_inicio"] = request.form["hora_inicio"]
        dados_agenda["hora_termino"] = request.form["hora_termino"]
        dados_agenda["lotacao_maxima_permitida"] = int(request.form["lotacao_maxima_permitida"])

        if salvar_agenda(dados["cnpj"],dados_agenda):
            return redirect(url_for("iniciar"))
        return "Erro"
    return "Erro"

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]

    if tipo == "cliente":
        cliente = localizar_cliente(senha,email)
        if cliente:
            session['usuario'] = model_to_dict(cliente)
            session["tipo"] = tipo
            session["reserva"] = list(map(model_to_dict,Reserva.select().where(Reserva.cliente==cliente)))
            return redirect(url_for("iniciar"))
        return "Erro"
    else:
        estabelecimento = localizar_estabelecimento(email,senha)
        if estabelecimento:
            session['usuario'] =  model_to_dict(estabelecimento)
            session["reserva"] = list(map(model_to_dict,Reserva.select().where(Reserva.estabelecimento==estabelecimento)))
            session["tipo"] = tipo
            session["pratos"] = list(map(model_to_dict,localizar_pratos(estabelecimento.cnpj)))
            session["bebidas"] = list(map(model_to_dict,localizar_bebidas(estabelecimento.cnpj)))
            return redirect(url_for("iniciar"))
        return "Erro"

@app.route("/logout")
def logout():
    session.pop("usuario")
    session.pop("tipo")
    return redirect(url_for("iniciar"))

@app.route("/inserir_prato_bebida", methods=["POST"])
def inserir_prato_bebida():
    tipo = request.form["selecionarTipo"]
    cnpj = request.form["estabelecimento"]
    estabelecimento = Estabelecimento.select().where(Estabelecimento.cnpj==cnpj)[0]
    dados = {
        "nome": request.form["nome"],
        "preco": float(request.form["preco"]),
        "imagem": None,
        "descricao": request.form["descricao"],
        "ingredientes": request.form["ingredientes"],
        "dia_periodo": None,
        "avaliacao": None,
        "categorias": request.form["categorias"].split(","),
        "estabelecimento": estabelecimento
    }

    if tipo == "prato":
        if salvar_prato(dados):
            return redirect(url_for("iniciar"))
    else:
        if salvar_bebida(dados):
            return redirect(url_for("iniciar"))
    return "Erro"

@app.route("/excluir_prato")
def processar_excluir_prato():
    id = request.args.get("id")
    if excluir_prato(id):
        return redirect(url_for("iniciar"))
    return "Erro"

@app.route("/excluir_bebida")
def processar_excluir_bebida():
    id = request.args.get("id")
    if excluir_bebida(id):
        return redirect(url_for("iniciar"))
    return "Erro"

@app.route("/confirmar_reserva")
def confirmar_reserva():
    try:
        reserva = Reserva.get_by_id(request.args.get("id"))
        print("OII")
        reserva.confirmacao = True
        reserva.save()
        return redirect(url_for("iniciar"))
    except:
        return "Erro"

@app.route("/realizar_reserva", methods=["POST"])
def processar_reserva():
    cpf = request.form["cpf"]
    nome = request.form["nome_estabelecimento"]
    data = request.form["data_marcada"]
    horario_chegada = request.form["horario_chegada"]
    horario_saida = request.form["horario_saida"]
    qtd_pessoas = int(request.form["qtd_pessoas"])

    cliente = Cliente.select().where(Cliente.cpf==cpf)[0]
    estabelecimento = Estabelecimento.select().where(Estabelecimento.nome_ficticio==nome)[0]
    
    dados ={
        "estabelecimento":estabelecimento,
        "cliente":cliente,
        "qtd_pessoas":qtd_pessoas,
        "data_marcada":data,
        "horario_chegada":horario_chegada,
        "horario_saida":horario_saida,
    }

    try:
        if realizar_reserva(dados):
            return redirect(url_for("iniciar"))
    except:
        return "Erro"

@app.route("/buscar", methods=["POST"])
def buscar_algo():
    tipo = request.form["tipo"]
    buscatxt = request.form["buscatxt"]

    if tipo == "estabelecimento":
        try:
            resultado = buscar_estabelecimento_por_nome(buscatxt)
            session["tipo_busca"] = "estabelecimento"
            session["resultado"] = list(map(model_to_dict,resultado))
            return redirect(url_for("iniciar"))
        except:
            return "Erro"
    
    elif tipo == "prato":
        try:
            resultado = buscar_prato_por_nome(buscatxt)
            session["tipo_busca"] = "prato"
            session["resultado"] = list(map(model_to_dict,resultado))
            return redirect(url_for("iniciar"))
        except:
            return "Erro"

    else:
        try:
            resultado = buscar_bebida_por_nome(buscatxt)
            session["tipo_busca"] = "bebida"
            session["resultado"] = list(map(model_to_dict,resultado))
            return redirect(url_for("iniciar"))
        except:
            return "Erro"

@app.route("/filtrar_busca", methods=["POST"])
def filtrar_busca():
    if session["tipo_busca"] == "estabelecimento":
        
        estabelecimentos = session["resultado"]
        cidades = request.form["filtro"].split(",")
        resultado = []
        
        for i in estabelecimentos:
            if i["local"] in cidades:
                resultado.append(i)
        session["resultado"] = resultado
        return redirect(url_for("iniciar"))
            
        
    else:
        busca = session["resultado"]
        preco_min = request.form["preco_min"]
        preco_max = request.form["preco_max"]
        
        if preco_min != "": 
            preco_min = float(preco_min)
        else:
            preco_min = 0
        
        if preco_max != "":
            preco_max = float(preco_max)
        else:
            preco_max = 10000000

        resultado = []

        for i in busca:
            if i["preco"] >= preco_min and i["preco"] <= preco_max:
                resultado.append(i)

        session["resultado"] = resultado
        return redirect(url_for("iniciar"))

@app.route("/limpar_busca")
def limpar_busca():
    try:
        session.pop("resultado")
        return redirect(url_for("iniciar"))
    except:
        return "Erro"

@app.route("/excluir_cliente")
def processar_excluir_cliente():
    cpf = request.args.get("cpf")
    if excluir_cliente(cpf):
        return redirect(url_for("iniciar"))
    return "Erro"

@app.route("/excluir_estabelecimento")
def processar_excluir_estabelecimento():
    cnpj = request.args.get("cnpj")
    if excluir_estabelecimento(cnpj):
        return redirect(url_for("iniciar"))
    return "Erro"


app.run(debug=True)