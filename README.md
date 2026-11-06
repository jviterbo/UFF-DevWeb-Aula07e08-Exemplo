# Lista de Recados — Running Example da Aula 07 (Flask-SQLAlchemy)

Evolução da aplicação da Aula 06: a lista de recados, que antes ficava em memória, agora é **persistida em um banco SQLite** com **Flask-SQLAlchemy** (ORM). Reiniciar o servidor não apaga mais os dados.

## O que mudou em relação à Aula 06

| Aula 06 | Aula 07 |
|---|---|
| Lista Python em memória | Tabelas `recado` e `categoria` no SQLite |
| `/recado?id=2` (query string) | `/recado/2` (rota dinâmica `<int:id>`) |
| `/remove?id=1` via GET | `/deletar/<id>` e `/concluir/<id>` via **POST** + CSRF |
| Sem edição | `/editar/<id>` com formulário pré-preenchido (`obj=`) |
| Sem categorias | Relacionamento 1:N `Categoria` → `Recado` |
| Sem feedback | Mensagens `flash()` com Alerts do Bootstrap |

## Executar

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                     # http://127.0.0.1:5000
```

O banco é criado em `instance/recados.db` na primeira execução, com 3 categorias e 3 recados de exemplo. Para recomeçar do zero, apague `instance/recados.db`.

## Estrutura

```
app.py          rotas (CRUD), configuração e carga inicial
models.py       db, Categoria e Recado
forms.py        RecadoForm (Flask-WTF)
templates/      base, index, recado, form (criar/editar), categorias, 404
```

## Rotas

| Rota | Método | Operação |
|---|---|---|
| `/` | GET | Read — todos os recados |
| `/pendentes` | GET | Read — `filter_by(concluido=False)` |
| `/busca?q=` | GET | Read — `filter(... .contains(q))` |
| `/categorias` | GET | Read — categorias e contagem de recados |
| `/recado/<id>` | GET | Read — detalhes (`get_or_404`) |
| `/novo` | GET, POST | Create |
| `/editar/<id>` | GET, POST | Update |
| `/concluir/<id>` | POST | Update (marca como concluído) |
| `/deletar/<id>` | POST | Delete |

## Onde cada conceito da aula aparece

| Conceito | Arquivo |
|---|---|
| `db.Model`, colunas, `nullable`, `unique`, `default` | `models.py` |
| `ForeignKey` e `relationship(back_populates=...)` | `models.py` |
| Consulta reutilizável (`pendentes()`) | `models.py` |
| `SQLALCHEMY_DATABASE_URI`, `db.init_app`, `db.create_all()` | `app.py` |
| `Model.query` (`all`, `filter_by`, `filter`, `order_by`, `count`) | `app.py` |
| `db.session.add / delete / commit` | `app.py` |
| `db.get_or_404` e `errorhandler(404)` | `app.py` |
| `SelectField` com opções vindas do banco | `forms.py`, `app.py` |
| `flash()` + `get_flashed_messages(with_categories=true)` | `app.py`, `base.html` |
| `CSRFProtect` e `csrf_token()` em formulários simples | `app.py`, `index.html` |

## Roteiro de exploração

1. Cadastre um recado em branco (erros de validação) e depois um válido (alerta verde).
2. Edite, conclua e remova recados; use a busca e `/pendentes`.
3. Pare e reinicie o servidor: os dados continuam lá.
4. Abra `instance/recados.db` (DB Browser for SQLite ou `sqlite3`) e confira tabelas e linhas.
5. Experimente no `flask shell`:
   ```python
   >>> from models import *
   >>> Recado.query.all()
   >>> r = db.session.get(Recado, 1); r.categoria.nome
   >>> Categoria.query.first().recados
   ```
   (execute `flask --app app shell`)

## Problemas comuns

- **`no such table`**: as tabelas não existem; apague `instance/recados.db` e rode de novo.
- **Mudei o model e nada mudou**: `create_all()` não altera tabelas existentes; apague o `.db` (ou use Flask-Migrate).
- **Erro 400 em POST**: falta o token CSRF no formulário.
- **405 ao abrir `/deletar/1` no navegador**: correto — a rota só aceita POST.
- **IntegrityError ao remover uma categoria com recados**: há recados que dependem dela.

## Exercícios

1. Adicionar o campo `prioridade` ao `Recado` (e recriar o banco).
2. Criar a rota `/concluidos` com `filter_by`.
3. Ordenar a listagem do mais novo para o mais antigo (`criado_em`).
4. Criar o cadastro de categorias tratando `IntegrityError` (com `rollback()`).
5. Mostrar na navbar o número de recados pendentes.

## Versões

Python 3.10+, Flask ≥ 3.0, Flask-WTF ≥ 1.2, Flask-SQLAlchemy ≥ 3.1, Bootstrap 5.3 (CDN).
