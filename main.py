__version__ = "0.0.3"
import argparse
import json
import logging
from enum import Enum

from scrapy.crawler import CrawlerProcess

from networking import DatabaseConnection
from overcraft.spiders.builds import BuildsSpider


class Actions(Enum):
    SCRAPE = "scrape"
    UPDATE = "update"


def main(args):
    if args.action == Actions.SCRAPE.value:
        logging.info("Creation of the requested file from the original Excel file")
        process = CrawlerProcess(
            settings={
                "FEEDS": {
                    "data.json": {"format": "json"},
                },
                "FEED_EXPORT_ENCODING": "utf-8",
            }
        )
        process.crawl(BuildsSpider)
        process.start()

    if args.action == Actions.UPDATE.value:
        with open("data.json", "r", encoding="utf8") as json_file:
            data = json.load(json_file)
        database_connection = DatabaseConnection()

        for build in data[:50]:
            database_connection.create_build(build)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action",
        "-a",
        type=str,
        choices=list(map(lambda c: c.value, Actions)),
        required=True,
        help="chose the action to be executed",
    )
    args = parser.parse_args()
    main(args)
