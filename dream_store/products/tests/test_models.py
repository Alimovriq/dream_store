import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
# from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import (
    Category,
    Brand,
    CountryProduct,
    Product,
)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dit=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CategoryModelTest(TestCase):
    """
    Тестирование модели категорий.
    """
    
    @classmethod
    