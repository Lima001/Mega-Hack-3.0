from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify

app = Flask("__name__")

@app.route("/")
def iniciar():
    return render_template("PÁGINA INICIO")