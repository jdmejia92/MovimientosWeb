from flask import render_template, request, redirect, url_for
from Balance import app

@app.route("/")
def inicio():
    lista_movimientos = []
    fichero_mv = open("data/movimientos.csv", "r")

    #----------------------------------------------------
    cab = fichero_mv.readline()
    linea = fichero_mv.readline()
    while linea != "":
        campos = linea.split(",")
        lista_movimientos.append(
            {
                "fecha": campos[0],
                "hora": campos[1],
                "concepto": campos[2],
                "es_ingreso": True if campos[3] == '1' else False,
                "cantidad": float(campos[4])
            }
        )

        linea = fichero_mv.readline()


    linea = fichero_mv.readline()

    fichero_mv.close()
    return render_template("lista_movimientos.html", 
                            movimientos = lista_movimientos)

@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("nuevo_movimiento.html")
    else:
        # recuperar los campos del request.form
        # grabar el nuevo registro en movimientos.csv
        return redirect(url_for("inicio"))