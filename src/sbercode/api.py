import httpx;
import json;
import uuid;
from dataclasses import dataclass, field;
from time import time;
import ssl;

from sbercode.cert import RUSSIAN_TRUSTED_ROOT_CA;

AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth";
BASE_URL = "https://api.giga.chat/v1/chat/completions";

def make_client():
    ssl_ctx = ssl.create_default_context(cadata=RUSSIAN_TRUSTED_ROOT_CA);
    timeout = httpx.Timeout(10);
    return httpx.Client(http2=True, verify=ssl_ctx, timeout=timeout);

@dataclass
class SberChat:
    token: str;
    model: str = "GigaChat-3-Lightning";
    scope: str = "GIGACHAT_API_PERS";
    access_token: str = None;
    session_id: str = str(uuid.uuid4());
    http: httpx.Client = make_client();
    functions: list[dict] = field(default_factory=list);

    def get_token(self):
        if self.access_token == None or time()*1000 > self.access_token["expires_at"]:
            headers = {
                "Authorization": f"Basic {self.token}",
                "RqUID": str(uuid.uuid4()),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            };
            data = "scope=" + self.scope;
            res = self.http.post(AUTH_URL, headers=headers, data=data);
            res.raise_for_status();
            self.access_token = res.json();
        return self.access_token["access_token"];

    def build_headers(self):
        return {
            "Authorization": f"Bearer {self.get_token()}",
            "RqUID": str(uuid.uuid4()),
            "X-Session-Id": self.session_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        };

    def build_request(self, history, stream=False):
        return {
            "model": self.model,
            "messages": history,
            "function_call": "auto",
            "functions": self.functions,
            "stream": stream,
        };

    def complete(self, history):
        headers = self.build_headers();
        data = self.build_request(history);
        res = self.http.post(BASE_URL, headers=headers, json=data);
        if res.status_code != 200:
            raise SberChatError(res.json()["message"]);
        return res.json()["choices"][0];

    def complete_stream(self, history):
        headers = self.build_headers();
        data = self.build_request(history, stream=True);
        with self.http.stream("POST", BASE_URL, headers=headers, json=data) as res:
            if res.status_code != 200:
                res = json.load(res);
                raise SberChatError(res["message"]);
            for chunk in sse_iter(res):
                yield chunk["choices"][0];

def sse_iter(res):
    event = "";
    for line in res.iter_lines():
        if line == "data: [DONE]": return;
        if line == "":
            yield json.loads(event);
            event = "";
        event += line.removeprefix("data:");

class SberChatError(Exception): pass;
