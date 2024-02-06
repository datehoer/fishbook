from flask import Flask, make_response
from helper import check_isbn, get_search_result

app = Flask(__name__)
app.config.from_object('config')


@app.route("/hello")
def hello():
    # status code 200, 404, 301
    # status code is a mark, don't need to care?
    headers = {
        "content-type": "text/html"
    }
    response = make_response("<html><body><p>Hello, World!</p></body></html>", 200)
    response.headers = headers
    return response


@app.route("/book/search/<q>/<page>")
def search(q, page):
    """
    :param q: 搜索关键词 ISBN
    :param page: 搜索页码
    :return:
    """
    isbn_or_key = check_isbn(q)
    if isbn_or_key == "isbn":
        url = "https://1lib.sk/s/{}".format(q)
    else:
        url = "https://1lib.sk/s/{}".format(q)
    data = get_search_result(url, app.config['PROXIES'])
    if len(data) == 0:
        return {
            "data": [],
            "success": "no",
            "msg": "no data",
            "page": page,
            "has_next": False,
        }, 404
    return_data = {
        "data": data,
        "success": "ok",
        "msg": "success",
        "page": page,
        "has_next": False,
    }
    return return_data, 200


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])