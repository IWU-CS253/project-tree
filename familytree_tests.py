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
    def test_add_tree(self):
        rv = self.app.post('/add-tree', data=dict(
            tree_name="Tree1"
        ), follow_redirects=True)
        rv = self.app.get('/tree?tree_id=1&tree=Tree1')
        assert b'No display yet, so enjoy this cat'

    def test_add_character(self):
        self.test_add_tree()
        rv = self.app.post('/add-character', data=dict(
            name='Alice',
            tree_id=1
        ), follow_redirects=True)
        rv = self.app.post('/add-character', data=dict(
            name='George',
            tree_id=1
        ), follow_redirects=True)
        rv = self.app.post('/add-character', data=dict(
            name='Mortimer',
            tree_id=1
        ), follow_redirects=True)

        assert b'No characters added.' not in rv.data
        # Below ensures that there are at least 2 unique appearances of 'Mortimer', since it should be present both in the
        # character list and in the flash message (at minimum; other features may also have it present)
        assert rv.data.count(b'Mortimer') >= 2

        assert b'Added Mortimer' in rv.data

    def test_edit_character(self):
        self.test_add_tree()
        self.test_add_character()
        edit_rv = self.app.post('/edit', data=dict(
            id=1,
            tree_id=1
        ), follow_redirects=True)

        assert b'Alice' in edit_rv.data

        assert b'George' not in edit_rv.data

    def test_save_edit_character(self):
        self.test_add_tree()
        self.test_add_character()
        edited_rv = self.app.post('/save_edit', data=dict(
            id=2,
            name='Hannibal',
            tree_id=1
        ), follow_redirects=True)
        assert b'Alice' in edited_rv.data

        assert b'George' not in edited_rv.data

        assert b'Hannibal' in edited_rv.data

    def test_delete(self):
        self.test_add_tree()
        self.test_add_character()
        deleted_rv = self.app.post('/delete', data=dict(
            id=1,
            tree_id=1
        ), follow_redirects=True)

        assert b'character was deleted' in deleted_rv.data

        assert b'Alice' not in deleted_rv.data

    def test_delete_last(self):
        self.test_add_tree()
        self.test_add_character()
        deleted_rv = self.app.post('/delete', data=dict(
            id=3,
            tree_id=1
        ), follow_redirects=True)

        assert b'character was deleted' in deleted_rv.data

        assert b'Mortimer' not in deleted_rv.data

        assert b'George' in deleted_rv.data

    def test_add_relationship(self):
        self.test_add_tree()
        self.test_add_character()
        rv = self.app.post('/relationship', data=dict(
            character1=1,
            character2=2,
            type='Parent - Child',
            tree_id=1
        ), follow_redirects=True)

        assert b'Alice & George:'

    def test_relationship_adder_appearance(self):
        # Tests to ensure that the add relationship fields appear when (and only one) 2 or more characters exist
        self.test_add_tree()
        rv = self.app.post('/add-character', data=dict(
            name='Alice',
            tree_id=1
        ), follow_redirects=True)

        assert b'Add Relationship' not in rv.data

        rv = self.app.post('/add-character', data=dict(
            name='George',
            tree_id=1
        ), follow_redirects=True)

        assert b'Add Relationship' in rv.data

    def test_delete_relationship(self):
        self.test_add_tree()
        self.test_add_character()
        self.test_add_relationship()
        deleted_rv = self.app.post('/delete_relationship', data=dict(
            character1=1, character2=2, tree_id=1), follow_redirects=True)

        assert b'Alice & George:' not in deleted_rv.data
        
        assert b'relationship was deleted' in deleted_rv.data

if __name__ == '__main__':
    unittest.main()
