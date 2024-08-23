from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from orders.models import Order, OrderItems, OrderRefund, OrderItemsRefund
from products.models import Product, Category, CountryProduct, Brand

USER = get_user_model()


class OrderModelTest(TestCase):
    """
    Тестирование основной модели Order.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.customer = USER.objects.create_user(email='supertester@test.com')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.customer)

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
        cls.order = Order.objects.create(
            customer=cls.customer,
            phone='89238574598',
            email='supertester@test.com',
            comment='Тестовый коммент к заказу',
            address='г.Москва, улица Удачи'
        )
        cls.order_items = OrderItems.objects.create(
            order=cls.order,
            product=cls.product,
            quantity=1
        )

    def test_order_model_verbose_name(self):
        """
        Тест на корректность отображения verbose_name
        у модели Order.
        """

        order_obj = OrderModelTest.order
        verbose_fields = {
            'customer': 'Покупатель',
            'products': 'Товары',
            'total_price': 'Итоговая стоимость',
            'created_at': 'Дата заказа',
            'phone': 'Номер телефона',
            'email': 'Email',
            'address': 'Адрес доставки',
            'status': 'Статус Заказа',
            'is_payed': 'Статус оплаты'
        }

        for field, expected_value in verbose_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value,
                    order_obj._meta.get_field(field).verbose_name
                )

    def test_order_model_have_correct_name(self):
        """
        Тест на корректность отображения __str__
        у модели Order.
        """

        order_obj = OrderModelTest.order
        self.assertEqual(
            f'Заказ № {order_obj.pk}',
            'Заказ № 1'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
