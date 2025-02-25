from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Sortnull")


@_attrs_define
class Sortnull:
    """
    Attributes:
        sorted_ (Union[Unset, bool]):
        unsorted (Union[Unset, bool]):
        empty (Union[Unset, bool]):
    """

    sorted_: Union[Unset, bool] = UNSET
    unsorted: Union[Unset, bool] = UNSET
    empty: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sorted_ = self.sorted_

        unsorted = self.unsorted

        empty = self.empty

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sorted_ is not UNSET:
            field_dict["sorted"] = sorted_
        if unsorted is not UNSET:
            field_dict["unsorted"] = unsorted
        if empty is not UNSET:
            field_dict["empty"] = empty

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        sorted_ = d.pop("sorted", UNSET)

        unsorted = d.pop("unsorted", UNSET)

        empty = d.pop("empty", UNSET)

        sortnull = cls(
            sorted_=sorted_,
            unsorted=unsorted,
            empty=empty,
        )

        sortnull.additional_properties = d
        return sortnull

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
