# CiviProxy_Logs2Json

Translate a [CiviProxy](https://github.com/systopia/CiviProxy) logfile into JSON format.

## Installation
```bash
python3 -m pip install civiproxy_logs2json --user
```

## Example Usage

Pass logfile as positional argument:
```bash
cpl2j /var/www/proxy_logs/proxy.log
```

Pipe logfile into program:
```bash
cat proxy.log | cpl2j 
```

Set JSON indentation to two spaces:
```bash
cat proxy.log | cpl2j -s 2 
```

### Tip
Use [VisiData](https://github.com/saulpw/visidata) to explore the data in a very comfortable way:
/var/www/proxy_logs/proxy.log
```bash
cpl2j /var/www/proxy_logs/proxy.log | vd -f json
```