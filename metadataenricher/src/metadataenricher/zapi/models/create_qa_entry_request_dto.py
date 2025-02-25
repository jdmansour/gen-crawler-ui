from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateQAEntryRequestDTO")


@_attrs_define
class CreateQAEntryRequestDTO:
    """
    Attributes:
        question (Union[Unset, str]):
        answer (Union[Unset, str]):
    """

    question: Union[Unset, str] = UNSET
    answer: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        question = self.question

        answer = self.answer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if question is not UNSET:
            field_dict["question"] = question
        if answer is not UNSET:
            field_dict["answer"] = answer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        question = d.pop("question", UNSET)

        answer = d.pop("answer", UNSET)

        create_qa_entry_request_dto = cls(
            question=question,
            answer=answer,
        )

        create_qa_entry_request_dto.additional_properties = d
        return create_qa_entry_request_dto

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
