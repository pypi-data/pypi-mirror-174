import os

from . import base_test


class UserLoginTestCase(base_test.NewUserTestCase):
    """
    This class is used to test the login functionality and
    check whether a user is successfully getting logged in to the
    system.
    """
    databases = '__all__'

    def setUp(self) -> None:
        self.accounts_base_url = os.environ.get('ACCOUNTS_API').strip('/')
        super().setUp()

    def test_user_login(self):
        r = self.session.get(url=f'{self.accounts_base_url}/accounts-group/')
        self.assertEqual(r.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
