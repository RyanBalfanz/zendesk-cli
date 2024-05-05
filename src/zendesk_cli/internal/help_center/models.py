"""
Models for the Help Center API.
"""

# pylint: disable=too-many-instance-attributes
import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    """
    Represents an article in a Help Center.
    """

    id: int
    title: str
    url: str
    html_url: str
    author_id: int
    comments_disabled: bool
    draft: bool
    promoted: bool
    position: int
    vote_sum: int
    vote_count: int
    section_id: int
    created_at: str
    updated_at: str
    name: typing.Any
    source_locale: str
    locale: str
    outdated: bool
    outdated_locales: list
    edited_at: str
    user_segment_id: int
    permission_group_id: int
    content_tag_ids: list
    label_names: list
    body: str

    @staticmethod
    def get_field_names():
        """
        Returns the field names for the Article dataclass.
        """
        # return Article.__annotations__.keys()
        # pylint: disable=no-member
        return Article.__dataclass_fields__.keys()
