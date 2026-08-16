from aiohttp import ClientSession
from futile_di_azya0 import inject, Depends
from pydantic import TypeAdapter

from .exceptions import UnexpectedStatus
from .models import Candidate
from .client import get_session
from settings import Settings, get_settings


@inject
async def get_list_of_candidates(
    settings: Settings = get_settings(),
    session: ClientSession = Depends(get_session)
) -> list[Candidate]:
    async with session.get(settings.spbstu_settings.url) as response:
        if response.status != 200:
            raise UnexpectedStatus(response.status, await response.text())

        data = (await response.json())["results"]

    return TypeAdapter(list[Candidate]).validate_python(data)


async def get_list_of_candidates_for_admission() -> list[Candidate]:
    data = await get_list_of_candidates()

    test = [candidate for candidate in data if candidate.comment_status == "К зачислению"]

    return test
