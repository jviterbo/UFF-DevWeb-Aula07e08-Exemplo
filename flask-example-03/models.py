from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False, unique=True)

    # lado "um" do relacionamento um-para-muitos: uma categoria tem vários recados
    recados = db.relationship("Recado", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Recado(db.Model):
    __tablename__ = "recado"

    id = db.Column(db.Integer, primary_key=True)             # chave primária (autoincremento)
    texto = db.Column(db.String(80), nullable=False)
    descr = db.Column(db.String(280), nullable=False)
    concluido = db.Column(db.Boolean, nullable=False, default=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # chave estrangeira + lado "muitos" do relacionamento
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)
    categoria = db.relationship("Categoria", back_populates="recados")

    @classmethod
    def pendentes(cls):
        """Consulta reutilizável: recados ainda não concluídos."""
        return cls.query.filter_by(concluido=False).order_by(cls.id).all()

    def __repr__(self):
        return f"<Recado {self.id}: {self.texto}>"
