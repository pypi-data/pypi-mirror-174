import os.path
from typing import Dict

import aiohttp_jinja2
from aiohttp import web

import jinja2


class Website:
    def __init__(self, rules: Dict[str, str]):
        self.rules = rules
        self.loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
        self.routes = [
            web.get('/nuzlocke/rules', lambda r: self.get_rules(r))
        ]

    @aiohttp_jinja2.template('rules.html')
    def get_rules(self, request: web.Request):
        return {'rules': self.rules}
