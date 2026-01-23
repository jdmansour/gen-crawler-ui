
from __future__ import annotations
from typing import cast

class MyBaseClass:
    @classmethod
    def create(cls):
        return cls()

class MyDerivedClass(MyBaseClass):
    static = "some_static_value"
    @classmethod
    def create(cls: type['MyDerivedClass']) -> 'MyDerivedClass':
        mc = super(MyDerivedClass, cls).create()
        # Casting or explicit type annotation doesn't help,
        # nor does assigning to a different variable
        mdc: MyDerivedClass = cast(MyDerivedClass, mc)
        # Assert doesn't help
        assert isinstance(mdc, MyDerivedClass)
        
        # this would work:
        # mc = MyDerivedClass()

        # try to access the callback
        # PyLint complains with Pylint(E1101:no-member)
        # Instance of 'MyBaseClass' has no 'my_callback' member
        print(mdc.my_callback)
        return mdc

    def my_callback(self):
        print("Callback method executed.")