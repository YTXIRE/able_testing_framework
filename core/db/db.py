from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ARRAY, BIGINT, BigInteger, Binary, BLOB, Boolean, CHAR, CLOB, Date, \
    DateTime, DECIMAL, Enum, Float, Integer, Interval, JSON, LargeBinary, NCHAR, Numeric, NVARCHAR, PickleType, REAL, \
    SmallInteger, String, Text, Time, TIMESTAMP, TypeDecorator, Unicode, UnicodeText, VARBINARY, VARCHAR

from core.helpers import get_settings

BASE = declarative_base()


class DB:
    def _connection(self, environment):
        data = get_settings(environment)
        engine = None

        if data['DB']['DB_TYPE'].lower() == 'postgresql':
            engine = create_engine(f"postgresql://{data['DB']['USER']}:{data['DB']['PASSWORD']}@"
                                   f"{data['DB']['HOST']}:{data['DB']['PORT']}/{data['DB']['DB_NAME']}")
        elif data['DB']['DB_TYPE'].lower() == 'mysql':
            engine = create_engine(f"mysql://{data['DB']['USER']}:{data['DB']['PASSWORD']}@{data['DB']['HOST']}/"
                                   f"{data['DB']['DB_NAME']}")
        elif data['DB']['DB_TYPE'].lower() == 'oracle':
            engine = create_engine(f"oracle://{data['DB']['USER']}:{data['DB']['PASSWORD']}@{data['DB']['HOST']}:"
                                   f"{data['DB']['PORT']}/{data['DB']['DB_NAME']}")
        elif data['DB']['DB_TYPE'].lower() == 'mssql':
            engine = create_engine(f"mssql+pyodbc://{data['DB']['USER']}:{data['DB']['PASSWORD']}@"
                                   f"{data['DB']['DB_NAME']}")
        elif data['DB']['DB_TYPE'].lower() == 'sqlite':
            engine = create_engine(f"sqlite:///{data['DB']['PATH']}")

        return engine

    def _create_session(self, environment):
        connection = self._connection(environment=environment)
        Session = sessionmaker(connection)
        BASE.metadata.create_all(connection)
        return Session()

    def get(self, table_name: any, environment: str, limit: int = 0, offset: int = 0):
        session = self._create_session(environment=environment)
        if limit and not offset:
            return session.query(table_name).limit(limit)
        elif limit and offset:
            return session.query(table_name).limit(limit).offset(offset)
        return session.query(table_name)

    def create(self, query_object: any, environment: str):
        session = self._create_session(environment=environment)
        try:
            session.add(query_object)
            session.commit()
            return {'id': query_object.id}
        except BaseException as e:
            print(e.args)
            session.rollback()
            return False

    def create_all(self, query_object: any, environment: str):
        session = self._create_session(environment=environment)
        try:
            session.add_all(query_object)
            session.commit()
            ids = []
            for item in query_object:
                ids.append(item.id)
            return {'ids': ids}
        except BaseException as e:
            print(e.args)
            session.rollback()
            return False

    def update(self, table_name: any, environment: str, condition: dict, update_value: dict):
        session = self._create_session(environment=environment)
        try:
            session.query(table_name).filter_by(**condition).update(update_value)
            session.commit()
            return 'Successful updated'
        except BaseException as e:
            print(e.args)
            session.rollback()
            return False

    def delete(self, table_name: any, environment: str, condition: dict):
        session = self._create_session(environment=environment)
        try:
            session.query(table_name).filter_by(**condition).delete()
            session.commit()
            return 'Successful deleted'
        except BaseException as e:
            print(e.args)
            session.rollback()
            return False

    def execute(self, environment: str, query: str):
        """
            execute("SELECT * FROM user WHERE id=5")
            :param query: str
            :param environment: str
            :return:
        """
        session = self._create_session(environment=environment)
        try:
            result = session.execute(query)
            session.commit()
            items = []
            for row in result:
                items.append(row)
            return items
        except BaseException as e:
            print(e.args)
            session.rollback()
            return False

    def get_by(self, table_name: any, environment: str, condition: dict, limit: int = 0, offset: int = 0):
        session = self._create_session(environment=environment)
        try:
            if limit and not offset:
                result = session.query(table_name).filter_by(**condition).limit(limit).all()
            elif limit and offset:
                result = session.query(table_name).filter_by(**condition).limit(limit).offset(offset).all()
            else:
                result = session.query(table_name).filter_by(**condition).all()
            items = []
            for row in result:
                tmp = {}
                for _row in vars(row):
                    if _row not in ['_sa_instance_state']:
                        tmp[_row] = row.__dict__[_row]
                items.append(tmp)
            return items
        except BaseException as e:
            print(e.args)
            return False


class DBHelper:
    def column(self, column, *args, **kwargs):
        """
        :param column:
            array, biging, giginteger, binary,
            blob, bool, char, clob, date,
            datetime, decimal, emum, float,
            int, interval, json, largebinary,
            nchar, numeric, nvarchar, pickletype,
            real, smallint, str, text, time,
            timestamp, typedecoder, unicode,
            unicodetext, varbinary, varchar
        :return: поле типа SQL
        """
        column_type = {
            'array': ARRAY,
            'biging': BIGINT,
            'giginteger': BigInteger,
            'binary': Binary,
            'blob': BLOB,
            'bool': Boolean,
            'char': CHAR,
            'clob': CLOB,
            'date': Date,
            'datetime': DateTime,
            'decimal': DECIMAL,
            'emum': Enum,
            'float': Float,
            'int': Integer,
            'interval': Interval,
            'json': JSON,
            'largebinary': LargeBinary,
            'nchar': NCHAR,
            'numeric': Numeric,
            'nvarchar': NVARCHAR,
            'pickletype': PickleType,
            'real': REAL,
            'smallint': SmallInteger,
            'str': String,
            'text': Text,
            'time': Time,
            'timestamp': TIMESTAMP,
            'typedecoder': TypeDecorator,
            'unicode': Unicode,
            'unicodetext': UnicodeText,
            'varbinary': VARBINARY,
            'varchar': VARCHAR,
        }.get(column, 'varchar')

        return Column(column_type, *args, **kwargs)
