import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.profession_profile_info import ProfessionProfileInfo


T = TypeVar("T", bound="ProfessionProfileEntity")


@_attrs_define
class ProfessionProfileEntity:
    """
    Attributes:
        prompt (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        profiles (Union[Unset, list['ProfessionProfileInfo']]):
    """

    prompt: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    profiles: Union[Unset, list["ProfessionProfileInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        profiles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.profiles, Unset):
            profiles = []
            for profiles_item_data in self.profiles:
                profiles_item = profiles_item_data.to_dict()
                profiles.append(profiles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if modified is not UNSET:
            field_dict["modified"] = modified
        if profiles is not UNSET:
            field_dict["profiles"] = profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.profession_profile_info import ProfessionProfileInfo

        d = src_dict.copy()
        prompt = d.pop("prompt", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        profiles = []
        _profiles = d.pop("profiles", UNSET)
        for profiles_item_data in _profiles or []:
            profiles_item = ProfessionProfileInfo.from_dict(profiles_item_data)

            profiles.append(profiles_item)

        profession_profile_entity = cls(
            prompt=prompt,
            modified=modified,
            profiles=profiles,
        )

        profession_profile_entity.additional_properties = d
        return profession_profile_entity

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
