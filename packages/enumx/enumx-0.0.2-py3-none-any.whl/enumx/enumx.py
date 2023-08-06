#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Anebit Inc.
# All rights reserved.
#
# "Enumx" version 1.0
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of Anebit Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ---
# Author: Richard
# E-mail: richard.zen.liew@gmail.com
# Date  : 2022-10-15 12:20:00
#
# ---
# Description:
#   An extended enum for python.
#
# ---
# TODO (@Richard):
#   1. Complete unittests.
#
################################################################################

"""Introduction:
    An extended enum for python.
"""

__all__ = [
    "ExtendedEnumMeta",
    "ExtendedEnum",
    "IntegerEnum",
    "StringEnum",
]


from enum import EnumMeta, Enum, unique


class ExtendedEnumMeta(EnumMeta):
    """Description:
        An extended enum meta.
    """

    __DEFAULT_VALUE__ = object()

    #def __get__(cls, instance, owner):
    #    pass

    #def __set__(cls, instance, value):
    #    pass

    #def __delete__(cls, instance):
    #    pass

    #def __setitem__(cls, key, value):
    #    pass

    #def __delitem__(self, key):
    #    pass

    #def __getattribute__(cls, key):
    #    return object.__getattribute__(cls, key)

    #def __getattr__(cls, key):
    #    return cls.shuck(super().__getattr__(key))

    #def __setattr__(cls, key, value):
    #    super().__setattr__(key, value)

    #def __delattr__(cls, key):
    #    super().__delattr__(key)

    #def __len__(cls):
    #    return super().__len__()

    #def __bool__(cls):
    #    return True

    def __getitem__(cls, key):
        return cls.shuck(super().__getitem__(key))

    def __iter__(cls):
        return (
            cls.shuck(member)
            for member in super().__iter__()
        )

    def __reversed__(cls):
        return (
            cls.shuck(member)
            for member in super().__reversed__()
        )

    def __contains__(cls, item):
        return cls.shuck(item) in [
            cls.shuck(member)
            for member in cls.__members__.values()
        ]

    def __repr__(cls):
        return "<ExtendedEnum %r>" % cls.__name__

    @classmethod
    def is_enum(cls, value):
        mros = []
        if hasattr(value, "mro"):
            mros = getattr(value, "mro")()
        elif hasattr(value, "__mro__"):
            mros = getattr(value, "__mro__")
        elif hasattr(type(value), "mro"):
            mros = getattr(type(value), "mro")()
        elif hasattr(type(value), "__mro__"):
            mros = getattr(type(value), "__mro__")
        return Enum in mros or EnumMeta in mros

    @classmethod
    def shuck(cls, value):
        if cls.is_enum(value):
            value = getattr(value, "_value_", value)
        if type(value) is str and value == "None":
            value = None
        return value

    @staticmethod
    def unique(enumeration):
        return unique(enumeration)


class ExtendedEnum(Enum, metaclass=ExtendedEnumMeta):
    """Description:
        A extended enum.
    """

    __DEFAULT_VALUE__ = ExtendedEnumMeta.__DEFAULT_VALUE__
    __BASE_ENUMS__ = ()

    class __Decorators__(object):
        @staticmethod
        def base_first(function):
            def wrapper(cls, *args, **kwargs):
                result_function = function
                for base_enum in reversed(cls.__BASE_ENUMS__):
                    if cls.is_enum(base_enum):
                        if hasattr(base_enum, function.__name__):
                            cls = base_enum
                            result_function = getattr(cls, function.__name__)
                            break
                if hasattr(result_function, "__func__"):
                    result_function = result_function.__func__
                if not hasattr(result_function, "__call__"):
                    return result_function
                return result_function(cls, *args, **kwargs)
            return wrapper

    @classmethod
    @__Decorators__.base_first
    def __DEFAULT_WRAP__(cls, value):
        return cls.shuck(value)

    @classmethod
    @__Decorators__.base_first
    def __DEFAULT_EXCEPTS__(cls):
        return []

    #def __getattr__(self, key):
    #    return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        self.clones(reversed(self.__BASE_ENUMS__))
        if key == "_value_":
            pass
        if key == "_name_":
            pass
        if key == "__objclass__":
            pass
        super().__setattr__(key, value)

    def __contains__(self, other):
        return self.bare() == self.shuck(other)

    def __bool__(self):
        return bool(self.bare())

    def __or__(self, other):
        return bool(self.bare()) or bool(self.shuck(other))

    def __and__(self, other):
        return bool(self.bare()) and bool(self.shuck(other))

    def __xor__(self, other):
        return not (bool(self.bare()) == bool(self.shuck(other)))

    def __str__(self):
        return str(self.bare())

    def __repr__(self):
        return self.__str__()

    @classmethod
    def shuck(cls, value):
        return ExtendedEnumMeta.shuck(value)

    @classmethod
    def is_enum(cls, value):
        return ExtendedEnumMeta.is_enum(value)

    @classmethod
    def clone(cls, base_enum):
        if base_enum != cls.__DEFAULT_VALUE__ and base_enum is not None:
            if cls.is_enum(base_enum):
                if hasattr(base_enum, "_member_map_"):
                    member_map = getattr(base_enum, "_member_map_")
                    for key in member_map:
                        if key not in cls._member_map_:
                            cls._member_map_[key] = member_map[key]
                if hasattr(base_enum, "_member_names_"):
                    member_names = [
                        name
                        for name in getattr(base_enum, "_member_names_")
                        if name not in cls._member_names_
                    ]
                    cls._member_names_ = member_names + cls._member_names_

    @classmethod
    def clones(cls, base_enums=reversed(__BASE_ENUMS__)):
        for base_enum in base_enums:
            cls.clone(base_enum)

    @classmethod
    def members(cls, wrap_function=__DEFAULT_VALUE__, excepts=__DEFAULT_VALUE__):
        if wrap_function == cls.__DEFAULT_VALUE__:
            wrap_function = cls.__DEFAULT_WRAP__
        if excepts == cls.__DEFAULT_VALUE__:
            excepts = cls.__DEFAULT_EXCEPTS__()
        excepts = [cls.shuck(item) for item in excepts]
        results = []
        for member in cls.__members__.values():
            member = cls.shuck(member)
            if member not in excepts:
                if wrap_function is not None:
                    member = wrap_function(member)
                results.append(member)
        return results

    @classmethod
    def validate(cls, value,
                 wrap_function=__DEFAULT_VALUE__, excepts=__DEFAULT_VALUE__):
        if wrap_function == cls.__DEFAULT_VALUE__:
            wrap_function = cls.__DEFAULT_WRAP__
        value = cls.shuck(value)
        if wrap_function is not None:
            value = wrap_function(value)
        return value in cls.members(wrap_function, excepts)

    @classmethod
    def compare(cls, member, value, wrap_function=__DEFAULT_VALUE__):
        if wrap_function == cls.__DEFAULT_VALUE__:
            wrap_function = cls.__DEFAULT_WRAP__
        member, value = cls.shuck(member), cls.shuck(value)
        if wrap_function is not None:
            member, value = wrap_function(member), wrap_function(value)
        if member is None and value is None:
            return 0
        if member is None:
            return -1
        if value is None:
            return 1
        if member < value:
            return -1
        if member > value:
            return 1
        return 0

    def bare(self):
        return self.shuck(self)

    def lt(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) < 0

    def le(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) <= 0

    def eq(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) == 0

    def ne(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) != 0

    def gt(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) > 0

    def ge(self, value, wrap_function=__DEFAULT_VALUE__):
        return self.compare(self, value, wrap_function) >= 0


class IntegerEnum(int, ExtendedEnum):
    """Description:
        Enum where members are also (and must be) ints.
    """


class StringEnum(str, ExtendedEnum):
    """Description:
        Enum where members are also (and must be) strs.
    """

    @classmethod
    @ExtendedEnum.__Decorators__.base_first
    def __DEFAULT_EXCEPTS__(cls):
        if "NONE" in cls._member_names_:
            return [cls.NONE]
        return []

    def __repr__(self):
        return "'{}'".format(str(self.bare()))
