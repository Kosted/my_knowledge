from collections import namedtuple

import pytest
from django.db.models import F
from faker import Faker
from rest_framework.authtoken.models import Token

from knowledge.models import RegularUser, Memory, Tag

fake = Faker()


@pytest.mark.django_db(transaction=True)
class TestFactory:

    def setUp(self) -> None:
        self.fake = Faker()


@pytest.fixture
def create_user():
    user_data_namedtuple = namedtuple('user', ['username', 'email', 'password'])
    user_data = user_data_namedtuple(fake.user_name(), fake.email(), fake.password())
    user = RegularUser.objects.create_user(*user_data)
    return user, user_data


@pytest.fixture
def login(create_user):
    user, user_data = create_user
    token = Token.objects.get_or_create(user)
    return token, user


@pytest.fixture
def make_user():
    def _make_user():
        return create_user

    return _make_user


@pytest.fixture
def do_login():
    def _do_login(user):
        token = Token.objects.get_or_create(user)
        return token, user

    return _do_login


@pytest.fixture
def make_memory():
    memory_namedtuple = namedtuple('memory', ['user', 'memory_text', 'tags', 'priority'])

    def _make_memory(user, tags: list, new_tags=0):
        m_data = memory_namedtuple(user, fake.text(), tags, fake.random_int(0, 10))
        memory = Memory.objects.create(user=user, memory_text=m_data.memory_text, priority=m_data.priority)
        m_data.tags.extend(
            list(Tag.objects.bulk_create([Tag(tag_text=fake.word(), user=user, count=0) for _ in range(new_tags)])))

        for tag in m_data.tags:
            memory.tags.add(tag)

        if m_data.tags:
            Tag.objects.filter(id__in=[tag.id for tag in m_data.tags]).update(count=F('count') + 1)

        return memory, m_data

    return _make_memory


@pytest.fixture
def make_tag():

    tag_namedtuple = namedtuple('tag', ['user', 'tag_text'])

    def _make_tag(user):
        tag_data = tag_namedtuple(user, fake.word())
        tag = Tag.objects.create(user=user, tag_text=tag_data.tag_text, count=0)
        return tag, tag_data

    return _make_tag


