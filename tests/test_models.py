import unittest2

from chronos import models
from tests import common


fake_data = {
    'ftable': [
        {'id': 1, 'one': 'a', 'two': 'b'},
        {'id': 2, 'one': 'c', 'two': 'd'},
    ]
}
fake_db = common.FakeCursor(fake_data)


class FakeModel(models.BaseModel):
    attributes = ('id', 'one', 'two')
    table_name = 'ftable'


class TestBase(unittest2.TestCase):

    def setUp(self):
        pass

    def test_set_attribute(self):
        model = FakeModel(db=fake_db)
        model.one = '123'
        self.assertEqual(model.one, '123')

    def test_set_attribute_on_init(self):
        model = FakeModel(two='123', db=fake_db)
        self.assertEqual(model.two, '123')

    def test_set_attribute_overwrite(self):
        model = FakeModel(one='123', db=fake_db)
        self.assertEqual(model.one, '123')
        model.one = '789'
        self.assertEqual(model.one, '789')

    def test_set_attribute_unknown(self):
        model = FakeModel(db=fake_db)
        self.assertRaises(AttributeError, setattr, model, 'three', '123')

    def test_set_attribute_unknown_on_init(self):
        self.assertRaises(AttributeError, FakeModel,
                          one='123', three='asdf', db=fake_db)
        self.assertRaises(AttributeError, FakeModel,
                          three='what', db=fake_db)

    def test_get_attribute_from_db(self):
        model = FakeModel(id=1, db=fake_db)
        self.assertEqual(model.one, 'a')
        self.assertEqual(model.two, 'b')

    def test_get_attribute_from_db_does_not_overwrite(self):
        model = FakeModel(id=2, one='e', db=fake_db)
        self.assertEqual(model.one, 'e')
        self.assertEqual(model.two, 'd')


class TestResult(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        attributes = {
            'id': 123,
            'name': 'test_result',
            'duration': 100,
            'begin_timestamp': 1321063622,
        }
        result = models.Result(db=fake_db, **attributes)
        for key, value in attributes.items():
            self.assertEqual(value, getattr(result, key))
