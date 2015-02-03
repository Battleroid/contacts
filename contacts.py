import os
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['PAGE_MAX'] = 1
app.config['SECRET_KEY'] = os.urandom(32)
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    phone = db.Column(db.String)
    addr = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return '<Contact %r %r %r>' % (self.fname, self.lname, self.email)

@app.errorhandler(404)
def nope(e):
    flash("Woops! What you're looking for doesn't exist!")
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    contact = Contact.query.with_entities(Contact.lname, Contact.fname, Contact.phone, Contact.addr, Contact.email).paginate(page, app.config['PAGE_MAX'], True)
    return render_template('index.html', entry=contact)

if __name__ == '__main__':
    app.run()
