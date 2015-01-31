import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee

app = Flask(__name__)
app.config['WHOOSHEE_DIR'] = 'whooshee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['PAGE_MAX'] = 1
app.config['SECRET_KEY'] = os.urandom(32)
db = SQLAlchemy(app)
whoosh = Whooshee(app)

@whoosh.register_model('fname', 'lname', 'email')
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, index=True)
    lname = db.Column(db.String, index=True)
    phone = db.Column(db.String)
    addr = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)

    def __repr__(self):
        return '<Contact %r %r %r>' % (self.fname, self.lname, self.email)

@app.errorhandler(404)
def nope(e):
    flash("Woops! What you're looking for doesn't exist!")
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    # if request.method == 'POST':
    #     query = request.form['search']
    #     result = Contact.query.whooshee_search(query).all()
    #     print query, 'result:', result
    contact = Contact.query.with_entities(Contact.lname, Contact.fname, Contact.phone, Contact.addr, Contact.email).paginate(page, app.config['PAGE_MAX'], True)
    return render_template('index.html', entry=contact)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
