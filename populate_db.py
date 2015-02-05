from faker import Faker
import sys
from contacts import Contact, db

fake = Faker()

def populate(total=10):
    for person in range(total):
        db.session.add(Contact(fname=fake.first_name(), lname=fake.last_name(), addr=fake.street_address(), email=fake.email(), phone=fake.phone_number()))
    db.session.commit()

if __name__ == '__main__':
    if sys.argv[1]:
        try:
            populate(int(sys.argv[1]))
        except Exception:
            print sys.argv[1], 'is not an integer'
    else:
        populate()
