class DB_METHODS:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name

    def get_sql(self):
        return self.db.get(table_name=self.table_name)

    def add_sql(self, query):
        return self.db.create(query_object=query)

    def add_all_sql(self, query):
        return self.db.create_all(query_object=query)

    def update_sql(self, condition, update_value):
        return self.db.update(table_name=self.table_name, condition=condition, update_value=update_value)

    def delete_sql(self, condition):
        return self.db.delete(table_name=self.table_name, condition=condition)

    def execute_sql(self, query):
        return self.db.execute(query=query)

    def get_by_sql(self, condition):
        return self.db.get_by(table_name=self.table_name, condition=condition)
