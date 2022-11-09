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

        # Below ensures that there are at least 2 unique appearances of 'Alice', since it should be present both in the
        # character list and in the flash message (at minimum; other features may also have it present)
        assert rv.data.count(b'Alice') >= 2

        assert b'Added Alice' in rv.data

    def test_edit_character(self):
        rv = self.app.post('/add-character', data=dict(
            name='Charles'
        ), follow_redirects=True)

        assert rv.data.count(b'Charles') >= 2

        assert b'Added Charles' in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='James'
        ), follow_redirects=True)
        assert b'Added James' in rv.data

        edit_rv = self.app.post('/edit', data=dict(
            id=1
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
            id=2,
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
            id=1
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
            id=2
        ), follow_redirects=True)

        assert b'character was deleted' in deleted_rv.data

        assert b'Leo' not in deleted_rv.data

        assert b'Charles' in deleted_rv.data

    def test_relationship_adder_appearance(self):
        # Tests to ensure that the add relationship fields appear when (and only one) 2 or more characters exist
        rv = self.app.get('/')
        assert b'Add Relationship' not in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='George'
        ), follow_redirects=True)
        assert b'Add Relationship' not in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='Martha'
        ), follow_redirects=True)
        assert b'Add Relationship' in rv.data

    def test_add_relationship(self):
        self.app.post('/add-character', data=dict(name='George'), follow_redirects=True)
        self.app.post('/add-character', data=dict(name='Martha'), follow_redirects=True)
        rv = self.app.post('/add_relationship', data=dict(
            character1=1, character2=2, type='Spouse - Spouse', description=''
        ), follow_redirects=True)
        assert b'<b>George</b> <i>Spouse - Spouse</i> <b>Martha</b>' in rv.data

        rv = self.app.post('/add_relationship', data=dict(
            character1=1, character2=2,  custom_type='Friend - Friend', type='Custom', description='Friends since preschool'
        ), follow_redirects=True)
        assert b'<b>George</b> <i>Friend - Friend</i> <b>Martha</b>' in rv.data

        assert b'Friends since preschool' in rv.data

if __name__ == '__main__':
    unittest.main()
