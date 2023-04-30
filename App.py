from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = '18.232.133.235'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'sistemas20.'
app.config['MYSQL_DB'] = 'Progrades'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data=cur.fetchall()
    return render_template('index.html', usuarios = data)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST': #Define método de envío
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        nickname = request.form['nickname']
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO usuarios (nombre, apellido,correo,contrasenia,nickname,COMUNIDAD_Nombre) VALUES (%s, %s, %s, %s, %s, %s)', 
        (nombre, apellido,correo, contrasenia,nickname,'Universidad Peruana de Ciencias Aplicadas')) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        flash('Usuario agregado correctamente')
        return redirect(url_for('Index')) #Redirecciona a pagina Index

@app.route('/edit/<id>')
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-user.html', user = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_user(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        nickname = request.form['nickname']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios
        SET nombre = %s,
            apellido = %s,
            correo = %s,
            contrasenia = %s,
            nickname = %s
        WHERE id = %s
        """, (nombre,apellido,correo,contrasenia,nickname,id))
        mysql.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM usuarios WHERE id = {id}')
    mysql.connection.commit()
    flash('Usuario eliminado exitosamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)