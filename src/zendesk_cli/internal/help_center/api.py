"""
Provides a client for the Help Center API.
"""

import json
import typing
import urllib.parse
import urllib.request
from dataclasses import dataclass

from .options import ListArticlesOptionsBuilder

# class HelpCenterAPI(typing.Protocol):
#     def list_articles(self, url: str) -> list[Article]: ...


# def get_articles(url: str, client: HelpCenterAPI) -> list[Article]:
#     return client.list_articles(url)


def urlopen_to_bytes(req: str | urllib.request.Request):
    """
    Read and return the response body as bytes for the HTTP or HTTPS request.
    """
    # pylint: disable=import-outside-toplevel
    from http.client import HTTPResponse

    # pylint: disable-next=line-too-long
    # For HTTP and HTTPS URLs, this function returns a http.client.HTTPResponse object slightly modified.
    response: HTTPResponse
    with urllib.request.urlopen(req) as response:
        return response.read()


class Meta(typing.TypedDict):
    has_more: bool
    after_cursor: str
    before_cursor: str


class Links(typing.TypedDict):
    next: str
    prev: str


class CursorPaginatedResponse(typing.TypedDict):
    meta: Meta
    links: Links


# class Article(typing.TypedDict):
#     author_id: int | None
#     body: str | None
#     comments_disabled: bool | None
#     content_tag_ids: list[typing.Any] | None
#     created_at: str | None
#     draft: bool | None
#     edited_at: str | None
#     html_url: str | None
#     id: int | None
#     label_names: list[typing.Any] | None
#     locale: str
#     outdated: bool | None
#     outdated_locales: list[typing.Any] | None
#     permission_group_id: int
#     position: int | None
#     promoted: bool | None
#     section_id: int | None
#     source_locale: str | None
#     title: str
#     updated_at: str | None
#     url: str | None
#     user_segment_id: int
#     vote_count: int | None
#     vote_sum: int | None


class ListArticlesResponse(CursorPaginatedResponse):
    articles: list[dict[str, typing.Any]]


@dataclass(frozen=True)
class HelpCenterClient:
    """
    Represents a client for the Help Center API.
    """

    base_url: str

    def get_articles(self, url: str | None = None):
        """
        Generator that yields articles from the Help Center API.
        """

        def first_url(page_size: int = 100) -> str:
            return (
                f"{ListArticlesOptionsBuilder().New(self.base_url).to_url()}?%s"
                % urllib.parse.urlencode({"page[size]": page_size})
            )

        url = url if url is not None else first_url()
        content = urlopen_to_bytes(
            urllib.request.Request(url, headers={"Accept": "application/json"})
        )
        data = ListArticlesResponse(json.loads(content))
        yield from data["articles"]
        if Meta(data["meta"])["has_more"] is True:
            yield from self.get_articles(Links(data["links"])["next"])
