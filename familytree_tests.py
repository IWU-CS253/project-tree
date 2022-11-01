import os
import app as familytree
import unittest
import tempfile


class FamilytreeTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, familytree.app.config['DATABASE'] = tempfile.mkstemp()
        familytree.app.testing = True
        self.app = familytree.app.test_client()
        with familytree.app.app_context():
            familytree.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(familytree.app.config['DATABASE'])

    # A simple placeholder test; can be removed once first tests are added
    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No characters added.' in rv.data

    def test_add_character(self):
        rv = self.app.post('/add-character', data=dict(
            name='Alice'
        ), follow_redirects=True)
        assert b'No characters added.' not in rv.data
        # Below ensures that there are 2 unique appearances of 'Alice', since it should be present both in the character
        # list and in the flash message.
        assert rv.data.count(b'Alice') == 2
        assert b'Added Alice' in rv.data


if __name__ == '__main__':
    unittest.main()
