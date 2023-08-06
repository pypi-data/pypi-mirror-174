import typing
import json
import copy
import inspect
import sys
import dataclasses
from collections import OrderedDict
from typing import Any, NewType, Dict, Union, Callable, List, Tuple, Optional, Type
try:
    from typing import Literal  # type: ignore
except(ImportError):
    # Literal polyfill
    import types

    class _LiteralMeta(type):
        @classmethod
        def __getitem__(cls, key):
            tp = type(key[0] if isinstance(key, tuple) else key)

            def _make_cls(ns):
                class Origin:
                    pass

                origin = Origin()
                setattr(origin, '_name', 'Literal')
                ns['__origin__'] = origin
                ns['__args__'] = key
                return ns

            return types.new_class('Literal', (tp,), {}, _make_cls)

    class Literal(metaclass=_LiteralMeta):  # type: ignore
        pass
AllArguments = NewType('AllArguments', Dict[str, Any])
_empty = object()


class DefaultFactory:
    def __init__(self, factory, comp_value_fn=None):
        self.factory = factory
        self._comp_value_fn = comp_value_fn

    def __repr__(self):
        return repr(self.factory())

    def __str__(self):
        return str(self.factory())

    def __call__(self):
        return self.factory()

    def __eq__(self, other):
        if not isinstance(other, DefaultFactory):
            return self._get_comp_value(self) == other
        return self._get_comp_value(self) == self._get_comp_value(other)

    def _get_comp_value(self, value):
        if self._comp_value_fn is not None:
            return self._comp_value_fn(value)
        if isinstance(value, DefaultFactory):
            value = value()
        if isinstance(value, (int, str, float, bool)):
            return str(value)
        if value is None:
            return 'None'
        if isinstance(value, (list, tuple, set)):
            return '[' + ', '.join(sorted(self._get_comp_value(x) for x in value)) + ']'
        if isinstance(value, (dict, OrderedDict)):
            return '{' + ', '.join(sorted(f'{k}:{self._get_comp_value(v)}' for k, v in value.items())) + '}'
        return self._get_comp_value(vars(value))

    def __hash__(self):
        return hash(self._get_comp_value(self))

    def get_default(self):
        value = self()
        if isinstance(value, (int, str, float, bool)):
            return value
        return self

    @staticmethod
    def get_factory(value):
        if isinstance(value, DefaultFactory):
            return value
        if value == _empty or value == inspect._empty:
            return None
        return DefaultFactory(lambda: value)


@dataclasses.dataclass
class Parameter:
    name: Optional[str]
    type: Optional[Type]
    help: str = ''
    children: List['Parameter'] = dataclasses.field(default_factory=list, repr=False)
    default_factory: Optional[Callable[[], Any]] = None
    choices: Optional[List[Any]] = None
    argument_type: Optional[Any] = None
    _argument_name: Optional[Tuple[str]] = None
    is_container: Optional[bool] = None

    def walk(self, fn: Callable[['ParameterWithPath', List[Any]], Any], reverse: bool = False):
        def _walk(e, parent):
            e = ParameterWithPath(e, parent)
            new_children = []
            children = e.children
            if reverse:
                children = reversed(children)
            for p in children:
                result = _walk(p, e)
                if result is not None:
                    if isinstance(result, ParameterWithPath):
                        result = result.parameter
                    new_children.append(result)
            if reverse:
                new_children = list(reversed(new_children))
            return fn(e, children=new_children)
        result = _walk(self, None)
        if isinstance(result, ParameterWithPath):
            return result.parameter
        return result

    def enumerate_parameters(self):
        def _enumerate(e, parent):
            e = ParameterWithPath(e, parent)
            yield e
            for x in e.children:
                for y in _enumerate(x, e):
                    yield y
        return _enumerate(self, None)

    def find(self, name: str) -> Optional['Parameter']:
        for x in self.children:
            if x.name == name:
                return x
        return None

    @property
    def default(self):
        if self.default_factory is None:
            return None
        if isinstance(self.default_factory, DefaultFactory):
            return self.default_factory.get_default()
        return self.default_factory()

    def replace(self, **kwargs):
        return dataclasses.replace(self, **kwargs)


@dataclasses.dataclass
class ParameterWithPath:
    parameter: Parameter
    parent: Optional['ParameterWithPath'] = dataclasses.field(repr=False, default=None)

    @property
    def name(self):
        return self.parameter.name

    @property
    def type(self):
        return self.parameter.type

    @property
    def argument_type(self):
        return self.parameter.argument_type

    @property
    def children(self):
        return self.parameter.children

    @property
    def default_factory(self):
        return self.parameter.default_factory

    @property
    def default(self):
        return self.parameter.default

    @property
    def choices(self):
        return self.parameter.choices

    @property
    def help(self):
        return self.parameter.help

    @property
    def full_name(self):
        if self.parent is not None and self.parent.name is not None:
            return self.parent.full_name + '.' + self.name
        return self.name

    def find(self, name):
        child = self.parameter.find(name)
        if child is not None:
            return ParameterWithPath(child, self)
        return None

    @property
    def argument_name(self):
        if self.parameter._argument_name is not None:
            return self.parameter._argument_name[0]
        if self.parent is not None and self.parent.argument_name is not None:
            return self.parent.argument_name + '_' + self.name
        return self.name

    def replace(self, **kwargs):
        return ParameterWithPath(self.parameter.replace(**kwargs), self.parent)


class Runtime:
    def add_parameter(self, argument_name: str,
                      argument_type: Type, required: bool = True,
                      help: str = None,
                      default: Any = _empty, choices: Optional[List[Any]] = None):
        raise NotImplementedError('add_parameter is not implemented')

    def read_defaults(self, parameters: Parameter) -> Parameter:
        raise NotImplementedError('read_defaults is not implemented')


class Handler:
    def preprocess_parameter(self, parameter: ParameterWithPath) -> Tuple[bool, ParameterWithPath]:
        return False, parameter

    def parse_value(self, parameter: ParameterWithPath, value: Any) -> Tuple[bool, Any]:
        return False, value

    def bind(self, parameter: ParameterWithPath, args: Dict[str, Any], children: List[Tuple[Parameter, Any]]) -> Tuple[bool, Any]:
        return False, args

    def add_parameter(self, parameter: ParameterWithPath, parser: Runtime) -> bool:
        return False


class _ConditionalTypeMeta(type):
    def __new__(cls, name, bases, ns, prefix=True, default=None):
        """Create new typed dict class object.
        This method is called when ConditionalType is subclassed,
        or when ConditionalType is instantiated. This way
        ConditionalType supports all three syntax forms described in its docstring.
        Subclasses and instances of ConditionalType return actual dictionaries.
        """
        for base in bases:
            if type(base) is not _ConditionalTypeMeta:
                raise TypeError('cannot inherit from both a ConditionalType type '
                                'and a non-ConditionalType base class')

        annotations = {}
        own_annotations = ns.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__dict__.get('__annotations__', {}))

        annotations.update(own_annotations)
        tp = Union.__getitem__(tuple(annotations.values()) + (None,))
        setattr(tp, '__conditional_map__', annotations)
        setattr(tp, '__conditional_prefix__', prefix)
        setattr(tp, '__conditional_default__', default)
        return tp

    def __subclasscheck__(cls, other):
        # Typed dicts are only for static structural subtyping.
        raise TypeError('ConditionalType does not support instance and class checks')

    __instancecheck__ = __subclasscheck__


def ConditionalType(typename, fields=None, *, prefix: bool = True, default=None, **kwargs):
    """ConditionalType allows aparse to condition its choices for a
    specific parameter based on an argument.
    Usage::
        class Model(ConditionalType):
            gpt2: GPT2
            resnet: ResNet
    The type info can be accessed via the Model.__annotations__ dict,
    and the Model.__required_keys__ and Model.__optional_keys__ frozensets.
    ConditionalType supports two additional equivalent forms:
        Model = ConditionalType('Model', gpt2=GPT2, resnet=ResNet)
        Model = ConditionalType('Model', dict(gpt2=GPT2, resnet=ResNet))
    The class syntax is only supported in Python 3.6+, while two other
    syntax forms work for Python 2.7 and 3.2+
    """
    if fields is None:
        fields = kwargs
    elif kwargs:
        raise TypeError("ConditionalType takes either a dict or keyword arguments,"
                        " but not both")

    ns = {'__annotations__': dict(fields)}
    try:
        # Setting correct module is necessary to make typed dict classes pickleable.
        ns['__module__'] = sys._getframe(1).f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    return _ConditionalTypeMeta(typename, (), ns, prefix=prefix, default=default)


_ConditionalType = type.__new__(_ConditionalTypeMeta, 'ConditionalType', (), {})
setattr(ConditionalType, '__mro_entries__', lambda bases: (_ConditionalType,))


def WithArgumentName(cls, name=None):
    new_type = typing.NewType('WithArgumentName', cls)
    setattr(new_type, '__aparse_argname__', name)
    return new_type


def FunctionConditionalType(switch: Callable[[Dict[str, str]], Type], prefix: bool = True):
    tp = typing.NewType('FunctionConditionalType', Callable[[Dict[str, str]], Type])
    setattr(tp, '__conditional_fmap__', switch)
    setattr(tp, '__conditional_prefix__', prefix)
    return tp


def _forward_parameters(fn, outer_args, outer_kwargs, skip_first=False):
    def _fn(*args, **kwargs):
        kwargs = dict(**kwargs)
        kwargs.update(outer_kwargs)
        fn(*outer_args, *args, **kwargs)

    signature = inspect.signature(fn)
    output_params = []
    num_args = len(outer_args)
    for p, param in signature.parameters.items():
        if (param.kind == inspect._POSITIONAL_ONLY or param.kind == inspect._POSITIONAL_OR_KEYWORD) \
                and num_args > 0 and not skip_first:
            num_args -= 1
        elif param.name not in outer_kwargs:
            output_params.append(param)
        skip_first = False
    signature = inspect.Signature(output_params)
    setattr(_fn, '__signature__', signature)
    return _fn


def ForwardParameters(fn, *args, **kwargs):
    if inspect.isclass(fn):
        class WithDefaults(fn):
            pass

        init = getattr(fn, '__init__')
        init = _forward_parameters(init, args, kwargs, True)
        setattr(WithDefaults, '__init__', init)
        return WithDefaults
    else:
        return _forward_parameters(fn, args, kwargs)
