# 🚰 pyoutbreaksnearme: A Python3 API for Outbreaks Near Me

[![CI](https://github.com/bachya/pyoutbreaksnearme/workflows/CI/badge.svg)](https://github.com/bachya/pyoutbreaksnearme/actions)
[![PyPi](https://img.shields.io/pypi/v/pyoutbreaksnearme.svg)](https://pypi.python.org/pypi/pyoutbreaksnearme)
[![Version](https://img.shields.io/pypi/pyversions/pyoutbreaksnearme.svg)](https://pypi.python.org/pypi/pyoutbreaksnearme)
[![License](https://img.shields.io/pypi/l/pyoutbreaksnearme.svg)](https://github.com/bachya/pyoutbreaksnearme/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyoutbreaksnearme/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyoutbreaksnearme)
[![Maintainability](https://api.codeclimate.com/v1/badges/4707fac476249d515511/maintainability)](https://codeclimate.com/github/bachya/pyoutbreaksnearme/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`pyoutbreaksnearme` is a Python3, asyncio-based library for getting data from
[Outbreaks Near Me](https://outbreaksnearme.org).

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```bash
pip install pyoutbreaksnearme
```

# Python Versions

`pyoutbreaksnearme` is currently supported on:

- Python 3.9
- Python 3.10
- Python 3.11

# Usage

```python
import asyncio

from aiohttp import ClientSession

from pyoutbreaksnearme import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    client = await Client()

    # Get user-reported data for the location closest to a latitude/longitude:
    nearest_user_data = await client.user_data.async_get_nearest_by_coordinates(
        40.7152, -73.9877
    )

    # Get totals for user-reported data:
    user_totals_data = await client.user_data.async_get_totals()

    # Get CDC data for the location closest to a latitude/longitude:
    nearest_user_data = await client.cdc_data.async_get_nearest_by_coordinates(
        40.7152, -73.9877
    )


asyncio.run(main())
```

By default, the library creates a new connection to Outbreaks Near Me with each
coroutine. If you are calling a large number of coroutines (or merely want to squeeze
out every second of runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from pyoutbreaksnearme import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        # Create a Notion API client:
        client = await Client(session=session)

        # Get to work...


asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyoutbreaksnearme/issues)
   or [initiate a discussion on one](https://github.com/bachya/pyoutbreaksnearme/issues/new).
2. [Fork the repository](https://github.com/bachya/pyoutbreaksnearme/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov pyoutbreaksnearme tests`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
