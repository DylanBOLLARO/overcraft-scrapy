__version__ = "0.0.1"

import argparse
import logging
from enum import Enum
from scrapy.crawler import CrawlerProcess

from overcraft.spiders.builds import BuildsSpider

class Actions(Enum):
    SCRAPE = "scrape"


def main(args):
    if args.action == Actions.SCRAPE.value:
        logging.info("Creation of the requested file from the original Excel file")
        process = CrawlerProcess(settings={
            "FEEDS": {
                "data.json": {"format": "json"},
            },
            'FEED_EXPORT_ENCODING': 'utf-8',
            'LOG_LEVEL' : 'WARNING'
        })
        process.crawl(BuildsSpider)
        process.start()



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
