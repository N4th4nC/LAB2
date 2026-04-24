from flask import Flask, render_template, request, redirect
import sqlite3
import secrets
import datetime
import qrcode
import os

app = Flask(__name__)

BASE_URL = "https://SEU-APP.onrender.com"

# banco
def init_db():
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            usado INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🖥️ painel
@app.route('/')
def painel():
    return render_template("painel.html")

# gerar QR
@app.route('/gerar', methods=['POST'])
def gerar():
    token = secrets.token_urlsafe(16)

    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute("INSERT INTO tokens (token) VALUES (?)", (token,))
    conn.commit()
    conn.close()

    link = f"{BASE_URL}/form/{token}"

    # gerar QR
    img = qrcode.make(link)
    path = f"static/{token}.png"
    img.save(path)

    return render_template("painel.html", qr=path, link=link)

# abrir formulário
@app.route('/form/<token>')
def form(token):
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute("SELECT usado FROM tokens WHERE token=?", (token,))
    result = c.fetchone()
    conn.close()

    if not result or result[0] == 1:
        return "Link inválido ou já usado"

    return render_template("form.html", token=token)

# envio
@app.route('/submit/<token>', methods=['POST'])
def submit(token):
    nome = request.form.get('nome')

    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()

    c.execute("SELECT usado FROM tokens WHERE token=?", (token,))
    result = c.fetchone()

    if not result or result[0] == 1:
        conn.close()
        return "Link inválido"

    # salva resposta
    with open("respostas.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {nome}\n")

    # invalida token
    c.execute("UPDATE tokens SET usado=1 WHERE token=?", (token,))
    conn.commit()
    conn.close()

    return "Enviado com sucesso!"
    
if __name__ == "__main__":
    app.run()
