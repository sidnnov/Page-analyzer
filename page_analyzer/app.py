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
from validators import url
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests import ConnectionError, HTTPError
from page_analyzer.db import (
    get_urls_data,
    get_checks_data,
    get_urls_from_db,
    save_new_url_to_bd_urls,
    check_url_from_db,
    save_to_db_url_checks,
)
import requests
import os


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
LENGTH = 255


def normalize_url(url: str) -> str:
    url_parse = urlparse(url)
    correct_url = url_parse._replace(
        path="", params="", query="", fragment="").geturl()
    return correct_url


def get_content(data: str) -> tuple:
    content = BeautifulSoup(data, "lxml")
    h1 = content.find("h1")
    title = content.find("title")
    meta_data = content.find("meta", attrs={"name": "description"})
    h1 = h1.text if h1 else ""
    title = title.text if title else ""
    description = meta_data.get("content") if meta_data else ""
    return h1, title, description


def check_error(url_with_form: str) -> list:
    if not url(url_with_form):
        flash("Некорректный URL", "danger")
        if not url_with_form:
            flash("URL обязателен", "danger")
    if len(url_with_form) > LENGTH:
        flash(f"URL превышает {LENGTH} символов", "danger")
    return get_flashed_messages(with_categories=True)


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
    url_with_form = request.form["url"].lower()
    error = check_error(url_with_form)
    if error:
        return render_template(
            "/index.html",
            url=url_with_form,
            messages=error), 422
    correct_url = normalize_url(url_with_form)
    data = save_new_url_to_bd_urls(correct_url)
    if data["recorded"] == "error":
        return render_template('errors/500.html'), 500
    if data["recorded"]:
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("get_url", id=data["id"]))
    flash("Страница уже существует", "info")
    return redirect(url_for("get_url", id=data["id"]))


@app.route("/urls", methods=["GET"])
def get_urls():
    data = get_urls_from_db()
    if not data:
        # flash('Ой, что-то отвалилось :(', "danger")
        # messages = get_flashed_messages(with_categories=True)
        # return render_template(
        #     'index.html',
        #     messages=messages), 500
        return render_template('errors/500.html'), 500
    return render_template("urls.html", data=data)


@app.route("/urls/<id>", methods=["GET"])
def get_url(id):
    urls_data = get_urls_data(id)
    if not urls_data:
        return render_template('errors/404.html'), 404
    checks_data = get_checks_data(id)
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
    data = check_url_from_db(id)
    try:
        response = requests.get(data.name)
        response.raise_for_status()
    except (ConnectionError, HTTPError):
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for('get_url', id=id))
    status_code = response.status_code
    h1, title, description = get_content(response.text)
    save_to_db_url_checks(id, status_code, h1, title, description)
    flash("Страница успешно проверена", "success")
    return redirect(url_for("get_url", id=id))
