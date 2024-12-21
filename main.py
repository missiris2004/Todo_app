from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///utiles.db'
db = SQLAlchemy(app)

# Modelo de la base de datos
class UtilEscolar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    estado = db.Column(db.String(20))  # "Por comprar" o "Comprado"

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    utiles = UtilEscolar.query.all()
    return render_template('index.html', utiles=utiles)

@app.route('/agregar', methods=['POST'])
def agregar_util():
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad', type=int)
    if nombre and cantidad:
        nuevo_util = UtilEscolar(nombre=nombre, cantidad=cantidad, estado="Por comprar")
        db.session.add(nuevo_util)
        db.session.commit()
    return redirect(url_for('inicio'))

@app.route('/cambiar_estado/<int:id>', methods=['POST'])
def cambiar_estado(id):
    util = UtilEscolar.query.get(id)
    if util:
        util.estado = "Comprado" if util.estado == "Por comprar" else "Por comprar"
        db.session.commit()
    return redirect(url_for('inicio'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    util = UtilEscolar.query.get(id)
    if util:
        db.session.delete(util)
        db.session.commit()
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
