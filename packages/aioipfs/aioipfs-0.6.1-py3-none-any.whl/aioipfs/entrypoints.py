import argparse
import asyncio

from aioipfs import config


async def run(args):
    print(args)
    if args.cmd == 'node':


def aioipfs_run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        nargs='+',
        dest='cmd'
    )

    asyncio.run(run(parser.parse_args()))
