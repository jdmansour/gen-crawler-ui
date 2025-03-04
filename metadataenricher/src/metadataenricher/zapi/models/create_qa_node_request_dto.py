from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_qa_entry_request_dto import CreateQAEntryRequestDTO


T = TypeVar("T", bound="CreateQANodeRequestDTO")


@_attrs_define
class CreateQANodeRequestDTO:
    """
    Attributes:
        used_text (Union[Unset, str]):
        entries (Union[Unset, list['CreateQAEntryRequestDTO']]):
    """

    used_text: Union[Unset, str] = UNSET
    entries: Union[Unset, list["CreateQAEntryRequestDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used_text = self.used_text

        entries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()
                entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if used_text is not UNSET:
            field_dict["usedText"] = used_text
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_qa_entry_request_dto import CreateQAEntryRequestDTO

        d = src_dict.copy()
        used_text = d.pop("usedText", UNSET)

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = CreateQAEntryRequestDTO.from_dict(entries_item_data)

            entries.append(entries_item)

        create_qa_node_request_dto = cls(
            used_text=used_text,
            entries=entries,
        )

        create_qa_node_request_dto.additional_properties = d
        return create_qa_node_request_dto

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
