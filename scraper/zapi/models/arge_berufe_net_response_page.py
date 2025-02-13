from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arge_berufe_net_response import ArgeBerufeNetResponse
    from ..models.pageablenull import Pageablenull
    from ..models.sortnull import Sortnull


T = TypeVar("T", bound="ArgeBerufeNetResponsePage")


@_attrs_define
class ArgeBerufeNetResponsePage:
    """
    Attributes:
        content (Union[Unset, list['ArgeBerufeNetResponse']]):
        pageable (Union[Unset, Pageablenull]):
        last (Union[Unset, bool]):
        total_elements (Union[Unset, int]):
        total_pages (Union[Unset, int]):
        first (Union[Unset, bool]):
        size (Union[Unset, int]):
        number (Union[Unset, int]):
        sort (Union[Unset, Sortnull]):
        number_of_elements (Union[Unset, int]):
        empty (Union[Unset, bool]):
    """

    content: Union[Unset, list["ArgeBerufeNetResponse"]] = UNSET
    pageable: Union[Unset, "Pageablenull"] = UNSET
    last: Union[Unset, bool] = UNSET
    total_elements: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    first: Union[Unset, bool] = UNSET
    size: Union[Unset, int] = UNSET
    number: Union[Unset, int] = UNSET
    sort: Union[Unset, "Sortnull"] = UNSET
    number_of_elements: Union[Unset, int] = UNSET
    empty: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()
                content.append(content_item)

        pageable: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pageable, Unset):
            pageable = self.pageable.to_dict()

        last = self.last

        total_elements = self.total_elements

        total_pages = self.total_pages

        first = self.first

        size = self.size

        number = self.number

        sort: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = self.sort.to_dict()

        number_of_elements = self.number_of_elements

        empty = self.empty

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if pageable is not UNSET:
            field_dict["pageable"] = pageable
        if last is not UNSET:
            field_dict["last"] = last
        if total_elements is not UNSET:
            field_dict["totalElements"] = total_elements
        if total_pages is not UNSET:
            field_dict["totalPages"] = total_pages
        if first is not UNSET:
            field_dict["first"] = first
        if size is not UNSET:
            field_dict["size"] = size
        if number is not UNSET:
            field_dict["number"] = number
        if sort is not UNSET:
            field_dict["sort"] = sort
        if number_of_elements is not UNSET:
            field_dict["numberOfElements"] = number_of_elements
        if empty is not UNSET:
            field_dict["empty"] = empty

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.arge_berufe_net_response import ArgeBerufeNetResponse
        from ..models.pageablenull import Pageablenull
        from ..models.sortnull import Sortnull

        d = src_dict.copy()
        content = []
        _content = d.pop("content", UNSET)
        for content_item_data in _content or []:
            content_item = ArgeBerufeNetResponse.from_dict(content_item_data)

            content.append(content_item)

        _pageable = d.pop("pageable", UNSET)
        pageable: Union[Unset, Pageablenull]
        if isinstance(_pageable, Unset):
            pageable = UNSET
        else:
            pageable = Pageablenull.from_dict(_pageable)

        last = d.pop("last", UNSET)

        total_elements = d.pop("totalElements", UNSET)

        total_pages = d.pop("totalPages", UNSET)

        first = d.pop("first", UNSET)

        size = d.pop("size", UNSET)

        number = d.pop("number", UNSET)

        _sort = d.pop("sort", UNSET)
        sort: Union[Unset, Sortnull]
        if isinstance(_sort, Unset):
            sort = UNSET
        else:
            sort = Sortnull.from_dict(_sort)

        number_of_elements = d.pop("numberOfElements", UNSET)

        empty = d.pop("empty", UNSET)

        arge_berufe_net_response_page = cls(
            content=content,
            pageable=pageable,
            last=last,
            total_elements=total_elements,
            total_pages=total_pages,
            first=first,
            size=size,
            number=number,
            sort=sort,
            number_of_elements=number_of_elements,
            empty=empty,
        )

        arge_berufe_net_response_page.additional_properties = d
        return arge_berufe_net_response_page

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
