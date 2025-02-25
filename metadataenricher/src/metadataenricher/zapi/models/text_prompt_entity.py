import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TextPromptEntity")


@_attrs_define
class TextPromptEntity:
    """
    Attributes:
        prompt (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        responses (Union[Unset, list[str]]):
    """

    prompt: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    responses: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        responses: Union[Unset, list[str]] = UNSET
        if not isinstance(self.responses, Unset):
            responses = self.responses

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if modified is not UNSET:
            field_dict["modified"] = modified
        if responses is not UNSET:
            field_dict["responses"] = responses

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        responses = cast(list[str], d.pop("responses", UNSET))

        text_prompt_entity = cls(
            prompt=prompt,
            modified=modified,
            responses=responses,
        )

        text_prompt_entity.additional_properties = d
        return text_prompt_entity

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
