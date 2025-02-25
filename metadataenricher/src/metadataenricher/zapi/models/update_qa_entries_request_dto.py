from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.qa_entry import QAEntry


T = TypeVar("T", bound="UpdateQAEntriesRequestDTO")


@_attrs_define
class UpdateQAEntriesRequestDTO:
    """
    Attributes:
        qa_entries (Union[Unset, list['QAEntry']]):
    """

    qa_entries: Union[Unset, list["QAEntry"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        qa_entries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.qa_entries, Unset):
            qa_entries = []
            for qa_entries_item_data in self.qa_entries:
                qa_entries_item = qa_entries_item_data.to_dict()
                qa_entries.append(qa_entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if qa_entries is not UNSET:
            field_dict["qaEntries"] = qa_entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.qa_entry import QAEntry

        d = src_dict.copy()
        qa_entries = []
        _qa_entries = d.pop("qaEntries", UNSET)
        for qa_entries_item_data in _qa_entries or []:
            qa_entries_item = QAEntry.from_dict(qa_entries_item_data)

            qa_entries.append(qa_entries_item)

        update_qa_entries_request_dto = cls(
            qa_entries=qa_entries,
        )

        update_qa_entries_request_dto.additional_properties = d
        return update_qa_entries_request_dto

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
