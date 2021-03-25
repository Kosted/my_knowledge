import pytest

from knowledge.models import RegularUser
from .conftest import TestFactory


class TestCase1(TestFactory):

    def test_create_user(self, create_user):
        user, info = create_user
        db_user = RegularUser.objects.filter(username=info.username, email=info.email)
        assert db_user[0].username == info.username, 'error !!!!!!!!!!!!!!!!!!!'
        assert len(RegularUser.objects.all()) == 1
