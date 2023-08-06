import random

from erptools.signals import DisableSignals
from faker import Faker

from api.accounts.models import User, Store, AccountGroup, Tax, TaxAgency, Account, Terms



def get_store():
    faker = Faker(locale="en-CA")
    name = faker.company()
    store = Store.objects.create(
        name=name,
        domain=faker.url(),
        location="Canada",
        currency_code="CAD",
        email=faker.email(domain='thefurnitureguys.ca'),
        address=faker.address,
        name_legal=name,
        phone=faker.phone_number(),
        tax_number=faker.msisdn(),
        interact_email=f"{name}@thefurnitureguys.ca",
    )
    store.save()
    return store


def get_address():
    faker = Faker(locale="en-CA")
    a = faker.address()
    street, other = a.split('\n')
    city, other = a.split(',')
    province = other[:2]
    postal_code = other[3:]

    return street, city, province, postal_code



def generate_user(is_staff=False):
    faker = Faker(locale="en-CA")
    username = faker.user_name()
    password = faker.password()
    firstname = faker.first_name()
    lastname = faker.last_name()

    if is_staff:
        email = f"{username}@thefurnitureguys.ca"
    else:
        email = f"tfgerpdevelop+{username}@gmail.com"

    try:
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=firstname,
                                        last_name=lastname,
                                        email=email,
                                        is_superuser=is_staff,
                                        is_staff=is_staff,
                                        )

    except:
        return generate_user(is_staff)
    return user


def get_group(discount=None):
    faker = Faker(locale="en-CA")
    if not discount:
        discount = random.randint(0, 50)
    type = "tests"
    try:
        return AccountGroup.objects.get(type=type)
    except:
        return AccountGroup.objects.create(
            type=type,
            discount=discount
        )


def get_tax():
    if Tax.objects.filter(tax_code="HST").exists():
        return Tax.objects.get(tax_code="HST")
    tax_agency = TaxAgency.objects.get_or_create(display_name="Revenue Canada")[0]
    return Tax.objects.get_or_create(tax_code="HST", tax_percentage=0.13, tax_agency=tax_agency)[0]


def get_terms(terms_name):
    term_list = [
        {
            "terms_name": "COD",
            "terms_details": "Cash On Delivery",
            "days": 0,
            "on_order_conversion": 0.0,
            "on_production_commencing": 0.0,
            "on_leaving_for_delivery": 100.0,
            "on_install_complete": 0.0,
            "on_order_completion": 0.0
        },
        {
            "terms_name": "Deposit 50",
            "terms_details": "50% due on order confirmation\r\n50% due on Installation",
            "days": 0,
            "on_order_conversion": 50.0,
            "on_production_commencing": 0.0,
            "on_leaving_for_delivery": 0.0,
            "on_install_complete": 50.0,
            "on_order_completion": 0.0
        },
        {
            "terms_name": "Deposit 75",
            "terms_details": "75 on order confirmation, 25 on delivery",
            "days": 0,
            "on_order_conversion": 75.0,
            "on_production_commencing": 0.0,
            "on_leaving_for_delivery": 25.0,
            "on_install_complete": 0.0,
            "on_order_completion": 0.0
        },
        {
            "terms_name": "Prepaid",
            "terms_details": "100% due on order confirmation",
            "days": 0,
            "on_order_conversion": 100.0,
            "on_production_commencing": 0.0,
            "on_leaving_for_delivery": 0.0,
            "on_install_complete": 0.0,
            "on_order_completion": 0.0
        },
        {
            "terms_name": "progressive",
            "terms_details": "45% when order is place\r\n45% when order leaves for delivery\r\n10% when order is completed",
            "days": 15,
            "on_order_conversion": 45.0,
            "on_production_commencing": 0.0,
            "on_leaving_for_delivery": 45.0,
            "on_install_complete": 0.0,
            "on_order_completion": 10.0
        }
    ]
    if terms_name is None:
        choice = random.choice(term_list)
    else:
        choice = term_list[0]
        for choice in term_list:
            if terms_name == choice['terms_name']:
                break
    return Terms.objects.get_or_create(**choice)[0]


def generate_account(owner=None, users=None, sales_rep=None, store=None, group=None, term_name=None)->Account:
    with DisableSignals():
        faker = Faker(locale="en-CA")


        if not owner:
            owner = generate_user()
            owner.title = "Owner"

        if not users:
            users = []
            n_users = random.randint(0, 4)
            for i in range(n_users):
                users.append(generate_user())
        if not sales_rep:
            sales_rep = generate_user(True)

        if not store:
            store = get_store()

        if not group:
            group = get_group()

        # account info

        business_trade_name = faker.company()
        business_legal_name = business_trade_name
        business_email = f"tfgerpdevelop+{owner.username}.business@gmail.com"
        accounts_payable_email = f"tfgerpdevelop+{owner.username}.payable.@gmail.com"
        business_phone = faker.phone_number()
        business_country = 'Canada'
        business_address, business_city, business_state_province, business_post_code = get_address()
        group = get_group()
        tax = get_tax()

        payment_terms = get_terms(term_name)

        account = Account.objects.get_or_create(
            owner=owner,
            sales_rep=sales_rep,

            payment_terms=payment_terms,
            business_legal_name=business_legal_name,
            business_trade_name=business_trade_name,
            business_email=business_email,
            business_phone=business_phone,
            business_address=business_address,
            business_city=business_city,
            business_state_province=business_state_province,
            business_country=business_country,
            business_post_code=business_post_code,
            accounts_payable_name=faker.name(),
            accounts_payable_email=accounts_payable_email,
            store=store,
            group=group,

        )[0]
        tax = get_tax()
        account.tax.add(tax)
        for user in users:
            account.users.add(user)
        account.save()
        return account
