import pandas as pd
from flask import render_template, request, redirect, url_for, flash
from Balance import app
from datetime import date

import csv

MOVEMENTS_FILE = "data/movements.csv"
HEADERS = ["fecha", "hora", "concepto", "es_ingreso", "cantidad", "id"]

@app.route("/")
def start():  
    """Mostrar los movimientos, verificando que todo este correcto
    en el CSV"""
    try:
        list_movements = []
        file_mv = open(MOVEMENTS_FILE, "r")
        reader = csv.DictReader(file_mv, delimiter=",", quotechar='"')
        for campo in reader:
            list_movements.append(campo)
    except:
        return render_template('error404.html', message='archivo')

    file_mv.close()

    # Organizar los movimientos por fecha y hora, mas antiguo de primero
    new_list = sorted(list_movements, key=lambda d: (d['fecha'], d['hora']))
    return render_template("list_movements.html", movements = new_list)

#Borrar los movimientos
@app.route("/delete/<int:id>")
def delete(id):
    try:
        file = pd.read_csv(MOVEMENTS_FILE, delimiter=",")
        file_id = file[file.id != id]
        file_id.to_csv(MOVEMENTS_FILE, index=False)
        return redirect(url_for("start"))
    except:
        return render_template('error404.html', message='error_inesperado')

@app.route("/update/<int:id>")
def update(id):
    try:
        file_mv = open(MOVEMENTS_FILE, "r")
        reader = csv.DictReader(file_mv, delimiter=",", quotechar='"')
        return render_template("new_movement.html")
    except:
        return render_template('error404.html', message='error_inesperado')


@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("new_movement.html", data={})
    else:
        # recuperar los campos del request.form
        file_names = ['fecha', 'hora', 'concepto', 'es_ingreso', 'cantidad', 'id']

        """
        validar la entrada
            - No fechas/horas futuras
            - Fecha requerida
            - Fecha formato y valor correcto
            - Hora requerida
            - Hora formato y valor correcto
            - Concepto es requerido
            - Concepto max 100 car

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

        # Obtener ID
        file_ids = []
        with open(MOVEMENTS_FILE, 'r') as file_id:
            reader = csv.DictReader(file_id)
            for row in reader:
                row_id = row['id']
                file_ids.append(row_id)

        file_id.close()
        try:
            new_id = int(file_ids[-1]) + 1
        except:
            new_id = '1'

        # verificar on y off sean 1 y 0 respectivamente
        try:
            es_ingreso_form = dict(request.form)
            if es_ingreso_form['es_ingreso'] == 'on':
                new_es_ingreso = '1'
            else:
                new_es_ingreso = '0'
        except:
            new_es_ingreso = '0'
        
        # grabar el nuevo registro en movements.csv
        file_mv = open(MOVEMENTS_FILE, 'a', newline="")
        writer = csv.DictWriter(file_mv, fieldnames=file_names)
        d = dict(request.form)
        d.pop('aceptar')
        # grabar nuevo id y es_ingreso
        d.update({'id': str(new_id)})
        d.update({'es_ingreso': new_es_ingreso})
        writer.writerow(d)
        file_mv.close()

        return redirect(url_for("start"))