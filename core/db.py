from typing import Any
from urllib.parse import quote_plus as urlquote

from sqlalchemy import (
    ARRAY,
    BIGINT,
    BINARY,
    BLOB,
    CHAR,
    CLOB,
    DECIMAL,
    JSON,
    NCHAR,
    NVARCHAR,
    REAL,
    TIMESTAMP,
    VARBINARY,
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    PickleType,
    SmallInteger,
    String,
    Text,
    Time,
    TypeDecorator,
    Unicode,
    UnicodeText,
    create_engine,
    inspect,
)
from sqlalchemy.dialects.oracle import RAW, VARCHAR2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from config import settings_config

BASE = declarative_base()


class DB:
    def __init__(self, session=None):
        self.session = session
        self.connection = None

    @staticmethod
    def _connection() -> create_engine:
        if settings_config.db.postgres.db_name == 'postgresql':
            engine = create_engine(
                f"postgresql://{settings_config.db.postgres.user}:{urlquote(settings_config.db.postgres.password)}@"
                f"{settings_config.db.postgres.host}:{settings_config.db.postgres.port}/"
                f"{settings_config.db.postgres.db_name}"
            )
        elif settings_config.db.mysql.db_name == 'mysql':
            engine = create_engine(
                f"mysql://{settings_config.db.mysql.user}:{urlquote(settings_config.db.mysql.password)}@"
                f"{settings_config.db.mysql.host}/{settings_config.db.mysql.db_name}"
            )
        elif settings_config.db.oracle.db_name == 'oracle':
            engine = create_engine(
                f"oracle://{settings_config.db.oracle.user}:{urlquote(settings_config.db.oracle.password)}@"
                f"{settings_config.db.oracle.host}:{settings_config.db.oracle.host}/"
                f"?service_name={settings_config.db.oracle.db_name}&mode=2"
            )
        elif settings_config.db.mssql.db_name == 'mssql':
            engine = create_engine(
                f"mssql+pyodbc://{settings_config.db.mssql.user}:{urlquote(settings_config.db.mssql.password)}@"
                f"{settings_config.db.mssql.db_name}"
            )
        elif settings_config.db.sqlite.db_name == 'sqlite':
            engine = create_engine(f"sqlite:///{settings_config.db.sqlite.path}")
        else:
            engine = None
        return engine

    def create_session(self) -> any:
        self.connection = self._connection()
        Session = sessionmaker(self.connection)
        if settings_config.db.postgres.db_name != 'postgresql':
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
            self.session.query(text(table_name)).filter_by(**condition).update(update_value)
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

    def execute(self, query: str) -> None | list[Any] | bool:
        try:
            result = self.session.execute(text(query))
            self.session.commit()
            if query.lower().startswith("update"):
                return
            if query.lower().startswith("insert"):
                return
            return [item for item in result]
        except BaseException as ex:
            print('Error for execute method in DB:', ex)
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

    def get_by_id(self, table: any, row_id: int or str):
        try:
            result = self.session.query(table).get(row_id)

            def object_as_dict(obj):
                return {c.key: getattr(obj, c.key)
                        for c in inspect(obj).mapper.column_attrs}

            return object_as_dict(result)
        except BaseException as e:
            print(e.args)
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
