from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatMessage")


@_attrs_define
class ChatMessage:
    """
    Attributes:
        text_content (Union[Unset, str]):
        name (Union[Unset, str]):
        role (Union[Unset, str]):
    """

    text_content: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text_content = self.text_content

        name = self.name

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text_content is not UNSET:
            field_dict["textContent"] = text_content
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text_content = d.pop("textContent", UNSET)

        name = d.pop("name", UNSET)

        role = d.pop("role", UNSET)

        chat_message = cls(
            text_content=text_content,
            name=name,
            role=role,
        )

        chat_message.additional_properties = d
        return chat_message

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
