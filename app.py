from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')  # This is the default route
def index():
    return '<a href="/posts">POSTS</a>'


@app.route('/redirect')
def redirect2():
    return redirect(url_for('response'))


@app.route('/response')
def response():
    return render_template(template_name_or_list='response.html')


@ app.route('/posts')
@ app.route('/posts/<int:id>')
def posts(id):
    titulo = request.args.get('titulo')

    data = dict(
        path=request.path,
        referrer=request.referrer,
        method=request.method,
        content_type=request.content_type,
        titulo=titulo,
        id=id if id else 0
    )
    return data


if __name__ == '__main__':
    app.run(debug=True)
