from __future__ import annotations
# Python 3.7 required

import sys
import copy
from typing import List, Optional, Callable

from .flag import FlagSet, Flag
from . import exception


class Command:
    def __init__(
            self,
            use: str,
            aliases: Optional[List[str]] = None,

            short: str = '',
            long: str = '',

            flags: Optional[FlagSet] = None,

            persistent_pre_run: Optional[Callable[[Command, List[str]], None]] = None,
            run: Optional[Callable[[Command, List[str]], None]] = None,
            persistent_post_run: Optional[Callable[[Command, List[str]], None]] = None,

            help_func: Optional[Callable[[Command], None]] = None):

        self.use = use
        self.aliases = [use.split()[0], ] if aliases is None else aliases

        self.short, self.long = short, long

        self.flags = FlagSet() if flags is None else flags

        self.persistent_pre_run = persistent_pre_run
        self.run = run
        self.persistent_post_run = persistent_post_run

        self.help_func = help_func

        self.parent = None
        self.sub_commands: List[Command] = list()

    def copy(self) -> Command:
        return copy.deepcopy(self)

    def _execute(self, args: List[str]):

        if self.flags.get('help'):
            self.print_help(args)

        elif self.run is None:
            if len(args) != 0:
                raise exception.ParseError(args[0], 'unknown command')

            self.print_help(args)

        else:
            self.run(self, args)

    def execute(self,
                args: Optional[List[str]] = None,
                oflags: FlagSet = None):
        # a command only can run once, it will be dirty after executed

        if self.parent is None and 'help' not in self.flags:
            self.add_flag('-h', '--help', name='help', type=bool)

        args = sys.argv[1:] if args is None else args
        args = self.flags.parse(args)

        if len(args) != 0 and args[0].startswith('-'):
            raise exception.ParseError(args[0], 'unknown flag')
        if oflags is not None:
            self.flags = self.flags.merge(oflags)

        self.flags.validate()
        if self.persistent_pre_run:
            self.persistent_pre_run(self, args)

        cmd = self._find_next(args)

        if cmd is None:
            self._execute(args)
        else:
            cmd.execute(args[1:], self.flags)

        if self.persistent_post_run:
            self.persistent_post_run(self, args)

    def _find_next(self, args: List[str]) -> Optional[Command]:
        if len(args) == 0:
            return None
        elif args[0].startswith('-'):
            raise exception.ParseError(args[0], 'unknown command')
        else:
            for cmd in self.sub_commands:
                if cmd.is_name(args[0]):
                    return cmd
            return None

    def is_name(self, name: str) -> bool:
        return name in self.aliases

    def add_command(self, cmd: Command):
        cmd.parent = self
        self.sub_commands.append(cmd)

    def add_flag(self, *args, **kwargs):
        self.flags.add_flag(Flag(*args, **kwargs))

    def print_help(self, args: List[str]):
        if self.help_func is not None:
            self.help_func(self.flags, args)
        else:
            self._default_help_func(args)

    def _default_help_func(self, args: List[str]):
        flag_desc = self.flags.help_str()
        usage_desc = f'Usage:\n\t{self.use}\n'
        desc = self.long if self.long != '' else self.short
        desc = '' if desc is None else desc + '\n'
        cmds_desc = 'Available Commands:\n'

        max_cmd_len = 0
        max_cmd_len = max([max_cmd_len] + [len(' '.join(cmd.aliases)) for cmd in self.sub_commands]) + 5
        for cmd in self.sub_commands:
            cmd_desc = " ".join(cmd.aliases)
            cmd_desc += ' '*(max_cmd_len - len(cmd_desc))
            cmds_desc += f'\t{cmd_desc}{cmd.short}\n'
        print(f"""{desc}\n{usage_desc}\n{cmds_desc}\n{flag_desc}""".strip())
