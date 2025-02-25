import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.binary import Binary


T = TypeVar("T", bound="ImagePromptEntity")


@_attrs_define
class ImagePromptEntity:
    """
    Attributes:
        prompt (Union[Unset, str]):
        modified (Union[Unset, datetime.datetime]):
        image (Union[Unset, Binary]):
    """

    prompt: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    image: Union[Unset, "Binary"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        image: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if modified is not UNSET:
            field_dict["modified"] = modified
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.binary import Binary

        d = src_dict.copy()
        prompt = d.pop("prompt", UNSET)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        _image = d.pop("image", UNSET)
        image: Union[Unset, Binary]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = Binary.from_dict(_image)

        image_prompt_entity = cls(
            prompt=prompt,
            modified=modified,
            image=image,
        )

        image_prompt_entity.additional_properties = d
        return image_prompt_entity

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
