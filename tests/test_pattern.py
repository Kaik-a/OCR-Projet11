"""Test pattern for other test"""
from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase, RequestFactory

from catalog.models import Product
from accounts.models import CustomUser, AwaitingData
from scrapping import NUTELLA


class TestPattern(TestCase):
    """Global set up"""

    def setUp(self) -> None:
        """Environment for tests"""
        self.factory = RequestFactory()
        self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')

        self.user = CustomUser.objects.create_user(
            username="test1",
            password="test1@1234",
            email="test@test.com"
        )

        self.client.login(username="test1", password="test1@1234")

        self.product_1 = Product(
            id=uuid4(),
            product_name_fr="produit bon",
            nutrition_grade_fr="A",
            categories_tags=["Pâte à tartiner"],
        )
        self.product_2 = Product(**NUTELLA)

        self.product_1.save()
        self.product_2.save()

        self.awaiting_data_1 = AwaitingData(
            guid=uuid4(),
            type="password",
            key="password",
            value="1234")

        self.awaiting_data_1.save()

        self.uuid_subscription = uuid4()
        self.awaiting_data_2 = AwaitingData(
            guid=self.uuid_subscription,
            type="subscription",
            key="login",
            value="test_login"
        )

        awaiting_subscription = [
            self.awaiting_data_2,
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="first_name",
                value="test_first_name"
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="last_name",
                value="test_last_name"
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="email",
                value="test2@test.com"
            ),
            AwaitingData(
                guid=self.uuid_subscription,
                type="subscription",
                key="password",
                value="12345"
            ),
        ]

        [data.save() for data in awaiting_subscription]

        self.stop_messages = patch('django.contrib.messages.add_message').start()

