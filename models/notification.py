from core.db import DB, DBHelper, BASE
from models.base_methods import DB_METHODS

db = DBHelper()


class Notification(DB, BASE, DB_METHODS):
    __tablename__ = 'Notification'
    __table_args__ = {'schema': 'public'}

    NotificationId = db.column(column='int', primary_key=True)
    Message = db.column(column='json')
    Created = db.column(column='timestamp')
    AttemptQuantity = db.column(column='int')

    def __init__(self, session, data=None):
        if data is None:
            data = {}
        super().__init__(session)
        self.NotificationId = data.get('NotificationId', '')
        self.Message = data.get('Message', '')
        self.Created = data.get('Created', '')
        self.AttemptQuantity = data.get('AttemptQuantity', '')
        DB_METHODS.__init__(self, db=self, table_name=Notification)
