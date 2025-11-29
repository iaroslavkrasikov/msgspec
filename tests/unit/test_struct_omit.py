import pytest

import msgspec


def test_struct_omit_json():
    class User(msgspec.Struct, omit_defaults=True):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int = 0

    u = User("alice", "secret", 30)
    assert msgspec.json.encode(u) == b'{"name":"alice","age":30}'

    u2 = User("bob", "secret")
    assert msgspec.json.encode(u2) == b'{"name":"bob"}'


def test_struct_omit_msgpack():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int = 0

    u = User("alice", "secret", 30)
    encoded = msgspec.msgpack.encode(u)
    decoded = msgspec.msgpack.decode(encoded)
    # Since we can't decode back to User (missing password), we decode to dict
    assert decoded == {"name": "alice", "age": 30}


def test_struct_omit_invalid_field():
    with pytest.raises(
        ValueError, match="Field 'invalid' in __struct_omit__ is not a field"
    ):

        class User(msgspec.Struct):
            __struct_omit__ = ("invalid",)
            name: str


def test_struct_omit_invalid_type():
    with pytest.raises(TypeError, match="__struct_omit__ must be a tuple or list"):

        class User(msgspec.Struct):
            __struct_omit__ = "invalid"
            name: str


def test_struct_omit_rename():
    class User(msgspec.Struct, rename="camel"):
        __struct_omit__ = ("password",)
        first_name: str
        password: str

    u = User("alice", "secret")
    assert msgspec.json.encode(u) == b'{"firstName":"alice"}'
