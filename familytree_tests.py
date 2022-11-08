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

    def test_edit_character(self):
        rv = self.app.post('/add-character', data=dict(
            name='Charles'
        ), follow_redirects=True)
        assert b'Added Charles' in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='James'
        ), follow_redirects=True)
        assert b'Added James' in rv.data

        edit_rv = self.app.post('/edit', data=dict(
            name='Charles'
        ), follow_redirects=True)

        assert b'Charles' in edit_rv.data
        assert b'James' not in edit_rv.data

    def test_save_edit_character(self):
        rv = self.app.post('/add-character', data=dict(
            name='Charles'
        ), follow_redirects=True)

        assert b'Added Charles' in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='James'
        ), follow_redirects=True)
        assert b'Added James' in rv.data

        edited_rv = self.app.post('/save_edit', data=dict(
            rename='James',
            name='Hannibal'
        ), follow_redirects=True)
        assert b'Charles' in edited_rv.data
        assert b'James' not in edited_rv.data
        assert b'Hannibal' in edited_rv.data

    def test_delete(self):
        rv = self.app.post('/add-character', data=dict(
            name='Charles'
        ), follow_redirects=True)

        assert b'Added Charles' in rv.data

        deleted_rv = self.app.post('/delete', data=dict(
            name = 'Charles'
        ), follow_redirects=True)

        assert b'character was deleted' in deleted_rv.data
        assert b'Charles' not in deleted_rv.data

    def test_delete_last(self):
        rv = self.app.post('/add-character', data=dict(
            name='Charles'
        ), follow_redirects=True)

        assert b'Added Charles' in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='Leo'
        ), follow_redirects=True)

        assert b'Added Leo' in rv.data

        deleted_rv = self.app.post('/delete', data=dict(
            name='Leo'
        ), follow_redirects=True)

        assert b'character was deleted' in deleted_rv.data
        assert b'Leo' not in deleted_rv.data
        assert b'Charles' in deleted_rv.data



if __name__ == '__main__':
    unittest.main()
