from aiohttp import ClientSession
from async_lru import alru_cache
from futile_di_azya0 import Depends, inject
from pydantic import TypeAdapter

from settings import Settings, get_settings

from .client import get_session
from .exceptions import UnexpectedStatus
from .models import Candidate, StudyProgram


@alru_cache(maxsize=1)
@inject
async def get_list_of_programs(
    session: ClientSession = Depends(get_session),
    settings: Settings = get_settings()
) -> list[StudyProgram]:
    async with session.post(
        settings.spbstu_settings.codes_list_url,
        json={
            "education_level": "master_pre_competition_lists",
            "id_1": "2",
            "id_2": "1",
        },
        allow_redirects=False
    ) as response:
        if response.status != 200:
            raise UnexpectedStatus(response.status, await response.text())

        data = (await response.json())["code_list"]

    return TypeAdapter(list[StudyProgram]).validate_python(data)


@inject
async def get_list_of_candidates(
    program_code: int,
    session: ClientSession = Depends(get_session),
    settings: Settings = get_settings()
) -> list[Candidate]:
    async with session.get(settings.spbstu_settings.program_candidates_list_url, params={
        "filter_1": "2",
        "filter_2": "1",
        "filter_3": program_code,
        "education_level": "master_pre_competition_lists"
    }) as response:
        if response.status != 200:
            raise UnexpectedStatus(response.status, await response.text())

        data = (await response.json())["results"]

    return TypeAdapter(list[Candidate]).validate_python(data)


async def get_list_of_candidates_for_admission(spbstu_program: int) -> list[Candidate]:
    data = await get_list_of_candidates(spbstu_program)

    test = [candidate for candidate in data if candidate.comment_status == "К зачислению"]

    return test


async def get_place_by_user_id(user_code: int, spbstu_program: int) -> int:
    data = await get_list_of_candidates_for_admission(spbstu_program)

    for index, candidate in enumerate(data):
        if int(candidate.code) == user_code:
            return index + 1

    return -1
