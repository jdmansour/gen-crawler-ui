import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="QAEntry")


@_attrs_define
class QAEntry:
    """
    Attributes:
        question (Union[Unset, str]):
        answer (Union[Unset, str]):
        reviewed (Union[Unset, bool]):
        edited (Union[Unset, bool]):
        last_reviewed (Union[Unset, datetime.datetime]):
        reviewed_by (Union[Unset, str]):
    """

    question: Union[Unset, str] = UNSET
    answer: Union[Unset, str] = UNSET
    reviewed: Union[Unset, bool] = UNSET
    edited: Union[Unset, bool] = UNSET
    last_reviewed: Union[Unset, datetime.datetime] = UNSET
    reviewed_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        answer = self.answer

        reviewed = self.reviewed

        edited = self.edited

        last_reviewed: Union[Unset, str] = UNSET
        if not isinstance(self.last_reviewed, Unset):
            last_reviewed = self.last_reviewed.isoformat()

        reviewed_by = self.reviewed_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if question is not UNSET:
            field_dict["question"] = question
        if answer is not UNSET:
            field_dict["answer"] = answer
        if reviewed is not UNSET:
            field_dict["reviewed"] = reviewed
        if edited is not UNSET:
            field_dict["edited"] = edited
        if last_reviewed is not UNSET:
            field_dict["lastReviewed"] = last_reviewed
        if reviewed_by is not UNSET:
            field_dict["reviewedBy"] = reviewed_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        question = d.pop("question", UNSET)

        answer = d.pop("answer", UNSET)

        reviewed = d.pop("reviewed", UNSET)

        edited = d.pop("edited", UNSET)

        _last_reviewed = d.pop("lastReviewed", UNSET)
        last_reviewed: Union[Unset, datetime.datetime]
        if isinstance(_last_reviewed, Unset):
            last_reviewed = UNSET
        else:
            last_reviewed = isoparse(_last_reviewed)

        reviewed_by = d.pop("reviewedBy", UNSET)

        qa_entry = cls(
            question=question,
            answer=answer,
            reviewed=reviewed,
            edited=edited,
            last_reviewed=last_reviewed,
            reviewed_by=reviewed_by,
        )

        qa_entry.additional_properties = d
        return qa_entry

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
