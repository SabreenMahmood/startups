from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
# from flask_sqlalchemy import SQLAlchemy
from cs50 import SQL


app = Flask(__name__)
app.config['SECRET_KEY'] = '49f4586280d204f701c73172a197fdbe'
db = SQL("sqlite:///startups_iq.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.execute('SELECT username FROM user WHERE id = ?;', user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        # ensue email was submitted
        if not request.form.get("email"):
            return flash("must provide username")

        # ensue password was submitted
        elif not request.form.get("password"):
            return flash("must provide password")

        # query DB for username
        u = db.execute('SELECT * FROM user WHERE email = ?;', request.form.get("email"))

        # ensure email exists and password is correct
        if len(u) != 1 or not request.form.get("password"):
            return flash("invalid email or password")

        return redirect(url_for('add'))
    else:
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return "Hello, world"
#    return render_template('index.html')


# GET    Retrieve list of startups
@app.route("/add", methods=['GET'])
@login_required
def get_startups():
    s1 = db.execute('SELECT * FROM startup;')
    return jsonify(s1)


@app.route("/add", methods=['POST'])
@login_required
def add_startups():
    s2 = dict(request.json)
    db.execute('INSERT INTO startup ("name", "website", "desc", "logo_path", "cat_id") VALUES (?,?,?,?,?);',
               s2['name'], s2['website'], s2['desc'], s2['logo_path'],  s2['cat_id'])
    return "hello, Sabreen"


# GET    Retrieve one of startups
@app.route("/add/<int:startup_id>", methods=['GET'])
@login_required
def get_startup(startup_id):
    s3 = db.execute('SELECT * FROM startup WHERE id = ?;', startup_id)
    return jsonify(s3)


# GET    Retrieve list of startups belong to one category
@app.route("/add/<string:cat_name>", methods=['GET'])
@login_required
def get_startup_category(cat_name):
    s4 = db.execute('SELECT * FROM startup JOIN category ON startup.cat_id = category.id WHERE category.name = ?;'
                    , cat_name)
    return jsonify(s4)


# PUT    updating a startup
@app.route("/add/<int:startup_id>", methods=['PUT'])
@login_required
def update_startup(startup_id):
    # get the startup
    s5 = db.execute('SELECT * FROM startup  WHERE id = ?;', startup_id)

    # update the startup
    name = request.json.get('name', s5[0]['name'])
    website = request.json.get('website', s5[0]['website'])
    desc = request.json.get('desc', s5[0]['desc'])
    logo_path = request.json.get('logo_path', s5[0]['logo_path'])
    cat_id = request.json.get('cat_id', s5[0]['cat_id'])

    # insert the updating startup
    db.execute('UPDATE startup SET name = ?, website = ?, desc = ?, logo_path = ?, cat_id = ? WHERE id = ?',
               name, website, desc, logo_path, cat_id, startup_id)
    return "startup updating"


# DELETE     delete a startup
@app.route("/add/<int:startup_id>", methods=['DELETE'])
@login_required
def delete_startups(startup_id):
    db.execute('DELETE FROM startup WHERE id = ?', startup_id)
    return "the startup deleted"


if __name__ == '__main':
    app.run(debug=True)
