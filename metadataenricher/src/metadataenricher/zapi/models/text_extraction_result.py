from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TextExtractionResult")


@_attrs_define
class TextExtractionResult:
    """
    Attributes:
        text (str):
        lang (str):
        version (Union[Unset, str]):  Default: '0.2.0'.
    """

    text: str
    lang: str
    version: Union[Unset, str] = "0.2.0"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        lang = self.lang

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "lang": lang,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text")

        lang = d.pop("lang")

        version = d.pop("version", UNSET)

        text_extraction_result = cls(
            text=text,
            lang=lang,
            version=version,
        )

        text_extraction_result.additional_properties = d
        return text_extraction_result

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
