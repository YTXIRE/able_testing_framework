from core.db.db import DB, DBHelper, BASE

db = DBHelper()


class Language(BASE, DB):
    __tablename__ = 'languages'

    id = db.column(column='int', primary_key=True)
    name = db.column(column='str')
    iso_code = db.column(column='str')
    code = db.column(column='str')
    voice_name = db.column(column='str')

    def __init__(self, name=None, iso_code=None, code=None, voice_name=None):
        self.name = name
        self.iso_code = iso_code
        self.code = code
        self.voice_name = voice_name

    def get_lang(self, environment):
        return self.get(table_name=Language, environment=environment)

    def add_lang(self, environment, query):
        return self.create(query_object=query, environment=environment)

    def add_langs(self, environment, query):
        return self.create_all(query_object=query, environment=environment)

    def update_lang(self, environment, condition, update_value):
        return self.update(table_name=Language, environment=environment, condition=condition, update_value=update_value)

    def delete_lang(self, environment, condition):
        return self.delete(table_name=Language, environment=environment, condition=condition)

    def execute_lang(self, environment, query):
        return self.execute(environment=environment, query=query)

    def get_lang_by(self, environment, condition):
        return self.get_by(table_name=Language, environment=environment, condition=condition)
