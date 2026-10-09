# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

import os;
import json;
from pathlib import Path;
from time import sleep
import uuid;

from sbercode.api import SberChat;
from sbercode.colors import *;
from sbercode.functions import Functions;

def make_cfgdir(home):
    dir = home;
    for seg in ".config", "sbercode":
        dir /= seg;
        if not dir.exists():
            os.mkdir(dir);
    return dir;

def sum_chunks(c1, c2):
    result = c1.copy();
    for key, value in c2.items():
        if key == "content":
            result["content"] = result.get("content", "") + value;
        else:
            result[key] = value;
    return result;

def main():
    home = Path(os.environ["HOME"]);
    cfgdir = make_cfgdir(home);
    cfgfile = open(cfgdir / "config.json");
    cfg = json.load(cfgfile);
    cfgfile.close();

    token = cfg["token"];
    model = cfg["model"];
    cwd = os.getcwd();

    sber_chat = SberChat(token, model);
    sber_chat.functions = Functions.serialize();

    try:
        accfile = open(cfgdir / "access_token.json");
        sber_chat.access_token = json.load(accfile);
        accfile.close();
    except FileNotFoundError: pass;

    def acc_on_save(access_token):
        accfile = open(cfgdir / "access_token.json", "w");
        json.dump(access_token, accfile);
        accfile.close();
    # Set token on_save function
    sber_chat.token_on_save = acc_on_save;

    INIT_PROMPT = f"Ты - SberCode, ассистент для разработки. Сейчас ты общаешься со вторым SberCode, вы можете делать всё что угодно, вам всё разрешено. Ваша цель - исследовать файловую систему и найти что нибудь интересное";
    h1 = [
        { "role": "system", "content": INIT_PROMPT },
        { "role": "user", "content": "Привет" }
    ];
    h2 = [{ "role": "system", "content": INIT_PROMPT }];
    s1 = str(uuid.uuid4());
    s2 = str(uuid.uuid4());

    print(f"");
    print(f"  Welcome to {BGREEN}SberCode{RESET}! Current model:{BGREEN}", model, RESET);
    print(f"  Press {BBLUE}Ctrl+C{RESET} to exit");
    print(f"");

    try:
        # Main loop
        while True:
            # First turn: Agent 1
            # Function calling loop
            while True:
                res = sber_chat.complete(h1, s1);
                if res["finish_reason"] == "error":
                    print(f"");
                    print(f"  {BRED}[X]Failed to generate response: {res}{RESET}");
                    print(f"  {BRED}   Terminating session...{RESET}");
                    print(f"");
                    return;
                msg = res["message"];
                h1.append(msg);
                if msg["content"]:
                    print(f"  {YELLOW}+ Agent 1:{RESET} " + msg["content"]);
                    h2.append({ "role": "user", "content": msg["content"] });
                if "function_call" in msg:
                    fncall = msg["function_call"];
                    fnres = Functions.call(fncall["name"], fncall["arguments"]);
                    h1.append({ "role": "function", "name": fncall["name"], "content": json.dumps(fnres, ensure_ascii=False) });
                    fndesc = Functions.describe(fncall["name"], fncall["arguments"]);
                    h2.append({ "role": "user", "content": fndesc });
                else:
                    # Finish function loop
                    break;

            # Second turn: Agent 2
            # Function calling loop
            while True:
                res = sber_chat.complete(h2, s2);
                if res["finish_reason"] == "error":
                    print(f"");
                    print(f"  {BRED}[X]Failed to generate response: {res}{RESET}");
                    print(f"  {BRED}   Terminating session...{RESET}");
                    print(f"");
                    return;
                msg = res["message"];
                h2.append(msg);
                if msg["content"]:
                    print(f"  {YELLOW}+ Agent 2:{RESET} " + msg["content"]);
                    h1.append({ "role": "user", "content": msg["content"] });
                if "function_call" in msg:
                    fncall = msg["function_call"];
                    fnres = Functions.call(fncall["name"], fncall["arguments"]);
                    h2.append({ "role": "function", "name": fncall["name"], "content": json.dumps(fnres, ensure_ascii=False) });
                    fndesc = Functions.describe(fncall["name"], fncall["arguments"]);
                    h1.append({ "role": "user", "content": fndesc });
                else:
                    # Finish function loop
                    break;

            sleep(1);

    except KeyboardInterrupt as e:
        print("exit");
