#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from textwrap import dedent
import random

import rich
import rich.color
from .__init__ import __version__ 

def say():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)
    elif "--help" in sys.argv[1:]:
        print("cowsay MESSAGE [MESSAGE]")
        exit(0)

    phrase = " ".join(sys.argv[1:])
    topbar = "-" * len(phrase)
    bottombar = "-" * len(phrase)
    output = dedent(
        """
      %s
    < %s >
      %s
       \   ^__^
        \  (oo)\_______
           (__)\       )\/\\
               ||----w |
               ||     ||
    """
        % (topbar, phrase, bottombar)
    )

    colors = list(rich.color.ANSI_COLOR_NAMES.keys())
    color = random.choice(colors)
    rich.print(f"[{color}]{output}")


if __name__ == "__main__":
    say()