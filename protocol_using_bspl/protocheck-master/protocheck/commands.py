#!/usr/bin/env python3
from protocheck import __version__
from protocheck.bspl import load_file

# Actions that only take one argument, and therefore can be repeated for each input file
class Commands:
    def version(self):
        """Print the currently running version of protocheck"""
        print(__version__)


def register_commands(new_commands):
    for k, v in new_commands.items():
        setattr(Commands, k, staticmethod(v))
