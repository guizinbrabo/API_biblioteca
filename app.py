from flask import Flask, jsonify, redirect, request
from flask_pydantic_spec import FlaskPydanticSpec
from datetime import date
from dateutil.relativedelta import relativedelta
from models import db_session, Usuarios
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, desc
app = Flask(__name__)
spec = FlaskPydanticSpec('Flask',
                         title='Flask API',
                         version='1.0.0')

spec.register(app)
app.secret_key = 'key_secret'

@app.route('/')
def index():
    return redirect('/cadastrar_usuario')


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        endereco = request.form.get('endereco')

        cpf_ja_cadastrado = select(Usuarios)
        cpf_ja_cadastrado = db_session.execute(cpf_ja_cadastrado.filter_by(CPF=cpf)).first()
        if cpf_ja_cadastrado:
            return jsonify({"error": 'CPF ja cadastrado'})

        endereco_ja_cadastrado = select(Usuarios)
        endereco_ja_cadastrado = db_session.execute(endereco_ja_cadastrado.filter_by(endereco=endereco)).first()
        if endereco_ja_cadastrado:
            return jsonify({"error": 'endereco ja cadastrado'})
        if not nome:
            return jsonify({"error": 'campo nome vazio'}, 400)
        if not cpf:
            return jsonify({"error": 'campo cpf vazio'}, 400)
        if not endereco:
            return jsonify({"error": 'campo endereco vazio'}, 400)
        else:
            try:
                usuario_salvado = Usuarios(nome=nome,
                                           CPF=cpf,
                                           endereco=endereco)
                usuario_salvado.save()
                return jsonify({
                    'titulo': usuario_salvado.nome,
                    'autor': usuario_salvado.CPF,
                    'resumo': usuario_salvado.endereco})
            except IntegrityError as e:
                return jsonify({'error': str(e)})

@app.route('/consultar_usuarios')
def consultar_usuario():
    try:
        lista_servicos = select(Usuarios)
        lista_servicos = db_session.execute(lista_servicos).scalars()
        result = []
        for servicos in lista_servicos:
            result.append(servicos.get_usuario())
        db_session.close()

        return jsonify({'usuarios': result})


    except IntegrityError as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)