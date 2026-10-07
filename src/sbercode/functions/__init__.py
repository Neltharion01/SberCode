# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

from sbercode.colors import *;

from sbercode.functions.run_command import RunCommand;
from sbercode.functions.read_file import ReadFile;
from sbercode.functions.write_file import WriteFile;
from sbercode.functions.edit_file import EditFile;
from sbercode.functions.web_fetch import WebFetch;
from sbercode.functions.list_files import ListFiles;
from sbercode.functions.create_dir import CreateDir;
from sbercode.functions.remove_file import RemoveFile;
from sbercode.functions.remove_dir import RemoveDir;

class FunctionNotFound:
    def __init__(self, name):
        self.name = name;
    def run(self, args):
        return { "error": f"function {self.name} not found" };
    def print_args(self, args):
        print(f"  {BRED}[X] Function {self.name} not found{RESET}");

class Functions:
    functions = {
        "run_command": RunCommand(),
        "read_file": ReadFile(),
        "write_file": WriteFile(),
        "edit_file": EditFile(),
        "web_fetch": WebFetch(),
        "list_files": ListFiles(),
        "create_dir": CreateDir(),
        "remove_file": RemoveFile(),
        "remove_dir": RemoveDir(),
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
            print(f"  {BRED}[X] {text}{RESET}");
            ret = { "error": text };
        return ret;
