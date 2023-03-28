from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect,
)
from dotenv import load_dotenv
from page_analyzer import db
from page_analyzer.utils import (
    check_error,
    get_content,
    get_data_from_url,
    normalize_url,
)
import os


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/urls", methods=["POST"])
def add_url():
    conn = db.create_connection()
    url_with_form = request.form["url"].lower()
    error = check_error(url_with_form)

    if error:
        return render_template(
            "/index.html",
            url=url_with_form,
            messages=error), 422

    correct_url = normalize_url(url_with_form)
    id = db.get_id_if_exist(correct_url, conn)

    if id:
        flash("Страница уже существует", "info")
        return redirect(url_for("get_url", id=id))

    data = db.save_url_to_urls(correct_url)

    if data is None:
        return render_template('errors/500.html'), 500

    flash("Страница успешно добавлена", "success")
    return redirect(url_for("get_url", id=data.id))


@app.route("/urls", methods=["GET"])
def get_urls():
    conn = db.create_connection()
    data = db.get_urls(conn)
    if data == 'error':
        return render_template('errors/500.html'), 500

    return render_template("urls.html", data=data)


@app.route("/urls/<id>", methods=["GET"])
def get_url(id):
    conn = db.create_connection()
    urls_data = db.get_urls_data(id, conn)

    if not urls_data:
        return render_template('errors/404.html'), 404

    checks_data = db.get_checks_data(id, conn)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "url.html",
        urls_id=urls_data.id,
        name=urls_data.name,
        urls_date=urls_data.created_at,
        checks_data=checks_data,
        messages=messages,
    )


@app.route("/urls/<id>/checks", methods=["POST", "GET"])
def check_url(id):
    conn = db.create_connection()
    url = db.get_url(id, conn)
    data = get_data_from_url(url)

    if data is None:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for('get_url', id=id))

    status_code, data_html = data
    h1, title, description = get_content(data_html)
    db.save_to_url_checks(id, status_code, h1, title, description)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("get_url", id=id))
