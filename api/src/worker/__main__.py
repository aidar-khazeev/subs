import logging
import asyncio

from . import run


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
import httpx  # noqa
logging.getLogger('httpx').setLevel(logging.WARNING)

asyncio.run(run())