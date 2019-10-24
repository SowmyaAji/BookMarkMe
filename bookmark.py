from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect

from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)

bookmarks = []


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return self.firstname + " " + self.lastname

    def initials(self):
        return "[{}{}]".format(self.firstname[0], self.lastname[0])


def store_bookmark(url):
    bookmarks.append(dict(url=url,
                          user=User("Alice", "Wonderland"),
                          datetime=datetime.utcnow()))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Random stuff",
                           text="Waiting to make sense",
                           user=User("Alice", "Wonderland"))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        store_bookmark(url)
        app.logger.debug('your stored_url is: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def servererror(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
