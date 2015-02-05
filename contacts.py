import os
from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['PAGE_SINGLE'] = 1
app.config['PAGE_DIRECTORY'] = 10
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

@app.route('/user/<int:userid>', methods=['GET'])
def user(userid):
    contact = Contact.query.get(userid)
    return render_template('user.html', entry=contact)

@app.route('/directory', methods=['GET'])
@app.route('/directory/<int:page>', methods=['GET'])
def directory(page=1):
    contact = Contact.query.with_entities(Contact.lname, Contact.fname, Contact.id).order_by(Contact.lname).paginate(page, app.config['PAGE_DIRECTORY'], True)
    return render_template('directory.html', entry=contact)

@app.route('/', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    contact = Contact.query.with_entities(Contact.lname, Contact.fname, Contact.phone, Contact.addr, Contact.email).order_by(Contact.lname).paginate(page, app.config['PAGE_SINGLE'], True)
    return render_template('index.html', entry=contact)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
