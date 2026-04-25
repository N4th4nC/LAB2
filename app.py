from flask import Flask, render_template, request
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://qfivgluqageacqgawfdj.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_-PBfQDu9c08W-OLPPfnLIw_KrJ1_Xuv"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔗 abrir formulário
@app.route('/form/<token>')
def form(token):
    res = supabase.table("tokens").select("*").eq("token", token).execute()

    if not res.data or res.data[0]["usado"]:
        return "Token inválido ou já usado"

    return render_template("form.html", token=token)

# 📩 enviar formulário
@app.route('/submit/<token>', methods=['POST'])
def submit(token):
    nome = request.form["nome"]

    # salva resposta
    supabase.table("respostas").insert({
        "token": token,
        "nome": nome
    }).execute()

    # marca token como usado
    supabase.table("tokens").update({
        "usado": True
    }).eq("token", token).execute()

    return "Enviado com sucesso!"

if __name__ == "__main__":
    app.run()
