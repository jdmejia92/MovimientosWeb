from flask import render_template, request, redirect, url_for
from Balance import app

@app.route("/")
def start():
    list_movements = []
    file_mv = open("data/movements.csv", "r")

    #----------------------------------------------------
    cab = file_mv.readline()
    line = file_mv.readline()
    while line != "":
        campos = line.split(",")
        list_movements.append(
            {
                "fecha": campos[0],
                "hora": campos[1],
                "concepto": campos[2],
                "es_ingreso": True if campos[3] == '1' else False,
                "cantidad": float(campos[4])
            }
        )

        line = file_mv.readline()

    file_mv.close()
    return render_template("list_movements.html", movements = list_movements)

@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("new_movement.html")
    else:
        # recuperar los campos del request.form
        # grabar el nuevo registro en movimientos.csv
        return redirect(url_for("start"))