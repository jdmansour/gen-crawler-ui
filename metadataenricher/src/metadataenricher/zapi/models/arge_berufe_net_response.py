from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArgeBerufeNetResponse")


@_attrs_define
class ArgeBerufeNetResponse:
    """
    Attributes:
        id (Union[Unset, str]):
        url (Union[Unset, str]):
        description_short (Union[Unset, str]):
        profession_group (Union[Unset, str]):
        profession_type (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    description_short: Union[Unset, str] = UNSET
    profession_group: Union[Unset, str] = UNSET
    profession_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        url = self.url

        description_short = self.description_short

        profession_group = self.profession_group

        profession_type = self.profession_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if url is not UNSET:
            field_dict["url"] = url
        if description_short is not UNSET:
            field_dict["description_short"] = description_short
        if profession_group is not UNSET:
            field_dict["profession_group"] = profession_group
        if profession_type is not UNSET:
            field_dict["profession_type"] = profession_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        url = d.pop("url", UNSET)

        description_short = d.pop("description_short", UNSET)

        profession_group = d.pop("profession_group", UNSET)

        profession_type = d.pop("profession_type", UNSET)

        arge_berufe_net_response = cls(
            id=id,
            url=url,
            description_short=description_short,
            profession_group=profession_group,
            profession_type=profession_type,
        )

        arge_berufe_net_response.additional_properties = d
        return arge_berufe_net_response

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
