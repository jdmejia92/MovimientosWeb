import pandas as pd
from flask import render_template, request, redirect, url_for, flash
from Balance import app
from datetime import date, datetime


import csv

MOVEMENTS_FILE = "data/movements.csv"
HEADERS = ['fecha', 'hora', 'concepto', 'es_ingreso', 'cantidad', 'id']

@app.route("/")
def start():  
    """Mostrar los movimientos, formateando al gusto"""
    try:
        list_movements = []
        file_mv = open(MOVEMENTS_FILE, "r")
        reader = csv.DictReader(file_mv, delimiter=",", quotechar='"')
        for campo in reader:
            # Mostrar la cantidad en el formato deseado
            amount = "${:0,.2f}".format(float(campo['cantidad']))
            old_time = datetime.strptime(campo['hora'],'%H:%M')
            new_time = datetime.strftime(old_time, '%I:%M %p')
            old_date = datetime.strptime(campo['fecha'], '%Y-%m-%d')
            new_date = datetime.strftime(old_date, '%d-%m-%Y')
            campo.update({'cantidad': amount})
            campo.update({'hora': new_time})
            campo.update({'fecha': new_date})
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
        file = pd.read_csv(MOVEMENTS_FILE, delimiter=",", quotechar='"')
        file_id = file[file.id != id]
        file_id.to_csv(MOVEMENTS_FILE, index=False)
        return redirect(url_for("start"))
    except:
        return render_template('error404.html', message='error-inesperado')

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == 'GET':
        # Recuperar los datos a actualizar
        file_mv = pd.read_csv(MOVEMENTS_FILE, delimiter=",", quotechar='"')
        file_id = file_mv[file_mv.id == id]
        new_file = file_id.to_dict('records')
        data_to_update = new_file[0]
        return render_template("new_movement.html", data=data_to_update)
    else:
        # Actualizar el archivo con la fila con el mismo id
        file_mv = pd.read_csv(MOVEMENTS_FILE, delimiter=",", quotechar='"')
        row_id = file_mv['id'] == id
        update_row = dict(request.form)
        amount = update_row['cantidad']
        time_mv = update_row['hora']
        date_mv = update_row['fecha']
        concept_mv = update_row['concepto']
        all_right = True
        
        #Validaciones
        try:
            amount = float(amount)
            if amount <= 0:
                flash("La cantidad debe ser positiva.")
                all_right = False
        except ValueError:
            flash("la cantidad debe ser numérica.")
            all_right = False

        try:
            in_time = datetime.strptime(time_mv,'%H:%M')
            time_mv = in_time.time()
            today = date.fromisoformat(date_mv)
            if today <= date.today() and time_mv > datetime.now().time() or today > date.today() and time_mv > datetime.now().time():
                flash("La hora no puede ser posterior a la actual")
                all_right = False
        except:
            flash("Se debe ingresar un horario")
            all_right = False

        try:
            date_mv = date.fromisoformat(date_mv)
            if date_mv > date.today():
                flash("La fecha no puede ser posterior a hoy.")
                all_right = False
        except ValueError as e:
            flash(f"Formato de la fecha incorrecta: {e}")
            all_right = False

        if concept_mv == "":
            flash("El concepto no debe estar vacio")
            all_right = False
        elif len(concept_mv) >= 100:
            flash("El concepto no puede tener mas de 100 caracteres")
            all_right = False

        if not all_right:
            return render_template("new_movement.html", data=update_row, id=id, error=1)

        update_row.pop('aceptar')
        update_row.pop('cantidad')
        status = request.form.get('es_ingreso')
        if status == 'on' or status == '1':
            new_es_ingreso = '1'
        else:
            new_es_ingreso = '0'
        update_row.update({'es_ingreso': new_es_ingreso})
        update_row.update({'cantidad': amount})
        update_row.update({'id': id})
        file_mv.loc[row_id, HEADERS] = list(update_row.values())
        file_mv.to_csv(MOVEMENTS_FILE, index=False)
        return redirect(url_for("start"))

@app.route("/alta", methods=["GET", "POST"])
def alta():
    if request.method == 'GET':
        return render_template("new_movement.html", data={}, new=1)
    else:
        # recuperar los campos del request.form
        form_mv = dict(request.form)
        form_mv.pop('aceptar')

        amount = form_mv['cantidad']
        date_mv = form_mv['fecha']
        time_mv = form_mv['hora']
        concept_mv = form_mv['concepto']

        all_right = True

        # Validaciones

        # Cantidad
        try:
            amount = float(amount)
            if amount <= 0:
                flash("La cantidad debe ser positiva.")
                all_right = False
        except ValueError:
            flash("la cantidad debe ser numérica.")
            all_right = False

        # Hora
        try:
            in_time = datetime.strptime(time_mv,'%H:%M')
            time_mv = in_time.time()
            today = date.fromisoformat(date_mv)
            if today <= date.today() and time_mv > datetime.now().time() or today > date.today() and time_mv > datetime.now().time():
                flash("La hora no puede ser posterior a la actual")
                all_right = False
        except:
            flash("Se debe ingresar un horario")
            all_right = False

        # Fecha
        try:
            date_mv = date.fromisoformat(date_mv)
            if date_mv > date.today():
                flash("La fecha no puede ser posterior a hoy.")
                all_right = False
        except ValueError as e:
            flash(f"Formato de la fecha incorrecta: {e}")
            all_right = False

        # Concepto
        if concept_mv == "":
            flash("El concepto no debe estar vacio")
            all_right = False
        elif len(concept_mv) >= 100:
            flash("El concepto no puede tener mas de 100 caracteres")
            all_right = False

        if not all_right:
            return render_template("new_movement.html", data = form_mv, new=1)

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

        status = form_mv.get('es_ingreso')
        if status == 'on':
            new_es_ingreso = '1'
        else:
            new_es_ingreso = '0'

        # grabar el nuevo registro en movements.csv
        file_mv = open(MOVEMENTS_FILE, 'a', newline="")
        writer = csv.DictWriter(file_mv, fieldnames=HEADERS)
        d = dict(request.form)
        d.pop('aceptar')

        # grabar nuevos valores con los formatos deseados
        d.update({'id': str(new_id)})
        d.update({'es_ingreso': new_es_ingreso})
        print(d)
        writer.writerow(d)
        file_mv.close()

        return redirect(url_for("start"))