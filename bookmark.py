from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import BookmarkForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'T\x87AD\xf1%\xf1\xe8\xe8\x85\xb6de\xca\xce'

bookmarks = []


class User:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return self.firstname + " " + self.lastname

    def initials(self):
        return "[{}{}]".format(self.firstname[0], self.lastname[0])


def store_bookmark(url, description):
    bookmarks.append(dict(url=url,
                          description=description,
                          user=User("Alice", "Wonderland"),
                          date=datetime.utcnow()))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Random stuff",
                           text="Waiting to make sense",
                           user=User("Alice", "Wonderland"), new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash("You have successfully bookmarked {} {}".format(url, description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def servererror(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
