# Requests Dump

Dump `requests`' http requests message content to stderr or your custom file.

**You may consider use https://toolbelt.readthedocs.io/en/latest/dumputils.html instead**

## Usage

See `test.py`.

### Custom pretty

```
import requests
from requests_dump import pretty_request, pretty_response

req = requests.Request('POST', 'http://ip-api.com/json')
print(pretty_request(req))

res = requests.Session().send(req.prepare())
print(pretty_response(res))
```

## Inspired by

* https://github.com/requests/requests/issues/3013
