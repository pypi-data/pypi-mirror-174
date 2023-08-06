from typing import List, Optional, Tuple, Dict

import aiohttp.web
import jinja2
from mahiru.core import Module, Event
from .website import Website


class NuzlockeModule(Module):
    def __init__(self, event_pool, rules: Dict[str, str]):
        super(NuzlockeModule, self).__init__(event_pool)
        self.website = Website(rules)

    def get_routes(self) -> Tuple[Optional["jinja2.BaseLoader"], List["aiohttp.web.RouteDef"]]:
        return self.website.loader, self.website.routes

    async def consume(self, event: Event):
        if event.name == 'raw_message':
            message: str = event.data['message']
            sender: str = event.data['user']
            if message == '!rules':
                await self.trigger_event(
                    'reply', {
                        'message': 'normal nuzlocke rules, '
                                   'no items, no overleveling. '
                                   'details at https://mahiru.henny022.eu.ngrok.io/nuzlocke/rules'
                    },
                    event.source.name, event.source.user
                )
