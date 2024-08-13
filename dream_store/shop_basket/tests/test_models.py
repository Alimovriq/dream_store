from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from shop_basket.models import Shop_basket, Shop_basket_items
from products.models import (
    Product, Category, CountryProduct, Brand,)

USER = get_user_model()


class Shop_BasketModelTest(TestCase):
    """
    Тестирование основной модели Shop_basket
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = USER.objects.create_user(email='supertester@test.com')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.category = Category.objects.create(
            name='Электроника',
            description='Цифровые товары',
            slug='elektronika'
        )
        cls.brand = Brand.objects.create(
            name='Apple',
            description='Компания из Купертино',
            slug='apple'
        )
        cls.countryproduct = CountryProduct.objects.create(
            name='США'
        )
        cls.product = Product.objects.create(
            name='Iphone 15 256 gb black',
            price=100000,
            quantity=10,
            brand=cls.brand,
            category=cls.category,
            description='Новый iphone',
            country=cls.countryproduct,
            vendor_code=999999,
            slug='iphone_15'
        )
        cls.shop_basket_obj = Shop_basket.objects.create(
            customer=cls.user
        )
        cls.shop_basket_items_obj = Shop_basket_items.objects.create(
            shop_basket=cls.shop_basket_obj,
            product=cls.product,
            quantity=8
        )

    def test_shop_basket_model_verbose_name(self):
        """
        Тест на корректность отображения verbose_name
        у модели Shop_basket.
        """

        shop_basket = Shop_BasketModelTest.shop_basket_obj
        verbose_fields = {
            'products': 'Товары',
            'customer': 'Покупатель'
        }
        for field, expected_value in verbose_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value,
                    shop_basket._meta.get_field(field).verbose_name)

    def test_shop_basket_model_have_correct_name(self):
        """
        Тест на корректность отображения __str__ у 
        модели Shop_basket.
        """

        shop_basket = Shop_BasketModelTest.shop_basket_obj
        self.assertEqual(
            f'Корзина для {shop_basket.customer}',
            f'Корзина для supertester@test.com')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


class Shop_basket_itemsModelTest(TestCase):
    """
    Тестирование модели Shop_basket_items.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = USER.objects.create_user(email='supertester@test.com')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.category = Category.objects.create(
            name='Электроника',
            description='Цифровые товары',
            slug='elektronika'
        )
        cls.brand = Brand.objects.create(
            name='Apple',
            description='Компания из Купертино',
            slug='apple'
        )
        cls.countryproduct = CountryProduct.objects.create(
            name='США'
        )
        cls.product = Product.objects.create(
            name='Iphone 15 256 gb black',
            price=100000,
            quantity=10,
            brand=cls.brand,
            category=cls.category,
            description='Новый iphone',
            country=cls.countryproduct,
            vendor_code=999999,
            slug='iphone_15'
        )
        cls.shop_basket_obj = Shop_basket.objects.create(
            customer=cls.user
        )
        cls.shop_basket_items_obj = Shop_basket_items.objects.create(
            shop_basket=cls.shop_basket_obj,
            product=cls.product,
            quantity=8
        )

    def test_shop_basket_items_model_verbose_name(self):
        """
        Тест на корректность отображения verbose_name у 
        модели Shop_basket_items.
        """

        shop_basket_items = Shop_basket_itemsModelTest.shop_basket_items_obj
        verbose_fields = {
            'shop_basket': 'Корзина',
            'product': 'Товар',
            'quantity': 'Количество'
        }

        for field, expected_value in verbose_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value,
                    shop_basket_items._meta.get_field(field).verbose_name)

    def test_shop_basket_items_model_have_correct_name(self):
        """
        Тест на корректность отображения __str__ у
        модели Shop_basket_items.
        """

        shop_basket_items = Shop_basket_itemsModelTest.shop_basket_items_obj
        self.assertEqual(
            f'Объект корзины с {shop_basket_items.product} в кол-ве {shop_basket_items.quantity} ед.',
            f'Объект корзины с Iphone 15 256 gb black в кол-ве 8 ед.'
        )

    # def test_shop_basket_items_model_product_quantity_exists(self):
    #     """
    #     Тест на количество доступного товара для добавления в 
    #     корзину Пользователя.
    #     """

    #     shop_basket_items = Shop_basket_itemsModelTest.shop_basket_items_obj
    #     try:
    #         shop_basket_items.quantity = 50
    #     except ValidationError:
    #         print('lol?')
    #         return self.assertTrue(shop_basket_items.quantity == 5)