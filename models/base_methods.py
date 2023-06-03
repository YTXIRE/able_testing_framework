class DB_METHODS:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def get(self):
        return self.db.get(table_name=self.table_name)

    def add(self, query):
        return self.db.create(query_object=query)

    def add_all(self, query):
        return self.db.create_all(query_object=query)

    def update(self, condition, update_value):
        return self.db.update(table_name=self.table_name, condition=condition, update_value=update_value)

    def delete(self, condition):
        return self.db.delete(table_name=self.table_name, condition=condition)

    def execute(self, query):
        return self.db.execute(query=query)

    def get_by(self, condition):
        return self.db.get_by(table_name=self.table_name, condition=condition)
