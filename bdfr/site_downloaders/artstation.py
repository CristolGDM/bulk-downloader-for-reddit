#!/usr/bin/env python3
# coding=utf-8

import logging
import re
from abc import ABC, abstractmethod
from typing import Optional, Callable

import requests
from praw.models import Submission

from bdfr.exceptions import ResourceNotFound, SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class Artstation(BaseDownloader):
    def __init__(self, post: Submission, typical_extension: Optional[str] = None):
        self.post = post
        self.typical_extension = typical_extension

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        url = self.post.url
        url = re.sub('.*\.artstation\.com', "https://cdn.artstation.com", url)
        return [Resource(self.post, url, self.artstation_download(url))]

    @staticmethod
    def artstation_download(url: str) -> Callable:
        download_parameters = {
            'headers': {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/88.0.4324.104 Safari/537.36',
                'Referer': 'https://www.artstation.com/',
            },
        }
        return lambda global_params: Resource.http_download(url, global_params | download_parameters)