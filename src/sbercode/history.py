# SPDX-License-Identifier: 0BSD
# Copyright 2026 Neltharion01

import json;
import uuid;

class History:
    def get(self):
        return self._history;

    def get_session_id(self):
        return self._sid;

    def load():
        l = [];
        sid = None;
        f = open(".sc-history.jsonl", "a+");
        f.seek(0);
        for line in f:
            if not sid:
                sid = json.loads(line);
            else:
                l.append(json.loads(line));

        if not sid:
            sid = str(uuid.uuid4());
            f.write(json.dumps(sid) + "\n");

        h = History();
        h._history = l;
        h._file = f;
        h._sid = sid;
        return h;

    def append(self, msg):
        self._history.append(msg);
        self._file.write(json.dumps(msg, ensure_ascii=False) + "\n");

    def close(self):
        self._file.close();
