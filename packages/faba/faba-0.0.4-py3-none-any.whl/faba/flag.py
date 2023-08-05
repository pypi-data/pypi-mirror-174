from __future__ import annotations

import sys

from typing import List, Dict, Set, Tuple, Any, Union, Type, Optional

from . import exception


if sys.version_info < (3, 8):
    def get_origin(t: Type[Any]) -> Optional[Type[Any]]:
        return getattr(t, '__origin__', None)

    def get_args(t: Type[Any]) -> Tuple[Any, ...]:
        return getattr(t, '__args__', ())

else:
    from typing import get_origin, get_args


def _parse_list(args: List[str], arg_type: Type) -> Tuple(List[str], List):
    args = args[:]
    result = list()
    for index, value in enumerate(args):
        if value == '-':
            # get '-', parse end
            args[index] = None
            break
        if value is None or value.startswith('-'):
            # value already  parsed or is another flag, parse end
            break
        else:
            result.append(arg_type(value))
            args[index] = None
    return args, result


# very like _parse_list, but use add to insert value, rather than appen
def _parse_set(args: List[str], arg_type: Type) -> Tuple(List[str], List):
    args = args[:]
    result = set()
    for index, value in enumerate(args):
        if value == '-':
            # get '-', parse end
            args[index] = None
            break
        if value is None or value.startswith('-'):
            # value already  parsed or is another flag, parse end
            break
        else:
            result.add(arg_type(value))
            args[index] = None
    return args, result


def _parse_dict(args: List[str], key_type: Type, value_type: Type) -> Tuple(List[str], Dict):
    args = args[:]
    result = dict()

    for index, value in enumerate(args):
        if value == '-':
            args[index] = None
            break
        if value is None or value.startswith('-') or '=' not in value:
            # parsed, another flag, or value is not dict form (key=value)
            break
        else:
            k, v = value.split('=', 1)
            result[key_type(k)] = value_type(v)
            args[index] = None

    return args, result


class Flag:
    def __init__(
            self,
            *aliases: List[str],
            name: Optional[str] = None,
            type: Optional[Type] = None,
            default: Any = None,
            help: str = ''):

        self.aliases: List[str] = [i for i in aliases if i.startswith('-')]
        if len(self.aliases) == 0:
            raise ValueError('empty aliases')
        elif len(self.aliases) != len(aliases):
            invalid_aliases = list(set(aliases) - set(aliases))
            raise ValueError(
                f'alias must start with "-" but get {invalid_aliases}'
            )

        self.name: str = name
        if self.name is None:
            for alias in self.aliases:
                if alias.startswith('--'):
                    self.name = alias.lstrip('--')
                    break
        if self.name is None:
            raise ValueError('empty flag name')

        self.required: bool = True
        self.type: Type = self._uniform_type(type) if type is not None else str
        self.help: str = help

        self.value: Any = False if self.type == bool else default

    def _uniform_type(self, intype: Type) -> Type:
        """
        convert types for compatibility with python <= 3.8:
        list[x] -> List[x]
        dict[k,v] -> Dict[k,v]
        set[x] -> Set[x]

        List / list / List[Any] / list[Any] -> List[str]
        Dict / dict / Dict[Any, Any] / dict[any, any] -> Dict[str, str]
        Set / Set[any] / set / set[Any] -> Set[str]

        Optional[x] -> x with self.required=Flase
        """

        ori = get_origin(intype)
        args = get_args(intype)

        if ori == Union and len(args) == 2 and type(None) in args:
            # Optional[FlagTypes]
            self.required = False
            intype = args[0] if args.index(type(None)) == 1 else args[1]

            ori = get_origin(type)
            args = get_args(type)

        if intype in [list, List]:
            return List[str]
        elif intype in [Dict, dict]:
            return Dict[str, str]
        elif intype in [set, Set]:
            return Set[str]
        # Why is not list
        elif ori == List:
            return List[str] if args[0] == Any else List[args[0]]
        elif ori == Dict:
            args = [str if args[0] == Any else args[0]]
            return Dict[args[0], args[1]]
        elif ori == Set:
            return Set[str] if args[0] == Any else Set[args[0]]
        else:
            return intype

    def is_valid(self) -> bool:
        if self.value is None and self.required:
            return False
        # TODO : Check value is valid type
        return True

    def parse(self, args: List[Union[str, None]]) -> List[Union[str, None]]:
        """
        parse value from parameter "args",
        return a clone of "args" with "None" at used elements
        """
        ori_type, arg_types = get_origin(self.type), get_args(self.type)
        args = args.copy()

        # TODO: Support Enum

        for index, arg in enumerate(args):
            if arg is None:
                continue

            arg = arg.split('=', 1)

            if not arg[0].startswith('-') or not self.in_aliases(arg[0]):
                continue

            args[index] = None
            if self.type == bool:
                if len(arg) != 1:
                    self.value = bool(arg[1])
                else:
                    self.value = True if self.value is None else not self.value

            elif ori_type == list:
                assert len(arg_types) == 1
                arg_type = arg_types[0]
                if len(arg) > 1:
                    # argument format like --list=1,2,3
                    self.value = [arg_type(i) for i in arg[1].split(',')]
                    break
                else:
                    later_args, self.value = _parse_list(args[index+1:], arg_type)
                    args = args[:index+1] + later_args
            elif ori_type == set:
                assert len(arg_types) == 1
                arg_type = arg_types[0]
                if len(arg) > 1:
                    # argument format like --set=1,2,3
                    self.value = {arg_type(i) for i in arg[1].split(',')}
                    break
                else:
                    later_args, self.value = _parse_set(args[index+1:], arg_type)
                    args = args[:index+1] + later_args
            elif ori_type == dict:
                assert len(arg_types) == 2
                later_args, self.value = _parse_dict(args[index+1:], *arg_types)
                args = args[:index+1] + later_args
            else:
                if len(arg) > 1:
                    self.value = self.type(arg[1])
                    break
                elif len(args) < index + 2:
                    raise ValueError(f'need a value for flag "{arg[0]}"')

                self.value = self.type(args[index + 1])
                args[index + 1] = None

        return args

    def in_aliases(self, key: str) -> bool:
        return key in self.aliases

    def help_str(self):
        type_hint: str = ''
        ori_type, args_types = get_origin(self.type), get_args(self.type)

        if ori_type == list or ori_type == set:
            type_hint = f'[{args_types[0].__name__} ...]'
        elif ori_type == dict:
            type_hint = f'{{{args_types[0].__name__}={args_types[1].__name__} ...}}'
        elif self.type == bool:
            type_hint = ''
        else:
            type_hint = self.type.__name__

        return f'\t{"  ".join(self.aliases) + " " + type_hint:20}\t{self.help}'

    def __repr__(self) -> str:
        return f'<faba.Flag {self.name}:{self.value} {"required" if self.required else ""} {self.aliases}>'


class FlagSet:
    def __init__(self):
        self._flags: List[Flag] = list()

    def __iter__(self):
        yield from self._flags

    def get_flag(self, key: str) -> Flag:
        for flag in self._flags:
            if flag.name == key:
                return flag
        raise KeyError

    def __contains__(self, key: str):
        try:
            self.get_flag(key)
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> Any:
        return self.get_flag(key).value

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.get_flag(key).value
        except KeyError:
            return default

    def copy(self) -> FlagSet:
        nset = FlagSet()
        nset._flags = self._flags.copy()
        return nset

    def merge(self, flagset: FlagSet):
        for flag in flagset:
            self.add_flag(flag)
        return self

    def add_flag(self, flag: Flag):
        if flag.name in [i.name for i in self._flags]:
            raise exception.FlagError(flag, 'name conflict')

        cross = [
            alias
            for loflag in self._flags
            for alias in loflag.aliases
            if alias in flag.aliases
        ]
        if len(cross) != 0:
            raise exception.FlagError(flag, 'alias conflict')
        self._flags.append(flag)

    def parse(self, args: List[str]) -> List[str]:

        for flag in self._flags:
            args = flag.parse(args)

        return [i for i in args if i is not None]

    def validate(self):
        for flag in self._flags:
            if not flag.is_valid():
                raise exception.ValueError(f'conditions of flag "{flag.name}" are not satisfied')

    def as_dict(self):
        return {i.name: i.value for i in self._flags}

    def help_str(self):
        return 'Flags:\n' + '\n'.join([flag.help_str() for flag in self._flags])

    def __repr__(self):
        return f'<faba.FlagSet {self.asDict()}>'
