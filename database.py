import sys
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
from tkinter import *
from tkinter import ttk


#Dictionary for mapping
Patient = {
    'ID': '',
    'name': '',
    'lastname': '',
    'celphone': '',
    'birthdate': '',
    'address': ''
}

#DATABASE---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Exception Handling
def print_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno

    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    #psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    #print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

#Check if patient is in database and if so, saves ID
def select_paciente_query():

    select_id_Query = """SELECT paciente_id 
                         FROM paciente
                         WHERE nombre = '%s' AND apellido = '%s' AND telefono = '%s'""" %(Patient['name'], Patient['lastname'], Patient['celphone'])
    try:
        cursor.execute(select_id_Query)
        ID = cursor.fetchall()
        Patient['ID'] = ID[0]  #Add ID input to dictionary
    except Exception as err:
        print_psycopg2_exception(err)
        print('No se pudo encontrar al paciente')
    else:
        print_paciente_query() 


#SELECT and PRINT patient information
def print_paciente_query():
    
    Select_Paciente_Query = """SELECT * 
                                 FROM paciente
                                 WHERE nombre = '%s' AND apellido = '%s' AND telefono = '%s'""" %(Patient['name'], Patient['lastname'], Patient['celphone'])
    cursor.execute(Select_Paciente_Query)
    paciente = cursor.fetchall()

    print("Paciente: ")
    for row in paciente:
       print("paciente_id = ", row[0])
       print("nombre = ", row[1])
       print("apellido  = ", row[2])
       print("fecha_nacimiento  = ", row[3])
       print("telefono  = ", row[4])
       print("direccion = ", row[5], "\n")


    select_reporte_query(paciente)
    
#SELECT all reports from a specific patient
def select_reporte_query(paciente):
    
    Select_Reporte_Query = """SELECT * FROM reporte WHERE reporte_id IN 
                             (SELECT reporte_id FROM historial WHERE paciente_id = %s)""" %(Patient['ID'])
    try:
        cursor.execute(Select_Reporte_Query)
        reporte = cursor.fetchall()
    except(Exception,psycopg2.Error) as error:
        if (connection):
            print('No se pudo encontrar los reportes del paciente')
    else:

        print("Reporte: ")
        for row in reporte:
            print('reporte_id = ', row[0])
            print('fecha_creado = ', row[1])
            print('nota = ', row[2], '\n')

        #mostrar paciente en GUI   
        mostrar_paciente(paciente,reporte)

#Insert a new patient into database
def insert_paciente_query():
   
    Insert_Paciente_Query = """INSERT INTO paciente(nombre,apellido,fecha_nacimiento,telefono,direccion)
                               VALUES
                               ('%s', '%s', '%s', '%s', '%s')""" %(Patient['name'],Patient['lastname'],Patient['birthdate'],Patient['celphone'],Patient['address'])
    
    try:
        cursor.execute(Insert_Paciente_Query)
        connection.commit()
        count = cursor.rowcount
        print(count, "Paciente insertado exitosamente a tabla de paciente")
    except Exception as err:
        print_psycopg2_exception(err)
        print('No se pudo insertar al paciente')


#Insert a new report for selected patient
def insertar_reportes_query(report):
    #query para crear reporte
    #query para update historial
    
    Crear_Reporte_Query = """INSERT INTO reporte(fecha_creado,nota)
                             VALUES (CURRENT_TIMESTAMP,'%s') """ %(report)

    try:
        cursor.execute(Crear_Reporte_Query)
        connection.commit()
        print('Reporte insertado exitosamente a tabla de reporte')
    except(Exception,psycopg2.Error) as error:
        if (connection):
            print('Error en insertar reporte a tabla de reporte')
    else:
        update_historial_query()

#Update the history of the patient to reflect the last report created
def update_historial_query():

    Update_Historial_Query = """INSERT INTO historial(paciente_id,reporte_id)
                                VALUES ('%s',(SELECT MAX(reporte_id) FROM reporte))""" %(Patient['ID'])

    try:
        cursor.execute(Update_Historial_Query)
        connection.commit()
        print('Historial actualizado exitosamente')
    except(Exception,psycopg2.Error) as error:
        if (connection):
            print('Error en actualizar al historial')

def select_inventario_query():
    
    Select_Inventario_Query = '''SELECT articulo,cantidad FROM inventario
                                 ORDER BY inventario_id'''

    try:
        cursor.execute(Select_Inventario_Query)
        inventario = cursor.fetchall()
    except Exception as err:
        print_psycopg2_exception(err)
        print('No se pudo encontrar el inventario')
    else:
        return inventario
    
def modify_inventory_query(articulo, cantidad_sumar,modify):
    
    AddToInventory_query = '''UPDATE inventario
                              SET cantidad = cantidad + '%s'
                              WHERE articulo = '%s' ''' %(cantidad_sumar,articulo)
    SubToInventory_query = '''UPDATE inventario
                              SET cantidad = cantidad - '%s'
                              WHERE articulo = '%s' ''' %(cantidad_sumar,articulo)
    
    try:
        if(modify == 'sumar'):
            cursor.execute(AddToInventory_query)
            print('%s %s añadidos al inventario'%(cantidad_sumar,articulo)) 
        elif(modify=='restar'):
            cursor.execute(SubToInventory_query)
            print('%s %s restados al inventario'%(cantidad_sumar,articulo)) 
        connection.commit()
    except Exception as err:
        print_psycopg2_exception(err)
        if(modify == 'sumar'):
            print('No se pudo añadir al inventario')
        elif(modify=='restar'):
            print('No se pudo restar al inventario')


        


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#GUI----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Start of program
def main_GUI_window():

    root = Tk()
    root.title('Clinica Quiropractica')
    root.iconbitmap('Logo.ico')
    root.geometry('400x400')

    Paciente_btn = Button(root,text = 'Paciente', command=Open_Paciente).pack(fill = BOTH, expand = 1)
    Inventario_btn = Button(root,text = 'Inventario', command=Open_Inventario).pack(fill = BOTH, expand = 1)

    #insertar_reportes()

    root.mainloop()

#Window for dealing with patient
def Open_Paciente():
    top = Toplevel()
    top.title('Seleccionar Paciente')
    top.resizable(False,False)
    top.iconbitmap('Logo.ico')
    
    def on_entry_click(event): 
        if name.get() == 'Fulano':
            name.delete(0,'end')
        elif lastname.get() == 'Detal':
            lastname.delete(0,'end')
        elif celphone.get() == '1234567890':
            celphone.delete(0,'end')

        elif birthdate.get() == 'YYYY-MM-DD':
            birthdate.delete(0,'end')
        elif address.get() == 'Algun lugar por ahi':
            address.delete(0,'end')
        else:
            return
        
    #text boxes
    name = Entry(top,width=30)
    name.grid(row=0, column=1, padx=20)
    name.insert(0,'Fulano')
    name.bind('<FocusIn>', on_entry_click)

    lastname = Entry(top,width=30)
    lastname.grid(row=1, column=1)
    lastname.insert(0,'Detal')
    lastname.bind('<FocusIn>', on_entry_click)

    celphone = Entry(top,width=30)
    celphone.grid(row=2, column=1)
    celphone.insert(0,'1234567890')
    celphone.bind('<FocusIn>', on_entry_click)

    birthdate = Entry(top,width=30)
    birthdate.grid(row=3,column=1)
    birthdate.insert(0,'YYYY-MM-DD')
    birthdate.bind('<FocusIn>', on_entry_click)

    address = Entry(top,width=30)
    address.grid(row=4,column=1)
    address.insert(0,'Algun lugar por ahi')
    address.bind('<FocusIn>', on_entry_click)

    #text box labels
    name_label = Label(top,text='Nombre').grid(row=0, column=0)
    lastname_label = Label(top,text='Apellido').grid(row=1, column=0)
    celphone_label = Label(top,text='Telefono').grid(row=2, column=0)
    birthdate_label = Label(top,text='Fecha Nacimiento').grid(row=3, column=0)
    address_label = Label(top,text='Direccion Fisica').grid(row=4, column=0)

    #search button
    search_btn = Button(top, text='Buscar Paciente', command=lambda: buscar_paciente(name.get(),lastname.get(),celphone.get()))
    search_btn.grid(row=6,column=0,columnspan=2, pady=10,padx=10,ipadx=100)

    #insert button
    insert_btn = Button(top, text='Insertar Paciente', command=lambda: insertar_paciente(name.get(),lastname.get(),birthdate.get(),celphone.get(),address.get()))
    insert_btn.grid(row=7,column=0,columnspan=2, pady=5,padx=10,ipadx=100)

#Adds input about patient into dictionary
def buscar_paciente(name,lastname,celphone):
    #Add input to dictionary
    Patient['name'] = name
    Patient['lastname'] = lastname
    Patient['celphone'] = celphone
    select_paciente_query()
    print(Patient)

#Adds input of to-be-patient to the dictionary
def insertar_paciente(name,lastname,birthdate,celphone,address):
    #Add input to dictionary
    Patient['name'] = name
    Patient['lastname'] = lastname
    Patient['celphone'] = celphone
    Patient['birthdate'] = birthdate
    Patient['address'] = address
    insert_paciente_query()
    print(Patient)

#Window to show Patient information and his History of reports
def mostrar_paciente(paciente,reporte):
    top = Toplevel()
    top.title('Paciente')
    top.geometry('930x500')
    top.resizable(False,False)
    top.iconbitmap('Logo.ico')

    frm = Frame(top)
    frm.pack(side=TOP,padx=20)

    #Label for patient table
    paciente_label = Label(frm,text='Paciente')
    paciente_label.pack(side=TOP)
    paciente_label.config(font=("Courier", 44))

    #Table por patient
    pac = ttk.Treeview(frm,columns=(1,2,3,4,5,6),show='headings',height='2')
    pac.pack(side=TOP,fill=X)
    
    pac.column(1,width=80,minwidth=50)
    pac.column(2,width=80,minwidth=50)
    pac.column(3,width=100,minwidth=70)
    pac.column(4,width=120,minwidth=100)
    pac.column(5,width=100,minwidth=70)
    pac.column(6,width=400,minwidth=200)

    pac.heading(1,text='ID',anchor=W)
    pac.heading(2,text='Nombre',anchor=W)
    pac.heading(3,text='Apellido',anchor=W)
    pac.heading(4,text='Fecha Nacimiento',anchor=W)
    pac.heading(5,text='Telefono',anchor=W)
    pac.heading(6,text='Direccion',anchor=W)

    for row in paciente:
        pac.insert('', 'end', values=row)

    #label for historial table
    reporte_label = Label(frm,text='Historial')
    reporte_label.pack(side=TOP)
    reporte_label.config(font=("Courier", 44))

    #Tabla for report
    rep = ttk.Treeview(frm,columns=(1,2,3),show='headings',height='9')
    rep.pack(side=TOP,fill=X)

    rep.column(1,width=80,minwidth=50)
    rep.column(2,width=80,minwidth=50)
    rep.column(3,width=400,minwidth=200)

    rep.heading(1,text='ID',anchor=W)
    rep.heading(2,text='Fecha Creado',anchor=W)
    rep.heading(3,text='Nota',anchor=W)

    for row in reporte:
        rep.insert('', 'end', values=row)

    #Create Report Button
    create_report_btn = Button(top, text='Crear Reporte', command=insertar_reportes)
    create_report_btn.pack(side=TOP,pady=20,padx=10)

#Window to create another Report and save it
def insertar_reportes():
    top = Toplevel()
    top.title('Crear Reporte')
    top.geometry('650x500')
    top.resizable(False,False)
    top.iconbitmap('Logo.ico')

    frm = Frame(top)
    frm.pack(side=TOP,padx=20)

    reporte_label = Label(frm,text='Reporte')
    reporte_label.pack(side=TOP, pady=10)
    reporte_label.config(font=("Courier", 44))

    report = Text(frm,width=150,height=10, wrap=WORD,bd = 3)
    report.pack(side=TOP)

    guardar_btn = Button(top, text='Guardar', command=lambda: insertar_reportes_query(report.get('1.0','end-1c')))
    guardar_btn.pack(side=TOP,pady=20,padx=10)

def Open_Inventario():
    top = Toplevel()
    top.title('Inventario')
    top.geometry('650x500')
    top.resizable(False,False)
    top.iconbitmap('Logo.ico')

    frm = Frame(top)
    frm.pack(side=TOP,padx=20)

    #Label for inventory table
    paciente_label = Label(frm,text='Inventario')
    paciente_label.pack(side=TOP)
    paciente_label.config(font=("Courier", 44))

    #Table por inventory
    pac = ttk.Treeview(frm,columns=(1,2,),show='headings',height='4')
    pac.pack(side=TOP,fill=X)
    
    pac.column(1,width=80,minwidth=50)
    pac.column(2,width=80,minwidth=50)
    
    pac.heading(1,text='Articulo',anchor=W)
    pac.heading(2,text='Cantidad',anchor=W)

    def refresh_table():
        pac.delete(*pac.get_children())
        inventario = select_inventario_query()
        for row in inventario:
            pac.insert('', 'end', values=row)
    
    refresh_table()

    #Labels
    articulo_label = Label(top,text='Articulo')
    articulo_label.place(relx=0.3,rely=0.5,anchor=CENTER)
    cantidad_label = Label(top,text='Cantidad')
    cantidad_label.place(relx=0.3,rely=0.6,anchor=CENTER)


    #Entry for amount of increment or decrement
    mod_entry = Entry(top,width=5)
    mod_entry.place(relx=0.385,rely=0.6,anchor=CENTER)

    mi_articulo = StringVar()
    articulos = ttk.Combobox(top, width=27, textvariable = mi_articulo)
    articulos['values'] = ('Tape Bandas','Desinfectantes','Facepapers','Biofreeze')
    articulos.place(relx=0.5,rely=0.5,anchor=CENTER)
    articulos.current()

    add_button = Button(top, text='Añadir', command=lambda: [modify_inventory_query(mi_articulo.get(), mod_entry.get(),'sumar'),refresh_table()])
    add_button.place(relx=0.7,rely=0.5,anchor=CENTER)
    restar_button = Button(top, text='Quitar', command=lambda: [modify_inventory_query(mi_articulo.get(), mod_entry.get(),'restar'),refresh_table()])
    restar_button.place(relx=0.7,rely=0.6,anchor=CENTER)

    


    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#MAIN

try:
    connection = psycopg2.connect(user = "postgres", password = "jahesgrande01", host = "localhost", port = "5432", database = "Clinica")

    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(),'\n')

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
  
    main_GUI_window()
    
except(Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    #closing database connection
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")