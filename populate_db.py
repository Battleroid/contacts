from faker import Faker
from contacts import Contact, db

fake = Faker()

def populate(total=10):
    for person in range(total):
        db.session.add(Contact(fname=fake.first_name(), lname=fake.last_name(), addr=fake.street_address(), email=fake.email(), phone=fake.phone_number()))
    db.session.commit()

if __name__ == '__main__':
    populate()
