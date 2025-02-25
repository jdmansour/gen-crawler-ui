from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TopicStatisticsInputUpdate")


@_attrs_define
class TopicStatisticsInputUpdate:
    """
    Attributes:
        skip_if_exists (Union[Unset, bool]):  Default: True.
    """

    skip_if_exists: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        skip_if_exists = self.skip_if_exists

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if skip_if_exists is not UNSET:
            field_dict["skip_if_exists"] = skip_if_exists

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        skip_if_exists = d.pop("skip_if_exists", UNSET)

        topic_statistics_input_update = cls(
            skip_if_exists=skip_if_exists,
        )

        topic_statistics_input_update.additional_properties = d
        return topic_statistics_input_update

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
