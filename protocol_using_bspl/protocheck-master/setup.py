#!/usr/bin/env python
from setuptools import setup
from setuptools.command.build_py import build_py
import sys


class Build(build_py):
    def run(self):
        sys.path.append("./")
        from protocheck.bspl.build import build_parser, save_parser

        model = build_parser()
        save_parser(model)
        super(Build, self).run()


setup(
    cmdclass={
        "build_py": Build,
    }
)
