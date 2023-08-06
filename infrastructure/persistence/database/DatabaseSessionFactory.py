import configparser
import os
from sqlalchemy import create_engine , select,text
from sqlalchemy.orm import sessionmaker, clear_mappers
from infrastructure.persistence.orm.models  import metadata

config = configparser.ConfigParser()
config.read('config.ini')

current_env = os.environ.get('current_env') or config.get('environment', 'current')

class DatabaseSessionFactory:
    def create_session(self):
        print(current_env)
        if current_env == 'production':
            return create_prod_session()
        elif current_env == 'development':
            return create_dev_session()

def create_prod_session():
    engine=create_engine(config.get(current_env, 'sqlite'),echo=True,connect_args={'check_same_thread': False})
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(text('pragma foreign_keys=on'))
    yield sessionmaker(bind=engine)()


def create_dev_session():
    engine=create_engine(config.get(current_env, 'sqlite'),echo=True,connect_args={'check_same_thread': False})
    metadata.create_all(engine)
    with engine.connect() as conn:
        result = conn.execute(text('pragma foreign_keys=on'))
    return sessionmaker(bind=engine)()