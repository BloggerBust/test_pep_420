from implicit_namespace_foo.baz.my_baz import MyBaz


class MyBar:
    def __init__(self):
        print(f"{self.__class__.__name__} was created")
        my_baz = MyBaz()
