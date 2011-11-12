

class FakeCursor(object):

    def __init__(self, data=None):
        self.data = data or {}

    def get(self, table_name, attributes, model_id):
        for row in self.data[table_name]:
            if row['id'] == model_id:
                return row
        raise KeyError(model_id)
