from os import getenv

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ARRAY, BIGINT, BigInteger, BINARY, BLOB, Boolean, CHAR, CLOB, Date, \
    DateTime, DECIMAL, Enum, Float, Integer, Interval, JSON, LargeBinary, NCHAR, Numeric, NVARCHAR, PickleType, REAL, \
    SmallInteger, String, Text, Time, TIMESTAMP, TypeDecorator, Unicode, UnicodeText, VARBINARY, VARCHAR
from sqlalchemy.dialects.oracle import RAW, VARCHAR2
from sqlalchemy import inspect
from urllib.parse import quote_plus as urlquote

BASE = declarative_base()


class DB:
    def __init__(self, session=None):
        self.session = session
        self.connection = None

    def _connection(self, *, environment: dict, name: str) -> create_engine:
        environment[name]['USER'] = getenv(f"DB_USER_{name.upper()}")
        environment[name]['PASSWORD'] = getenv(f"DB_PASSWORD_{name.upper()}")
        db_name = environment[name]['DB_TYPE'].lower()
        match db_name:
            case 'postgresql':
                return create_engine(
                    f"postgresql://{environment[name]['USER']}:{urlquote(environment[name]['PASSWORD'])}@"
                    f"{environment[name]['HOST']}:{environment[name]['PORT']}/{environment[name]['DB_NAME']}"
                )
            case 'mysql':
                return create_engine(
                    f"mysql://{environment[name]['USER']}:{urlquote(environment[name]['PASSWORD'])}@{environment[name]['HOST']}/"
                    f"{environment[name]['DB_NAME']}"
                )
            case 'oracle':
                return create_engine(
                    f"oracle://{environment[name]['USER']}:{urlquote(environment[name]['PASSWORD'])}@{environment[name]['HOST']}:"
                    f"{environment[name]['PORT']}/?service_name={environment[name]['DB_NAME']}&mode=2"
                )
            case 'mssql':
                return create_engine(
                    f"mssql+pyodbc://{environment[name]['USER']}:{urlquote(environment[name]['PASSWORD'])}@"
                    f"{environment[name]['DB_NAME']}"
                )
            case 'sqlite':
                return create_engine(f"sqlite:///{environment[name]['PATH']}")

    def create_session(self, environment: dict, name: str) -> any:
        self.connection = self._connection(environment=environment, name=name)
        Session = sessionmaker(self.connection)
        if environment[name]['DB_TYPE'].lower() != 'postgresql':
            BASE.metadata.create_all(self.connection)
        return Session()

    def get(self, table_name: any, limit: int = 0, offset: int = 0) -> list | bool:
        try:
            if limit and not offset:
                result = self.session.query(table_name).limit(limit).all()
            elif limit and offset:
                result = self.session.query(table_name).limit(limit).offset(offset).all()
            else:
                result = self.session.query(table_name).all()
            items = []
            for row in result:
                tmp = {}
                for _row in vars(row):
                    if _row not in ['_sa_instance_state']:
                        tmp[_row] = row.__dict__[_row]
                items.append(tmp)
            return items
        except Exception as e:
            print('Error for get method in DB:', e.args)
            return False

    def create(self, query_object: any) -> dict | bool:
        try:
            self.session.add(query_object)
            self.session.commit()
            return {'id': query_object.id}
        except BaseException as e:
            print('Error for create method in DB:', e.args)
            self.session.rollback()
            return False

    def create_all(self, query_object: any) -> dict | bool:
        try:
            self.session.add_all(query_object)
            self.session.commit()
            ids = [item.id for item in query_object]
            return {'ids': ids}
        except BaseException as e:
            print('Error for create_all method id DB:', e.args)
            self.session.rollback()
            return False

    def update(self, table_name: any, condition: dict, update_value: dict) -> str | bool:
        try:
            self.session.query(table_name).filter_by(**condition).update(update_value)
            self.session.commit()
            return 'Successful updated'
        except BaseException as e:
            print('Error for update method in DB:', e.args)
            self.session.rollback()
            return False

    def delete(self, table_name: any, condition: dict) -> str | bool:
        try:
            self.session.query(table_name).filter_by(**condition).delete()
            self.session.commit()
            return 'Successful deleted'
        except BaseException as e:
            print('Error for delete method in DB:', e.args)
            self.session.rollback()
            return False

    def execute(self, query: str) -> list | bool:
        """
            execute("SELECT * FROM user WHERE id=5")
            :param query: str
            :return:
        """
        try:
            result = self.session.execute(query)
            self.session.commit()
            return [item for item in result]
        except BaseException as e:
            print('Error for execute method in DB:', e.args)
            self.session.rollback()
            return False

    def get_by(self, table_name: any, condition: dict, limit: int = 0, offset: int = 0) -> list | bool:
        try:
            if limit and not offset:
                result = self.session.query(table_name).filter_by(**condition).limit(limit).all()
            elif limit and offset:
                result = self.session.query(table_name).filter_by(**condition).limit(limit).offset(offset).all()
            else:
                result = self.session.query(table_name).filter_by(**condition).all()

            def object_as_dict(obj):
                return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

            return [object_as_dict(item) for item in result]
        except BaseException as e:
            print('Error for get_by method in DB:', e.args)
            return False

    def get_columns_by_filter(self, table_name: any, filter_expression: any, columns: [str] = None) -> list | bool:
        try:
            if columns:
                query = self.session.query(table_name).with_entities(*[Column(x) for x in columns])
            else:
                query = self.session.query(table_name)
            result = query.filter(filter_expression).all()
            return [dict(zip(columns, item)) for item in result]
        except BaseException as e:
            print('Error for get_columns_by_filter method in DB:', e.args)
            return False

    def get_by_id(self, table: any, row_id: int | str) -> dict | bool:
        """
        get row from DB by ID
        :param table: table model
        :param row_id: primary key
        :return: row
        """
        try:
            result = self.session.query(table).get(row_id)
            return {c.key: getattr(result, c.key) for c in inspect(result).mapper.column_attrs}
        except BaseException as e:
            print('Error for get_by_id method in DB:', e.args)
            return False

    def close(self):
        self.session.close()
        self.connection.dispose()


class DBHelper:
    def column(self, column: str, dimensions: int = 1, *args, **kwargs) -> Column:
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
        :param dimensions: 1
        :return: поле типа SQL
        """
        column_type = {
            'array': ARRAY,
            'biging': BIGINT,
            'giginteger': BigInteger,
            'binary': BINARY,
            'blob': BLOB,
            'bool': Boolean,
            'char': CHAR,
            'clob': CLOB,
            'date': Date,
            'datetime': DateTime,
            'decimal': DECIMAL,
            'emum': Enum,
            'float': Float(dimensions),
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
            'str': String(dimensions),
            'text': Text(dimensions),
            'time': Time,
            'timestamp': TIMESTAMP,
            'typedecoder': TypeDecorator,
            'unicode': Unicode,
            'unicodetext': UnicodeText,
            'varbinary': VARBINARY,
            'varchar': VARCHAR(dimensions),
            'varchar2': VARCHAR2(dimensions),
            'raw': RAW(dimensions),
        }.get(column, 'varchar')

        return Column(column_type, *args, **kwargs)
