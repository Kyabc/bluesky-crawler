import asyncio
from datetime import date, datetime

from atproto.firehose import AsyncFirehoseSubscribeReposClient, parse_subscribe_repos_message
from loguru import logger
from settings import settings
from utils.bluesky import get_commit_as_dict, get_date_by_commit
from utils.file_manager import JsonLinesFile

today = datetime.now()
logger.add(today.strftime("logs/%Y-%m-%d.log"), rotation=settings.logger_rotation)


def data_file_path(date: date) -> str:
    return f"{settings.data_dir}/{date}.bsky"


async def main():
    client = AsyncFirehoseSubscribeReposClient()
    file = JsonLinesFile(file_path=data_file_path(today.date()))

    async def on_message_handler(message):
        try:
            commit = parse_subscribe_repos_message(message)
            commit_dict = get_commit_as_dict(commit)
            created_at = get_date_by_commit(commit)
            file_path = data_file_path(created_at)
            if file.file_path != file_path:
                file.reopen(file_path)
            file.add_json(commit_dict)
        except Exception as e:
            logger.error(f"Exception raised ({e})")

    await client.start(on_message_handler)


if __name__ == '__main__':
    logger.info(f"Start crawling at {today}")
    asyncio.get_event_loop().run_until_complete(main())
