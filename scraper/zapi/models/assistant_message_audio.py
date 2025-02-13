from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssistantMessageAudio")


@_attrs_define
class AssistantMessageAudio:
    """
    Attributes:
        id (Union[Unset, str]):
        transcript (Union[Unset, str]):
        data (Union[Unset, str]):
        expires_at (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    transcript: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    expires_at: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        transcript = self.transcript

        data = self.data

        expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if transcript is not UNSET:
            field_dict["transcript"] = transcript
        if data is not UNSET:
            field_dict["data"] = data
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        transcript = d.pop("transcript", UNSET)

        data = d.pop("data", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        assistant_message_audio = cls(
            id=id,
            transcript=transcript,
            data=data,
            expires_at=expires_at,
        )

        assistant_message_audio.additional_properties = d
        return assistant_message_audio

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
