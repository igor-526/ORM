import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Stock, Sale, Book
import json


def loaddata(session):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def get_id(session, q):

    try:
        int(q)
        print(f'Выбран издатель: {session.query(Publisher.name).filter(Publisher.id == q).first()[0]}')
        return q
    except:
        return session.query(Publisher.id).filter(Publisher.name.like(q)).first()[0]


def searchsales(session, q):
    id = get_id(session, q)
    for sale in (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Sale.stock)
           .join(Stock.shop).join(Stock.book).filter(Book.id_publisher == id).all()):
        print(f'Название книги: {sale[0]}\n'
              f'Магазин: {sale[1]}\n'
              f'Цена: {sale[2]}$\n'
              f'Дата: {sale[3].strftime("%d-%m-%Y")}\n')


def main():
    DSM = f'postgresql://{config.user}:{config.password}@{config.host}:5432/{config.database}'
    engine = sqlalchemy.create_engine(DSM)
    Session = sessionmaker(bind=engine)
    session = Session()
    if config.resetdb == 1:
        create_tables(engine)
    if config.loaddata == 1:
        loaddata(session)
    searchsales(session, input("Введите имя или id издателя: "))
    session.close()


if __name__ == "__main__":
    main()
