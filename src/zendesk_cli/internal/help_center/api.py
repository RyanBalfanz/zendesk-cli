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
    from http.client import HTTPResponse

    # For HTTP and HTTPS URLs, this function returns a http.client.HTTPResponse object slightly modified.
    response: HTTPResponse
    with urllib.request.urlopen(req) as response:
        return response.read()


@dataclass(frozen=True)
class HelpCenterClient:
    base_url: str

    def get_articles(self, url: str | None = None):
        def first_url(page_size: int = 100) -> str:
            return (
                f"{ListArticlesOptionsBuilder().New(self.base_url).to_url()}?%s"
                % urllib.parse.urlencode({"page[size]": page_size})
            )

        url = url if url is not None else first_url()
        content = urlopen_to_bytes(
            urllib.request.Request(url, headers={"Accept": "application/json"})
        )
        data: dict[str, typing.Any] = json.loads(content)
        data_articles: list[dict[str, typing.Any]] = data["articles"]
        for a in data_articles:
            yield a
        if data["meta"]["has_more"] is True:
            yield from self.get_articles(data["links"]["next"])
