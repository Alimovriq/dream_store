import shutil
import tempfile

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import (
    Category,
    Brand,
    CountryProduct,
    Product,
    Shop_basket,
    Shop_basket_items,
    Order,
    OrderItems,)


MEDIA_ROOT = tempfile.mkdtemp()
USER = get_user_model()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class CategoryModelTest(TestCase):
    """
    Тестирование модели категорий.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория',
            description='Тестовое описание категории',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test_category',
            meta_title='test_meta_title',
            meta_description='test_meta_description'
        )

    def test_category_model_have_correct_object_name(self):
        """
        Тестирование корректности отображения
        __str__ у модели категорий.
        """

        category = CategoryModelTest.category
        expected_category_name = category.name
        self.assertEqual(expected_category_name, str(category))

    def test_category_model_verbose_name(self):
        """
        Тестирование verbose_name у модели категорий.
        """

        category = CategoryModelTest.category
        field_verboses = {
            "name": "Название",
            "description": "Описание",
            "image": "Изображение",
            "slug": "Слаг"
        }
        for field_name, expected_value in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    category._meta.get_field(
                        field_name
                    ).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class BrandModelTest(TestCase):
    """
    Тестирование модели брендов.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = Brand.objects.create(
            name='Тестовый бренд',
            description='Описание тестового бренда',
            slug='test_brand'
        )

    def test_brand_have_correct_object_name(self):
        """
        Тестирование корректности отображения
        __str__ у модели брендов.
        """

        brand = BrandModelTest.brand
        expected_brand_name = brand.name
        self.assertEqual(expected_brand_name, str(brand))

    def test_brand_model_verbose_name(self):
        """
        Тестирование verbose_name у модели брендов.
        """

        brand = BrandModelTest.brand
        field_verboses = {
            "name": "Бренд",
            "description": "Описание",
            "slug": "Слаг"
        }
        for field_name, expected_value in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(brand._meta.get_field(
                    field_name
                ).verbose_name, expected_value)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class CountryProductModelTest(TestCase):
    """
    Тестирование модели стран для товаров.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.countryproduct = CountryProduct.objects.create(
            name="Тестовая страна"
        )

    def test_countryproduct_model_have_correct_object_name(self):
        """
        Тестирование корректности отображения
        __str__ у модели брендов.
        """

        countryproduct = CountryProductModelTest.countryproduct
        expected_countryproduct_name = countryproduct.name
        self.assertEqual(
            expected_countryproduct_name,
            str(countryproduct))

    def test_countryproduct_verbose_name(self):
        """
        Тестирование verbose_name у модели
        стран для товаров.
        """

        countryproduct = CountryProductModelTest.countryproduct
        field_verboses = {
            "name": "Название страны"
        }
        for field_name, expected_value in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    countryproduct._meta.get_field(
                        field_name
                    ).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProductModelTest(TestCase):
    """
    Тестирование модели товаров.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория',
            description='Тестовое описание категории',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test_category',
            meta_title='test_meta_title',
            meta_description='test_meta_description'
        )
        cls.countryproduct = CountryProduct.objects.create(
            name="Тестовая страна"
        )
        cls.brand = Brand.objects.create(
            name='Тестовый бренд',
            description='Описание тестового бренда',
            slug='test_brand'
        )
        cls.product = Product.objects.create(
            name="Тестовый товар",
            price=1000.00,
            quantity=100,
            brand=cls.brand,
            category=cls.category,
            image=SimpleUploadedFile(
                "test2.jpg", b"something2"
            ),
            description="Тестовое описание товара",
            country=cls.countryproduct,
            slug="test_product"
        )

    def test_product_model_have_correct_object_name(self):
        """
        Тестирование корректности отображения
        __str__ у модели товаров.
        """

        product = ProductModelTest.product
        expected_product_name = product.name
        self.assertEqual(
            expected_product_name, str(product))

    def test_product_verbose_name(self):
        """
        Тестирование verbose_name у модели
        товаров.
        """

        product = ProductModelTest.product
        field_verboses = {
            "name": "Наименование",
            "price": "Стоимость",
            "brand": "Бренд",
            "category": "Категория",
            "image": "Изображение",
            "description": "Описание",
            "country": "Страна",
            "slug": "Слаг"
        }
        for field_name, expected_value in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    product._meta.get_field(
                        field_name).verbose_name, expected_value)


class Shop_basketTest(TestCase):
    """
    Тестирование модели корзина.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория',
            description='Тестовое описание категории',
            image=SimpleUploadedFile(
                'test.jpg', b'something'),
            slug='test_category',
            meta_title='test_meta_title',
            meta_description='test_meta_description'
        )
        cls.countryproduct = CountryProduct.objects.create(
            name="Тестовая страна"
        )
        cls.brand = Brand.objects.create(
            name='Тестовый бренд',
            description='Описание тестового бренда',
            slug='test_brand'
        )
        cls.product = Product.objects.create(
            name="Тестовый товар",
            price=1000.00,
            quantity=100,
            brand=cls.brand,
            category=cls.category,
            image=SimpleUploadedFile(
                "test2.jpg", b"something2"
            ),
            description="Тестовое описание товара",
            country=cls.countryproduct,
            slug="test_product"
        )
        cls.customer = USER.objects.create(
            email='test@test.com',
            password='test123'
        )
        cls.shop_basket = Shop_basket.objects.create(
            customer=cls.customer
        )
        cls.shop_basket.products.add(
            cls.product)

    def test_shop_basket_model_have_correct_object_name(self):
        """
        Тестирование корректности отображения
        __str__ у модели корзина.
        """

        shop_basket = Shop_basketTest.shop_basket.__str__()
        expected_value = f'Корзина для {self.customer}'
        self.assertEqual(shop_basket, expected_value)

    def test_shop_basket_verbose_name(self):
        """
        Тестирование verbose_name у
        модели shop_basket.
        """

        shop_basket = Shop_basketTest.shop_basket
        field_verboses = {
            'products': 'Товары',
            'customer': 'Покупатель'
        }
        for field_name, expected_value in field_verboses.items():
            with self.subTest(field_name=field_name):
                self.assertEqual(
                    shop_basket._meta.get_field(
                        field_name).verbose_name, expected_value
                )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    # class Shop_basket_itemsTest(TestCase):
    #     """
    #     Тестирование модели товаров 
    #     для корзины.
    #     """

    #     @classmethod
    #     def setUpClas(cls):
    #         super().setUpClass()
    #         cls.