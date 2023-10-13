import asyncio
from pprint import pprint

from aioelectricitymaps import ElectricityMaps


async def main():
    async with ElectricityMaps(token="abc123") as em:
        pprint(await em.latest_carbon_intensity_by_country_code(code="DE"))


asyncio.run(main())
