from flask import render_template, request, redirect, url_for, flash
from Balance import app
from datetime import date

import csv

MOVEMENTS_FILE = "data/movements.csv"

@app.route("/")
def start():
    list_movements = []
    file_mv = open(MOVEMENTS_FILE, "r")
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
                "es_ingreso": True if campos[3] == 'on' else False,
                "cantidad": float(campos[4])
            }
        )

        line = file_mv.readline()

    line = file_mv.readline()

    file_mv.close()
    return render_template("list_movements.html", movements = list_movements)

@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("new_movement.html", data={})
    else:
        # recuperar los campos del request.form
        file_names = ['fecha', 'hora', 'concepto', 'es_ingreso', 'cantidad']

        """
        validar la entrada
            - No fechas/horas futuras
            - Fecha requerida
            - Fecha formato y valor correcto
            - Hora requerida
            - Hora formato y valor correcto
            - Concepto es requerido
            - Concepto max 100 car
            - es_ingreso: on / off

            - cantidad número mayor a cero
        """

        form_mv = dict(request.form)
        form_mv.pop('aceptar')

        amount = form_mv['cantidad']
        date_mv = form_mv['fecha']
        all_right = True

        try:
            amount = float(amount)
            if amount <= 0:
                flash("La cantidad debe ser positiva.")
                all_right = False
        except ValueError:
            flash("la cantidad debe ser numérica.")
            all_right = False

        try:
            date_mv = date.fromisoformat(date_mv)
            if date_mv > date.today():
                flash("La fecha no puede ser posterior a hoy.")
                all_right = False
        except ValueError as e:
            flash(f"Fecha incorrecta: {e}")
            all_right = False

        if not all_right:
            return render_template("new_movement.html", data = form_mv)

        # grabar el nuevo registro en movements.csv
        file_mv = open(MOVEMENTS_FILE, 'a', newline="")
        writer = csv.DictWriter(file_mv, fieldnames=file_names)
        d = dict(request.form)
        d.pop('aceptar')
        writer.writerow(d)
        file_mv.close()

        return redirect(url_for("start")) 