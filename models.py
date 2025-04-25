from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Boolean, DateTime, Float, Date, Function

# importamos session e sessionmaker

from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

from datetime import date

from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///APIbiblioteca')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Ordem_de_servicos(Base):
    __tablename__ = 'ordem_de_servicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    veiculo_associados = Column(Integer, ForeignKey('veiculo_associados.id'))
    data_de_abertura = Column(Date, nullable=True)
    descricao_do_servicos = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    valor_estimado = Column(Float, nullable=False)

    def __repr__(self):
        return '<Livro {},{},{},{},{}>'.format(self.id, self.veiculo_associados, self.data_de_abertura, self.descricao_do_servicos, self.status, self.valor_estimado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def get_servicos(self):
        dados_servicos = {
            'id': self.id,
            'veiculo_associados': self.veiculo_associados,
            'data_de_abertura': self.data_de_abertura,
            'descricaco_do_servicos': self.descricao_do_servicos,
            'status': self.status,
            'valor_estimado': self.valor_estimado,
        }
        return dados_servicos

class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    CPF = Column(String(11), nullable=False, unique=True)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return '<usuario {},{},{},{}>' .format(self.id, self.nome, self.CPF, self.telefone, self.endereco)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete_usuario(self):
        db_session.delete(self)
        db_session.commit()

    def get_usuario(self):
        dados_usuarios = {
            'id': self.id,
            'nome': self.nome,
            'CPF': self.CPF,
            'endereco': self.endereco,
        }
        return dados_usuarios

class Emprestimos(Base):
    __tablename__ = 'emprestimos'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    marca = Column(Date, nullable=False)
    modelo = Column(Date, nullable=False)
    placa = Column(Integer, index=True, nullable=False)
    ano_de_fabricacao = Column(Date, nullable=True)


    def __repr__(self):
        return '<emprestimo {},{},{},{},{}'. format(self.id, self.marca, self.modelo, self.placa, self.ano_de_fabricacao)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete_emprestimo(self):
        db_session.delete(self)
        db_session.commit()

    def get_emprestimo(self):
        dados_emprestimos = {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'placa': self.placa,
            'ano_de_fabricacao': self.ano_de_fabricacao,
        }
        return dados_emprestimos


def init_db():
    Base.metadata.create_all(engine)
if __name__ == '__main__':
    init_db()

