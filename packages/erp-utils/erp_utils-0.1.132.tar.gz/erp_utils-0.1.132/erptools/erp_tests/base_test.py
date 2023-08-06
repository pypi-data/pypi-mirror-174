import requests
from api.accounts.models import User
from faker import Faker
from rest_framework.test import APITestCase

from erptools.microservices import authenticate_and_get_token
from erptools.erp_tests.generate_account_objects import generate_account, generate_user

class NewUserTestCase(APITestCase):
    """
    This class is going to be inherited by other sub-classes.
    """

    def setUp(self) -> None:
        faker = Faker()
        self.username = faker.user_name()
        self.password = faker.password()
        self.email = faker.email()
        self.firstname = faker.first_name()
        self.lastname = faker.last_name()
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             first_name=self.firstname,
                                             last_name=self.lastname,
                                             email=self.email)

        self.session = requests.Session()
        credentials = authenticate_and_get_token(self.username, self.password)
        self.session.headers.update({'authorization': credentials})

        self.sales_rep = generate_user(True)
        self.account = generate_account(owner=self.user, sales_rep=self.sales_rep)

    def tearDown(self) -> None:
        self.user.delete()
