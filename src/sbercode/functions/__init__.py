# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

from sbercode.colors import *;

from sbercode.functions.run_command import RunCommand;

class FunctionNotFound:
    def __init__(self, name):
        self.name = name;
    def run(self, args):
        return { "error": f"function {self.name} not found" };
    def print_args(self, args):
        print(f"  {BRED}+ Function {self.name} not found{RESET}");

class Functions:
    functions = {
        "run_command": RunCommand()
    };

    def serialize():
        return list(f.desc for f in Functions.functions.values());

    def call(name, args):
        f = Functions.functions.get(name, FunctionNotFound(name));
        f.print_args(args);
        try:
            ret = f.run(args);
        except Exception as e:
            e_name = type(e).__name__;
            text = f"{e_name}: {e}";
            print(text);
            ret = { "error": text };
        return ret;
