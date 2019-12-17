import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athlete(Base):
	
	__tablename__ = 'athelete'
	id = sa.Column(sa.Integer, primary_key=True)
	age = sa.Column(sa.Integer)
	birthdate = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	weight = sa.Column(sa.Integer)
	name = sa.Column(sa.Text)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)

class User(Base):

    __tablename__ = 'user'
    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    """
    Устанавливает соединение к базе данных, 
    создает таблицы, если их еще нет и возвращает объект сессии 
    """

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():

    print("Привет! Я помогу тебе найти двух атлетов:\nближайшего по дате рождения и ближайшего по росту к введеному пользователю.")
    user_id = input("Для начала поиска введите идентификатор пользователя: ")

    return int(user_id)

def converting(birthdate_str):
	
	a = birthdate_str.split("-")
	b = map(int, a)
	date = datetime.date(*b)
	return date

def date_search_athlete(user, session):

	all_athlete_list=session.query(Athlete).all()
	slovar = {}
	for athlete in all_athlete_list:
		b = converting(athlete.birthdate)
		slovar[athlete.id] = b
	user_b = converting(user.birthdate)
	
	athlete_id = None
	athlete_b = None
	delta_min = None
	for i, b in slovar.items():
		delta = abs(user_b - b)
		if not delta_min or delta < delta_min:
			delta_min = delta
			athlete_id = i
			athlete_b = b
	return athlete_id, athlete_b

def height_search_athlete(user, session):
	
	all_athlete_list=session.query(Athlete).filter(Athlete.height != None).all()
	slovar_2 = {athlete.id: athlete.height for athlete in all_athlete_list}

	athlete_id = None
	athlete_height = None
	delta_min = None

	for i, h in slovar_2.items():
		delta = abs(user.height - h)
		if not delta_min or delta < delta_min:
			delta_min = delta
			athlete_id = i
			athlete_height = h
	return athlete_id, athlete_height

def main():
	session = connect_db()
	user_id = request_data()
	user = session.query(User).filter(User.id == user_id).first()
	if not user:
		print("Такого пользователя нет. Попробуйте снова.")
	else:
		a_b, b = date_search_athlete(user,session)
		a_h, h = height_search_athlete(user, session)

		print("Данные пользователя:\n<><><><><><><><><><><><><>\nДата рождения: {}\nРост: {}\n<><><><><><><><><><><><><>".format(user.birthdate,user.height))
		print("Ближайший атлет по дате рождения: {}, он родился: {}".format(a_b,b))
		print("Ближайший атлет по росту: {}, его рост: {}".format(a_h,h))

if __name__ == "__main__":
    main()