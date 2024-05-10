"""
Models for the Help Center API.
"""

# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    """
    Represents an article in a Help Center.
    """

    author_id: int | None
    body: str | None
    comments_disabled: bool | None
    content_tag_ids: list | None
    created_at: str | None
    draft: bool | None
    edited_at: str | None
    html_url: str | None
    id: int | None
    label_names: list | None
    locale: str
    outdated: bool | None
    outdated_locales: list | None
    permission_group_id: int
    position: int | None
    promoted: bool | None
    section_id: int | None
    source_locale: str | None
    title: str
    updated_at: str | None
    url: str | None
    user_segment_id: int
    vote_count: int | None
    vote_sum: int | None

    @staticmethod
    def get_field_names():
        """
        Returns the field names for the Article dataclass.
        """
        # return Article.__annotations__.keys()
        # pylint: disable=no-member
        return Article.__dataclass_fields__.keys()
