from typing import AsyncGenerator

from aiohttp import ClientSession, ClientResponse
from futile_di_azya0 import Depends


COOKIES: dict[str, str] = {
    "csrftoken": "ТВОЙ_CSRF",
    "sessionid": "ТВОЙ_SESSIONID",
    "cookie_name": "cookie_value",
}

HEADERS: dict[str, str | dict[str]] = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:153.0) "
        "Gecko/20100101 Firefox/153.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def get_session() -> AsyncGenerator[ClientSession]:
    async with ClientSession(cookies=COOKIES, headers=HEADERS) as session:
        yield session


async def get(url: str, session: ClientSession = Depends(get_session)) -> AsyncGenerator[ClientResponse]:
    async with session.get(url) as response:
        yield response
