# Prioridades Clickup 

<br>

sacar las prioridades de una(varias) vista(s) de clickup y conectarlo a una webhook.

<br>

## Prerequisitos

   [Python 3.9](https://www.python.org/downloads/release/python-390/) +


## Ejemplo de uso

en este caso usando variables de entorno 
```
from clickup_priorities import priorities
from decouple import config


view_urls = [config("view1"), config("view2"), config("view3"), config("view4")]
query_list =  [{"page": "1"},{"page": "2"},{"page": "3"}]
headers = {"Authorization": config("Authorization") }
post_url = config("hook")

priorities(view_urls, query_list, headers, post_url)

```
## Output Terminal
```
RESULTS:

URGENT

 Count: 4
 Total time: 8.0h

HIGH

 Count: 26
 Total time: 8.5h

NORMAL

 Count: 43
 Total time: 26.2h

LOW

 Count: 29
 Total time: 43.0h

status code: <200>
errors: <None>

besos en ese jopo <3
```

<br>