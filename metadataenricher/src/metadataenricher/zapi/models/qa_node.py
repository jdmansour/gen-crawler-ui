import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.qa_entry import QAEntry


T = TypeVar("T", bound="QANode")


@_attrs_define
class QANode:
    """
    Attributes:
        id (Union[Unset, str]):
        source_id (Union[Unset, str]):
        node_id (Union[Unset, str]):
        generated_date (Union[Unset, datetime.datetime]):
        used_text (Union[Unset, str]):
        entries (Union[Unset, list['QAEntry']]):
    """

    id: Union[Unset, str] = UNSET
    source_id: Union[Unset, str] = UNSET
    node_id: Union[Unset, str] = UNSET
    generated_date: Union[Unset, datetime.datetime] = UNSET
    used_text: Union[Unset, str] = UNSET
    entries: Union[Unset, list["QAEntry"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        source_id = self.source_id

        node_id = self.node_id

        generated_date: Union[Unset, str] = UNSET
        if not isinstance(self.generated_date, Unset):
            generated_date = self.generated_date.isoformat()

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
        if id is not UNSET:
            field_dict["id"] = id
        if source_id is not UNSET:
            field_dict["sourceId"] = source_id
        if node_id is not UNSET:
            field_dict["nodeId"] = node_id
        if generated_date is not UNSET:
            field_dict["generatedDate"] = generated_date
        if used_text is not UNSET:
            field_dict["usedText"] = used_text
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.qa_entry import QAEntry

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        source_id = d.pop("sourceId", UNSET)

        node_id = d.pop("nodeId", UNSET)

        _generated_date = d.pop("generatedDate", UNSET)
        generated_date: Union[Unset, datetime.datetime]
        if isinstance(_generated_date, Unset):
            generated_date = UNSET
        else:
            generated_date = isoparse(_generated_date)

        used_text = d.pop("usedText", UNSET)

        entries = []
        _entries = d.pop("entries", UNSET)
        for entries_item_data in _entries or []:
            entries_item = QAEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        qa_node = cls(
            id=id,
            source_id=source_id,
            node_id=node_id,
            generated_date=generated_date,
            used_text=used_text,
            entries=entries,
        )

        qa_node.additional_properties = d
        return qa_node

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
