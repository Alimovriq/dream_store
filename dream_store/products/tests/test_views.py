import shutil
import tempfile
from django.conf import settings

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from products.models import (
    Category,
    Brand,
    CountryProduct,
    Product,
    Shop_basket,
    Shop_basket_items,
    Order,
    OrderItems,)


USER = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ProductsViewsTests(TestCase):
    """
    Тестирование представления в
    приложении Products (вкл. корзину
    и заказы для пользователей).
    """

    user_data = {
        'email': 'test_user@example.ru',
        'password': 'test_user_password'
    }
    superuser_data = {
        'email': 'test_superuser@example.ru',
        'password': 'test_super_user_password'
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = USER.objects.create(
            **ProductsViewsTests.user_data
        )
        cls.super_user = USER.objects.create(
            **ProductsViewsTests.superuser_data
        )
        cls.category_1 = Category.objects.create(
            name='Тестовая категория',
            description='Тестовое описание категории',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test_category',
            meta_title='test_meta_title',
            meta_description='test_meta_description'
        )
        cls.countryproduct_1 = CountryProduct.objects.create(
            name='Тестовая страна'
        )
        cls.brand_1 = Brand.objects.create(
            name='Тестовый бренд',
            description='Описание тестового бренда',
            slug='test_brand'
        )
        cls.product_1 = Product.objects.create(
            name='Тестовый товар №1',
            price=1000.00,
            quantity=100,
            brand=cls.brand_1,
            category=cls.category_1,
            image=SimpleUploadedFile(
                'test2.jpg', b'something2'
            ),
            description="Тестовое описание товара №1",
            country=cls.countryproduct_1,
            slug='test_produc_1'
        )
        cls.product_2 = Product.objects.create(
            name='Тестовый товар №2',
            price=3000.00,
            quantity=30,
            brand=cls.brand_1,
            category=cls.category_1,
            image=SimpleUploadedFile(
                'test2.jpg', b'something2'
            ),
            description='Тестовое описание товара №2',
            country=cls.countryproduct_1,
            slug='test_product_2'
        )
        cls.customer = cls.user
        cls.shop_basket = Shop_basket.objects.create(
            customer=cls.user
        )
        cls.shop_basket_item = Shop_basket_items.objects.create(
            shop_basket=cls.shop_basket,
            product=cls.product_1,
            quantity=100
        )
        cls.order = Order.objects.create(
            customer=cls.user,
            total_price=1000,
            created_at='24 января 2024 г. 17:23',
            address='Тестовый адрес доставки',
            is_payed=False
            )
        cls.orderitems = OrderItems.objects.create(
            order=cls.order,
            product=cls.product_2,
            quantity=20)

    def setUp(self):
        super().setUp()
        self.unauthorized_client = APIClient()
        self.authorized_client = APIClient()
        # self.authorized_client.force_authenticate(
        #     ProductsViewsTests.user
        # )
        self.authorized_client.force_login(
            ProductsViewsTests.user
        )
        self.superuser_client = APIClient()
        self.superuser_client.force_login(
            ProductsViewsTests.super_user
        )

    def test_unauth_user_get_list_products_filtered_by_category(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по категории "Тестовая категория".
        """

        address = '/api/v1/products/?category=Тестовая категория'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            2, products_count,
            'Пользователь получил неверный список товаров по фильтру категория')

    def test_unauth_user_get_list_products_filtered_by_brand(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по бренду "Тестовый бренд".
        """

        address = '/api/v1/products/?brand=Тестовый бренд'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            2, products_count,
            'Пользователь получил неверный список товаров по фильтру бренд')

    def test_unauth_user_get_list_products_filtered_by_country(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по стране "Тестовая страна".
        """
        address = '/api/v1/products/?country=Тестовая страна'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            2, products_count,
            'Пользователь получил неверный список товаров по фильтру страна')

    def test_unauth_user_get_list_products_filtered_by_name(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по имени "Тестовый товар №1".
        """

        address = '/api/v1/products/?name=Тестовый товар №1'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            1, products_count,
            'Пользователь получил неверный список товаров по фильтру имя')

    def test_unauth_user_list_products_filtered_by_min_price(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по стоимости >= 2000.
        """

        address = '/api/v1/products/?min_price=2000'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            1, products_count,
            'Пользователь получил неверный список товаров по фильтру >= 2000')

    def test_unauth_user_list_products_filtered_by_max_price(self):
        """
        Получение неавторизованным пользователем списка товаров,
        отфильтрованных по стоимости <= 2000.
        """

        address = '/api/v1/products/?max_price=2000'
        response = self.unauthorized_client.get(address)
        products_count = len(response.data.get('results'))
        self.assertEqual(
            1, products_count,
            'Пользователь получил неверный список товаров по фильтру <= 2000')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(
            TEMP_MEDIA_ROOT,
            ignore_errors=True)
