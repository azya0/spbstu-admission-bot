from collections.abc import AsyncGenerator

from aiohttp import ClientResponse, ClientSession
from futile_di_azya0 import Depends

CSRF_TOKEN: str = "7Hc3rwyOA395HxZIdERcjnSwUbRGxjOz"

COOKIES: dict[str, str] = {
    "csrftoken": CSRF_TOKEN,
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
    "Content-Type": "application/json",
    "Origin": "https://my.spbstu.ru",
    "X-CSRFToken": CSRF_TOKEN,
}


async def get_session() -> AsyncGenerator[ClientSession]:
    async with ClientSession(cookies=COOKIES, headers=HEADERS) as session:
        yield session


async def get(url: str, session: ClientSession = Depends(get_session)) -> AsyncGenerator[ClientResponse]:
    async with session.get(url) as response:
        yield response
