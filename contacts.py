from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['PAGE_MAX'] = 1
app.config['WHOOSH_BASE'] = 'whoosh.base'

class Contact(db.Model):
    __tablename__ = 'contacts'
    __searchable__ = ['fname', 'lname', 'email']

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    phone = db.Column(db.String)
    addr = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return '<Contact %r %r %r>' % (self.fname, self.lname, self.email)

@app.route('/', methods=['GET', 'POST'])
@app.route('/page', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    # if request.method == 'POST':
    #     query = request.form['search']
    #     result = Contact.query.whoosh_search(query, limit=1).all()
    #     print result
    contact = Contact.query.with_entities(Contact.lname, Contact.fname, Contact.phone, Contact.addr, Contact.email).paginate(page, app.config['PAGE_MAX'], False)
    return render_template('index.html', entry=contact)

if __name__ == '__main__':
    app.run(debug=True)
