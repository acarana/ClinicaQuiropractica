from flask import Flask, render_template, request
import database as DB
app = Flask(__name__)
database = DB.Database()

@app.route('/Paciente')
def Paciente():
    title = "Paciente"
    return render_template('Paciente.html', title=title)



@app.route('/inventario')
def Inventario():
    title = "Inventario"
    return render_template('inventario.html', title=title)



@app.route('/Paciente/ver-paciente', methods=["POST"])
def ver_paciente():
    title = "Información de Paciente"
    firstname= request.form.get("inputname")
    lastname= request.form.get("inputlastname")
    celphone= request.form.get("inputcelphone")
    birthdate= request.form.get("inputbirthdate")
    address= request.form.get("inputaddress")
    paciente,reporte = database.select_paciente_query(firstname,lastname,celphone)

    if  not paciente or not reporte:
        error_statement = "Ese paciente no existe..."
        return render_template('Paciente.html', error_statement=error_statement)

    for row in paciente:
        firstname=row[1]
        lastname=row[2]
        birthdate=row[3]
        celphone=row[4]
        address=row[5]
    print(paciente)
    return render_template('ver_paciente.html', title=title, paciente=paciente)



if __name__ == '__main__':
    
    app.run(debug=True)

#conda activate my_flask_env
#set FLASK_APP=gui.py
#set FLASK_DEBUG=1
#-m flask run