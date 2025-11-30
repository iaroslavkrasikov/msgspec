import pytest

import msgspec


def test_struct_omit_inheritance():
    class Base(msgspec.Struct):
        __struct_omit__ = ("secret",)
        name: str
        secret: str

    class User(Base):
        age: int

    u = User("alice", "hidden", 30)
    assert msgspec.json.encode(u) == b'{"name":"alice","age":30}'


def test_struct_omit_inheritance_merge():
    class Base(msgspec.Struct):
        __struct_omit__ = ("secret",)
        name: str
        secret: str

    class User(Base):
        __struct_omit__ = ("internal",)
        age: int
        internal: str

    u = User("alice", "hidden", 30, "ignored")
    assert msgspec.json.encode(u) == b'{"name":"alice","age":30}'


def test_struct_omit_asdict():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    d = msgspec.structs.asdict(u)
    assert d == {"name": "alice", "age": 30}
    assert "password" not in d


def test_struct_omit_asdict_inheritance():
    class Base(msgspec.Struct):
        __struct_omit__ = ("secret",)
        name: str
        secret: str

    class User(Base):
        age: int

    u = User("alice", "hidden", 30)
    d = msgspec.structs.asdict(u)
    assert d == {"name": "alice", "age": 30}
    assert "secret" not in d
