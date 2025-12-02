import msgspec


def test_struct_omit_json_encoding():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    encoded = msgspec.json.encode(u)
    assert b"password" not in encoded
    assert b"name" in encoded
    assert b"age" in encoded

    # Note: password will be missing in decoded object if it's not optional,
    # but here we are testing encoding.
    # If we want roundtrip, the omitted field must be optional or have default.


def test_struct_omit_msgpack_encoding():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    encoded = msgspec.msgpack.encode(u)
    decoded_dict = msgspec.msgpack.decode(encoded, type=dict)
    assert "password" not in decoded_dict
    assert "name" in decoded_dict
    assert "age" in decoded_dict


def test_struct_omit_inheritance():
    class Base(msgspec.Struct):
        __struct_omit__ = ("secret",)
        name: str
        secret: str

    class User(Base):
        __struct_omit__ = ("age",)
        age: int

    u = User("alice", "hidden", 30)
    encoded = msgspec.json.encode(u)
    assert b"secret" not in encoded
    assert b"age" not in encoded
    assert b"name" in encoded


def test_struct_omit_asdict():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    d = msgspec.structs.asdict(u)
    assert "password" not in d
    assert d["name"] == "alice"
    assert d["age"] == 30


def test_struct_omit_repr():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    assert repr(u) == "User(name='alice', age=30)"


def test_struct_omit_repr_inheritance():
    class Base(msgspec.Struct):
        __struct_omit__ = ("secret",)
        name: str
        secret: str

    class User(Base):
        age: int

    u = User("alice", "hidden", 30)
    assert repr(u) == "User(name='alice', age=30)"


def test_struct_omit_rich_repr():
    class User(msgspec.Struct):
        __struct_omit__ = ("password",)
        name: str
        password: str
        age: int

    u = User("alice", "secret", 30)
    assert u.__rich_repr__() == [("name", "alice"), ("age", 30)]
