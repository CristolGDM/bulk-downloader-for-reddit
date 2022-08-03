#!/usr/bin/env python3

import logging
import re
from typing import Optional, Callable

import bs4
from praw.models import Submission

from bdfr.exceptions import SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class DeviantArt(BaseDownloader):
    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        link = self._get_link(self.post.url)

        if not link:
            raise SiteDownloaderError('DeviantArt parser could not find any link')

        if not re.match(r'https?://.*', link):
            link = 'https://' + link
        return [Resource(self.post, link, self.deviantart_download(link))]

    @staticmethod
    def _get_link(url: str) -> str:
        page = DeviantArt.retrieve_url(url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        title = soup.find('h1', attrs={'data-hook': 'deviation_title'})
        if not title:
            return

        image = soup.find('img', attrs={'alt': title.string})
        if not image:
            return

        return image.get("src")

    @staticmethod
    def deviantart_download(url: str) -> Callable:
        download_parameters = {
            'headers': {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/88.0.4324.104 Safari/537.36',
                'Referer': 'https://www.deviantart.com/',
            },
        }
        logger.info("----------------------")
        logger.info(url)
        logger.info("----------------------")
        return lambda global_params: Resource.http_download(url, global_params | download_parameters)
