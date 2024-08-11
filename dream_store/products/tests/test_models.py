import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import (
    Category,
    Brand,
    CountryProduct,
    Product,
)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CategoryModelTest(TestCase):
    """
    Тестирование модели категорий.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        image_data = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x00\x00\x02\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )

        uploaded_file = SimpleUploadedFile(
            name='test_image.gif',
            content=image_data,
            content_type='image/gif'
        )

        cls.category = Category.objects.create(
            name='Электроника',
            description='Цифровые товары',
            image=uploaded_file,
            slug='elektronika'
        )

    def test_category_model_verbose_name(self):
        """
        Тест на корретность отображения verbose_name
        у модели Category.
        """

        category = CategoryModelTest.category
        field_verboses = {
            'name': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'slug': 'Слаг'
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    category._meta.get_field(
                        field).verbose_name, expected_value
                )

    def test_category_model_have_correct_name(self):
        """
        Тест на корректное отображение __str__
        у модели Category.
        """

        category = CategoryModelTest.category
        self.assertEqual(category.name, 'Электроника')

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


class BrandModelTest(TestCase):
    """
    Тестирование модели Brand.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.brand = Brand.objects.create(
            name='Apple',
            description='Компания из Купертино',
            slug='apple'
        )

    def test_brand_model_verbose_name(self):
        """
        Тест на корретность отображения verbose_name
        у модели Brand.
        """

        brand = BrandModelTest.brand
        field_verboses = {
            'name': 'Бренд',
            'description': 'Описание',
            'slug': 'Слаг'
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value,
                    brand._meta.get_field(field).verbose_name)

    def test_brand_model_have_correct_name(self):
        """
        Тест на корректность отобржаения __str__
        у модели Brand.
        """

        brand = BrandModelTest.brand
        self.assertEqual(brand.name, 'Apple')

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()


class CountryProductTest(TestCase):
    """
    Тест для модели CountryProduct.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.countryproduct = CountryProduct.objects.create(
            name='США'
        )

    def countryproduct_model_verbose_name(self):
        """
        Тест на корретность отображения verbose_name
        у модели CountryProduct.
        """

        brand = CountryProductTest.countryproduct
        self.assertCountEqual(
            brand._meta.get_field('name').verbose_name, 'Название страны')

    def countryproduct_model_have_correct_name(self):
        """
        Тест на корретность отображения __str__
        у модели CountryProduct.
        """

        brand = CountryProductTest.countryproduct
        self.assertEqual(brand.name, 'США')


class ProductTest(TestCase):
    """
    Тест модели Product.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        image_data = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\xff\x00\xff\xff\xff\x00\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x00\x00\x02\x00\x2c\x00\x00\x00\x00\x02\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile(
            name='test_image.gif',
            content=image_data,
            content_type='image/gif'
        )
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
            quantity=1,
            brand=cls.brand,
            category=cls.category,
            image=uploaded_file,
            description='Новый iphone',
            country=cls.countryproduct,
            vendor_code=999999,
            slug='iphone_15'
        )

    def test_product_verbose_name(self):
        """
        Тест на корректность отображения
        verbose_name у модели Product.
        """

        product = ProductTest.product
        field_verbose = {
            'name': 'Наименование',
            'price': 'Стоимость',
            'quantity': 'Количество товара',
            'brand': 'Бренд',
            'category': 'Категория',
            'image': 'Изображение',
            'description': 'Описание',
            'country': 'Страна',
            'vendor_code': 'Код товара',
            'slug': 'Слаг'
        }

        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    product._meta.get_field(field).verbose_name,
                    expected_value)

    def test_product_model_have_correct_name(self):
        """
        Тест на корректность отображения __str__ 
        у модели Product.
        """

        product = ProductTest.product
        self.assertEqual(product.name, 'Iphone 15 256 gb black')
