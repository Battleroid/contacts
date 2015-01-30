from contacts import db

def main():
    setup_db()

def setup_db():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    main()