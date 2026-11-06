from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class RecadoForm(FlaskForm):
    texto = StringField("Recado", validators=[DataRequired(), Length(max=80)])
    descr = StringField("Descrição", validators=[DataRequired(), Length(max=280)])
    # o nome do campo é igual ao do atributo do model: assim RecadoForm(obj=recado) já preenche tudo
    categoria_id = SelectField("Categoria", coerce=int)
    enviar = SubmitField("Salvar")
