"""
Represents the options for the list articles API.
"""

import typing
import urllib.parse
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
# pylint: disable=line-too-long
class ListArticlesOptions:
    """
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us").to_url()
    'https://support.zendesk.com/api/v2/help_center/articles/'
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us", locale="en-us").to_url()
    'https://support.zendesk.com/api/v2/help_center/en-us/articles/'
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us", category_id=1).to_url()
    'https://support.zendesk.com/api/v2/help_center/categories/1/articles/'
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us", category_id=1, locale="en-us").to_url()
    'https://support.zendesk.com/api/v2/help_center/en-us/categories/1/articles/'
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us", section_id=1).to_url()
    'https://support.zendesk.com/api/v2/help_center/sections/1/articles/'
    >>> ListArticlesOptions("https://support.zendesk.com/hc/en-us", section_id=1, locale="en-us").to_url()
    'https://support.zendesk.com/api/v2/help_center/en-us/sections/1/articles/'
    """

    # pylint: enable=line-too-long

    base_url: str
    locale: str | None = None
    category_id: int | None = None
    section_id: int | None = None
    # user_id: int | None = None
    # start_time: str | None = None

    def to_url(self):
        """
        Returns the URL for the list articles API.
        """
        if self.category_id is not None:
            if self.locale is None:
                s = f"/api/v2/help_center/categories/{self.category_id}/articles/"
            else:
                s = f"/api/v2/help_center/{self.locale}/categories/{self.category_id}/articles/"
            return urllib.parse.urljoin(self.base_url, s)
        if self.section_id is not None:
            if self.locale is None:
                s = f"/api/v2/help_center/sections/{self.section_id}/articles/"
            else:
                s = f"/api/v2/help_center/{self.locale}/sections/{self.section_id}/articles/"
            return urllib.parse.urljoin(self.base_url, s)
        if self.locale is None:
            s = "/api/v2/help_center/articles/"
        else:
            s = f"/api/v2/help_center/{self.locale}/articles/"
        return urllib.parse.urljoin(self.base_url, s)

    # pylint: disable=invalid-name
    @staticmethod
    def WithLocale(locale: str):
        # pylint: disable=missing-function-docstring
        def with_locale(opts: ListArticlesOptions):
            return ListArticlesOptions(**(asdict(opts) | {"locale": locale}))

        return with_locale

    @staticmethod
    def WithCategoryId(category_id: int):
        # pylint: disable=missing-function-docstring
        def with_category_id(opts: ListArticlesOptions):
            return ListArticlesOptions(**(asdict(opts) | {"category_id": category_id}))

        return with_category_id

    @staticmethod
    def WithSectionId(section_id: int):
        # pylint: disable=missing-function-docstring
        def with_section_id(opts: ListArticlesOptions):
            return ListArticlesOptions(**(asdict(opts) | {"section_id": section_id}))

        return with_section_id

    # pylint: enable=invalid-name


# pylint: disable=too-few-public-methods
class OptionsBuilder[T](typing.Protocol):
    """
    Represents a builder for options.
    """

    @staticmethod
    # pylint: disable=missing-function-docstring
    # pylint: disable=invalid-name
    # pylint: disable=undefined-variable
    def New(base_url: str, *opts: typing.Callable[[T], T]) -> T: ...


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class ListArticlesOptionsBuilder(OptionsBuilder[ListArticlesOptions]):
    """
    # pylint: disable=line-too-long
    >>> ListArticlesOptionsBuilder.New("https://support.zendesk.com").to_url()
    'https://support.zendesk.com/api/v2/help_center/articles/'
    >>> ListArticlesOptionsBuilder.New("https://support.zendesk.com/hc/en-us").to_url()
    'https://support.zendesk.com/api/v2/help_center/articles/'
    >>> ListArticlesOptionsBuilder.New("https://support.zendesk.com/hc/en-us", ListArticlesOptions.WithLocale("en-us")).to_url()
    'https://support.zendesk.com/api/v2/help_center/en-us/articles/'
    >>> ListArticlesOptionsBuilder.New("https://support.zendesk.com/hc/en-us", ListArticlesOptions.WithCategoryId(1)).to_url()
    'https://support.zendesk.com/api/v2/help_center/categories/1/articles/'
    >>> ListArticlesOptionsBuilder.New("https://support.zendesk.com/hc/en-us", ListArticlesOptions.WithSectionId(1)).to_url()
    'https://support.zendesk.com/api/v2/help_center/sections/1/articles/'
    """

    # pylint: enable=line-too-long

    @staticmethod
    def New(
        base_url: str,
        *opts: typing.Callable[[ListArticlesOptions], ListArticlesOptions],
    ):
        options = ListArticlesOptions(base_url)
        for opt in opts:
            options = opt(options)
        return options


# pylint: enable=too-few-public-methods
