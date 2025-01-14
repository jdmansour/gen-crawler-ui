from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sortnull import Sortnull


T = TypeVar("T", bound="Pageablenull")


@_attrs_define
class Pageablenull:
    """
    Attributes:
        paged (Union[Unset, bool]):
        page_number (Union[Unset, int]):
        page_size (Union[Unset, int]):
        unpaged (Union[Unset, bool]):
        offset (Union[Unset, int]):
        sort (Union[Unset, Sortnull]):
    """

    paged: Union[Unset, bool] = UNSET
    page_number: Union[Unset, int] = UNSET
    page_size: Union[Unset, int] = UNSET
    unpaged: Union[Unset, bool] = UNSET
    offset: Union[Unset, int] = UNSET
    sort: Union[Unset, "Sortnull"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        paged = self.paged

        page_number = self.page_number

        page_size = self.page_size

        unpaged = self.unpaged

        offset = self.offset

        sort: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if paged is not UNSET:
            field_dict["paged"] = paged
        if page_number is not UNSET:
            field_dict["pageNumber"] = page_number
        if page_size is not UNSET:
            field_dict["pageSize"] = page_size
        if unpaged is not UNSET:
            field_dict["unpaged"] = unpaged
        if offset is not UNSET:
            field_dict["offset"] = offset
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.sortnull import Sortnull

        d = src_dict.copy()
        paged = d.pop("paged", UNSET)

        page_number = d.pop("pageNumber", UNSET)

        page_size = d.pop("pageSize", UNSET)

        unpaged = d.pop("unpaged", UNSET)

        offset = d.pop("offset", UNSET)

        _sort = d.pop("sort", UNSET)
        sort: Union[Unset, Sortnull]
        if isinstance(_sort, Unset):
            sort = UNSET
        else:
            sort = Sortnull.from_dict(_sort)

        pageablenull = cls(
            paged=paged,
            page_number=page_number,
            page_size=page_size,
            unpaged=unpaged,
            offset=offset,
            sort=sort,
        )

        pageablenull.additional_properties = d
        return pageablenull

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
