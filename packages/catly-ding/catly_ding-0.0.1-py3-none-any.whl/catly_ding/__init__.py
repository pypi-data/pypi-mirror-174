import json
import requests
from typing import Union, Dict, Text, List



def ding(
    webhook: Text,
    content: Union[Text, Dict, List],
    title: Text = None,
    atMobiles: Union[Text, List] = None,
    atAll: bool = False
) -> None:
    atMobiles = [] if atAll else [atMobiles] if atMobiles and not isinstance(atMobiles, list) else atMobiles
    content = f"{title}\n\n{content}" if title else content

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
            "msgtype": "text",
            "text": {
                "content": content},
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": atAll}}

    requests.post(webhook, headers=headers, data=json.dumps(data))