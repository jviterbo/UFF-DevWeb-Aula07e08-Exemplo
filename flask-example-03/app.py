from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect

from models import db, Recado, Categoria
from forms import RecadoForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-secreta-aula07"                # CSRF e flash()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recados.db"   # arquivo em instance/recados.db

CSRFProtect(app)   # exige o token CSRF em TODA requisição POST
db.init_app(app)


def opcoes_categorias():
    return [(c.id, c.nome) for c in Categoria.query.order_by(Categoria.nome).all()]


# ---------------------------------------------------------------- READ (listagens)
@app.route("/")
def index():
    recados = Recado.query.order_by(Recado.id).all()
    return render_template("index.html", recados=recados, titulo="Meus Recados")


@app.route("/pendentes")
def pendentes():
    recados = Recado.pendentes()
    return render_template("index.html", recados=recados, titulo="Recados Pendentes")


@app.route("/busca")
def busca():
    q = request.args.get("q", "")
    recados = Recado.query.filter(Recado.texto.contains(q)).order_by(Recado.id).all()
    return render_template("index.html", recados=recados, titulo=f"Busca por \"{q}\"")


@app.route("/categorias")
def categorias():
    todas = Categoria.query.order_by(Categoria.nome).all()
    return render_template("categorias.html", categorias=todas)


@app.route("/recado/<int:id>")
def detalhes(id):
    recado = db.get_or_404(Recado, id)
    return render_template("recado.html", recado=recado)


# ---------------------------------------------------------------- CREATE
@app.route("/novo", methods=["GET", "POST"])
def novo_recado():
    form = RecadoForm()
    form.categoria_id.choices = opcoes_categorias()
    if form.validate_on_submit():
        recado = Recado(
            texto=form.texto.data,
            descr=form.descr.data,
            categoria_id=form.categoria_id.data,
        )
        db.session.add(recado)
        db.session.commit()
        flash("Recado adicionado com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("form.html", form=form, titulo="Novo recado")


# ---------------------------------------------------------------- UPDATE
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_recado(id):
    recado = db.get_or_404(Recado, id)
    form = RecadoForm(obj=recado)          # no GET, preenche o formulário com os dados do banco
    form.categoria_id.choices = opcoes_categorias()
    if form.validate_on_submit():
        recado.texto = form.texto.data
        recado.descr = form.descr.data
        recado.categoria_id = form.categoria_id.data
        db.session.commit()                # entidade gerenciada: basta alterar e confirmar
        flash("Recado atualizado!", "info")
        return redirect(url_for("detalhes", id=recado.id))
    return render_template("form.html", form=form, titulo="Editar recado")


@app.route("/concluir/<int:id>", methods=["POST"])
def concluir_recado(id):
    recado = db.get_or_404(Recado, id)
    recado.concluido = True
    db.session.commit()
    flash(f"Recado \"{recado.texto}\" concluído!", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------- DELETE
@app.route("/deletar/<int:id>", methods=["POST"])
def deletar_recado(id):
    recado = db.get_or_404(Recado, id)
    db.session.delete(recado)
    db.session.commit()
    flash("Recado removido.", "warning")
    return redirect(url_for("index"))


@app.errorhandler(404)
def nao_encontrado(erro):
    return render_template("404.html"), 404


# ---------------------------------------------------------------- criação e carga inicial
def popula_banco():
    if Categoria.query.count() == 0:
        estudo = Categoria(nome="Estudo")
        trabalho = Categoria(nome="Trabalho")
        pessoal = Categoria(nome="Pessoal")
        db.session.add_all([estudo, trabalho, pessoal])
        db.session.add_all([
            Recado(texto="Revisar o Capítulo 3 de Flask",
                   descr="Reler o Capítulo 3 do livro e fazer os exercícios.",
                   concluido=True, categoria=estudo),
            Recado(texto="Estudar slides da Aula 6",
                   descr="Rodar os exemplos de Jinja2 e Flask-WTF.", categoria=estudo),
            Recado(texto="Entregar o Projeto Integrador",
                   descr="Subir o código do grupo e apresentar na Aula 8.", categoria=trabalho),
        ])
        db.session.commit()


with app.app_context():
    db.create_all()      # cria as tabelas que ainda não existem
    popula_banco()


if __name__ == "__main__":
    app.run(debug=True)
