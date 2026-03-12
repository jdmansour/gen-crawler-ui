
from typing import Any
from scrapy import Item, Spider
from scrapy.http import Response
from scrapy.logformatter import LogFormatter, LogFormatterResult
import rich.pretty
import rich.console


def format_dict(data):
    """ Formats a dict for logging, shortening long items. """
    console = rich.console.Console(color_system=None)
    with console.capture() as capture:
        rich.pretty.pprint(data, console=console, max_string=81, indent_guides=False)
    return capture.get()


def format_item(item: Item) -> str:
    """ Formats an Item for logging, shortening long items. """
    return format_dict(to_dict(item))


def to_dict(item: Item|list|dict) -> dict:
    # convert to dict, including nested items
    if isinstance(item, Item):
        return {k: to_dict(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [to_dict(i) for i in item]
    else:
        return item
    

class PrettyLogFormatter(LogFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def item_error(self, item: Any, exception: BaseException, response: Response | None, spider: Spider) -> LogFormatterResult:
        item = format_item(item)
        return super().item_error(item, exception, response, spider)