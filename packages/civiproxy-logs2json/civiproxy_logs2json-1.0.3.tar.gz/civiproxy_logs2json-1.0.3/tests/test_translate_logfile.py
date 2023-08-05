import os
import json
from civiproxy_logs2json import translate_logfile


def test_translate_logfile():
    with open(f"{os.path.dirname(__file__)}/assets/proxy_log.json") as json_file:
        json_ = json.load(json_file)
    with open(f"{os.path.dirname(__file__)}/assets/proxy.log", "r") as log_file:
        json_2 = translate_logfile(log_file)
        assert json_ == json_2
