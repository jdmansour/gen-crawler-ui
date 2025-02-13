from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary import Binary


T = TypeVar("T", bound="ProfessionProfileInfo")


@_attrs_define
class ProfessionProfileInfo:
    """
    Attributes:
        thumbnail (Union[Unset, Binary]):
        read_time (Union[Unset, int]):
        url (Union[Unset, str]):
        description_short (Union[Unset, str]):
        profession_group (Union[Unset, str]):
        profession_type (Union[Unset, str]):
    """

    thumbnail: Union[Unset, "Binary"] = UNSET
    read_time: Union[Unset, int] = UNSET
    url: Union[Unset, str] = UNSET
    description_short: Union[Unset, str] = UNSET
    profession_group: Union[Unset, str] = UNSET
    profession_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thumbnail: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.thumbnail, Unset):
            thumbnail = self.thumbnail.to_dict()

        read_time = self.read_time

        url = self.url

        description_short = self.description_short

        profession_group = self.profession_group

        profession_type = self.profession_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if read_time is not UNSET:
            field_dict["readTime"] = read_time
        if url is not UNSET:
            field_dict["url"] = url
        if description_short is not UNSET:
            field_dict["descriptionShort"] = description_short
        if profession_group is not UNSET:
            field_dict["professionGroup"] = profession_group
        if profession_type is not UNSET:
            field_dict["professionType"] = profession_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.binary import Binary

        d = src_dict.copy()
        _thumbnail = d.pop("thumbnail", UNSET)
        thumbnail: Union[Unset, Binary]
        if isinstance(_thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = Binary.from_dict(_thumbnail)

        read_time = d.pop("readTime", UNSET)

        url = d.pop("url", UNSET)

        description_short = d.pop("descriptionShort", UNSET)

        profession_group = d.pop("professionGroup", UNSET)

        profession_type = d.pop("professionType", UNSET)

        profession_profile_info = cls(
            thumbnail=thumbnail,
            read_time=read_time,
            url=url,
            description_short=description_short,
            profession_group=profession_group,
            profession_type=profession_type,
        )

        profession_profile_info.additional_properties = d
        return profession_profile_info

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
