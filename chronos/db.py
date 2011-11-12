import sqlite3

class Factory(object):
    def __init__(self, location):
        self.location = location

    def create(self):
        conn = sqlite3.connect(self.location)
        return Cursor(conn)

class Cursor(object):
    def __init__(self, conn):
        self._conn = conn

    def get(self, table_name, attributes, model_id):
        args = (', '.join(attributes), table_name, model_id)
        query = "select %s from %s where id=%s" % args
        #TODO: handle IndexError cleanly
        row = self._conn.execute(query).fetchone()
        return dict(zip(attributes, row))

    def get_all(self, table_name, attributes, extra_query=None, extra_args=None):
        args = (', '.join(attributes), table_name)
        query = "select %s from %s" % args
        if extra_query:
            query = "%s %s" % (query, extra_query)
        rows = self._conn.execute(query, extra_args or ()).fetchall()
        return [dict(zip(attributes, row)) for row in rows]

    def close(self):
        self._conn.close()

    def add(self, table_name, data):
        (columns, values) = zip(*data.items())
        args = (table_name, ', '.join(columns),
                ', '.join(['?' for i in range(len(values))]))
        query = "insert into %s (%s) values (%s)" % args
        self._conn.execute(query, values)
        self._conn.commit()
