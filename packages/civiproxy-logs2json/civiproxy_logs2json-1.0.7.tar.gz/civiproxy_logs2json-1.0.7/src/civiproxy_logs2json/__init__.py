from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "1.0.7"

_cfg = tomllib.loads(resources.read_text("civiproxy_logs2json", "config.toml"))
REQUEST_LINE_RE = _cfg["regex"]["request_line"]
VALUES_LINE_RE = _cfg["regex"]["values_line"]
CLOSING_LINE_RE = _cfg["regex"]["closing_line"]
