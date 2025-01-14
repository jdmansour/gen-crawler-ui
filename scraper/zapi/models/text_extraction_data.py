from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.methods import Methods
from ..models.text_extraction_data_preference import TextExtractionDataPreference
from ..types import UNSET, Unset

T = TypeVar("T", bound="TextExtractionData")


@_attrs_define
class TextExtractionData:
    """
    Attributes:
        url (str):
        method (Union[Unset, Methods]):  Default: Methods.SIMPLE.
        browser_location (Union[None, Unset, str]):
        lang (Union[Unset, str]):  Default: 'auto'.
        preference (Union[Unset, TextExtractionDataPreference]):  Default: TextExtractionDataPreference.NONE.
    """

    url: str
    method: Union[Unset, Methods] = Methods.SIMPLE
    browser_location: Union[None, Unset, str] = UNSET
    lang: Union[Unset, str] = "auto"
    preference: Union[Unset, TextExtractionDataPreference] = TextExtractionDataPreference.NONE
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        method: Union[Unset, str] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        browser_location: Union[None, Unset, str]
        if isinstance(self.browser_location, Unset):
            browser_location = UNSET
        else:
            browser_location = self.browser_location

        lang = self.lang

        preference: Union[Unset, str] = UNSET
        if not isinstance(self.preference, Unset):
            preference = self.preference.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if browser_location is not UNSET:
            field_dict["browser_location"] = browser_location
        if lang is not UNSET:
            field_dict["lang"] = lang
        if preference is not UNSET:
            field_dict["preference"] = preference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        _method = d.pop("method", UNSET)
        method: Union[Unset, Methods]
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = Methods(_method)

        def _parse_browser_location(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        browser_location = _parse_browser_location(d.pop("browser_location", UNSET))

        lang = d.pop("lang", UNSET)

        _preference = d.pop("preference", UNSET)
        preference: Union[Unset, TextExtractionDataPreference]
        if isinstance(_preference, Unset):
            preference = UNSET
        else:
            preference = TextExtractionDataPreference(_preference)

        text_extraction_data = cls(
            url=url,
            method=method,
            browser_location=browser_location,
            lang=lang,
            preference=preference,
        )

        text_extraction_data.additional_properties = d
        return text_extraction_data

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
