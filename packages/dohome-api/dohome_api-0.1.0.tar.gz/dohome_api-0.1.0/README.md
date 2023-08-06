# DoHome API [![Quality assurance](https://github.com/mishamyrt/dohome_api/actions/workflows/qa.yaml/badge.svg)](https://github.com/mishamyrt/dohome_api/actions/workflows/qa.yaml) [![PyPI version](https://badge.fury.io/py/dohome-api.svg)](https://pypi.org/project/dohome-api/)

Library for controlling smart bulbs that work using the DoIT protocol (DoHome app).

## Installation

```
pip install dohome-api
```

## Usage

### Find the light bulbs that are on

```py
from dohome_api import DoHomeGateway
from asyncio import run

async def main():
    gateway = DoHomeGateway()
    descriptions = await gateway.discover_lights()
    for description in descriptions:
        print(f"Found light: sid {descr['sid']}, ip {descr['sta_ip']}")

run(main())
```

### Change the color of the light bulb

```py
from dohome_api import DoHomeGateway
from asyncio import run

async def main():
    gateway = DoHomeGateway()
    light = await gateway.add_light("19eb") # last 4 symbols of mac address
    await light.set_rgb(255, 0, 0) # red

run(main())
```