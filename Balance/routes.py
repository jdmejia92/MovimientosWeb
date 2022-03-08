from flask import render_template
from flask import render_template
from Balance import app

@app.route("/")
def inicio():
    return render_template("lista_movimientos.html")