from flask import Flask, render_template, request, url_for, redirect
import database as DB
app = Flask(__name__)
database = DB.Database()


@app.route('/')
def Home():
    title = "Clinica Quiropractica"
    return render_template('home.html', title=title)


@app.route('/Paciente')
def Paciente():
    title = "Paciente"
    return render_template('Paciente.html', title=title)


@app.route('/inventario', methods=["POST", "GET"])
def Inventario():
    title = "Inventario"
    articulo = request.form.get("article")
    cantidad = request.form.get("amount")
    inventario = database.select_inventario_query()

    if "add" in request.form:
        database.modify_inventory_query(articulo,cantidad,'sumar')
        return redirect(url_for('Inventario'))
        return render_template('inventario.html', title=title, inventario=inventario)  
    
    elif "remove" in request.form:
        database.modify_inventory_query(articulo,cantidad,'restar')
        return redirect(url_for('Inventario'))
        return render_template('inventario.html', title=title, inventario=inventario)
    return render_template('inventario.html', title=title, inventario=inventario)



@app.route('/Paciente/ver-paciente', methods=["POST"])
def ver_paciente():
    title = "Información de Paciente"
    firstname= request.form.get("inputname")
    lastname= request.form.get("inputlastname")
    celphone= request.form.get("inputcelphone")
    birthdate= request.form.get("inputbirthdate")
    address= request.form.get("inputaddress")
    
    if "search" in request.form:
        paciente = database.select_paciente_query(firstname,lastname,celphone)
        if paciente:
            reportes = database.select_reporte_query()
        elif  not paciente:
            error_statement = "Ese paciente no existe..."
            return render_template('Paciente.html', error_statement=error_statement)

        return render_template('ver_paciente.html', title=title, paciente=paciente, reportes=reportes)

    elif "insert" in request.form:
        validate = database.insert_paciente_query(firstname,lastname,birthdate,celphone,address)
        if validate == False:
            error_statement = "Error insertando paciente..."
            return render_template('Paciente.html', error_statement=error_statement)

        return render_template('Paciente.html', title=title)

@app.route('/Paciente/ver-paciente/crear-reporte', methods=["GET", "POST"])
def Reporte():
    title = "Crear Reporte"
    reporte = request.form.get("nota")
    if "save" in request.form:
        print(reporte)
        database.insertar_reportes_query(reporte)
        return redirect(url_for('Inventario'))
    
    return render_template('reporte.html', title=title)   



if __name__ == '__main__':
    
    app.run(debug=True)

#conda activate my_flask_env
#set FLASK_APP=gui.py
#set FLASK_DEBUG=1
#-m flask run