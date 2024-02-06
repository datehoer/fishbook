from flask import Flask
from helper import check_isbn, get_search_result_zlibrary

app = Flask(__name__)
app.config.from_object('config')
search_return_data = {
    "data": [],
    "success": "ok",
    "msg": "",
    "page": 1,
    "has_next": False,
}


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
    data = get_search_result_zlibrary(url, app.config['PROXIES'])
    if len(data) == 0:
        not_found_data = search_return_data.copy()
        not_found_data['success'] = "no"
        not_found_data['message'] = "no data"
        not_found_data['page'] = page
        return not_found_data, 404
    ok_return_data = search_return_data.copy()
    ok_return_data['data'] = data
    ok_return_data['page'] = page
    ok_return_data['message'] = "success"
    return ok_return_data, 200


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])