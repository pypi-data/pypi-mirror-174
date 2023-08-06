from .module import NuzlockeModule


def initialize(event_pool, rules):
    return NuzlockeModule(event_pool, rules)
