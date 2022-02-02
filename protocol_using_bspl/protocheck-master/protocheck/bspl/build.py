#!/usr/bin/env python3

import tatsu
import os


grammar_path = os.path.join(os.path.dirname(__file__), "bspl.gr")


def build_parser():
    with open(grammar_path, "r", encoding="utf8") as grammar:
        # warning: dynamically compiled grammar is different from precompiled code
        model = tatsu.compile(grammar.read(), name="Bspl")
    return model


def save_parser(model):
    parser_path = os.path.join(os.path.dirname(__file__), "bspl_parser.py")
    with open(grammar_path, "r", encoding="utf8") as grammar:
        bspl_parser = tatsu.to_python_sourcecode(
            grammar.read(), "Bspl", "bspl_parser.py"
        )
        with open(parser_path, "w", encoding="utf8") as parser_file:
            parser_file.write(bspl_parser)
