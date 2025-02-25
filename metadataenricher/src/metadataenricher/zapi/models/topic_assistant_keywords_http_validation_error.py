from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topic_assistant_keywords_validation_error import TopicAssistantKeywordsValidationError


T = TypeVar("T", bound="TopicAssistantKeywordsHTTPValidationError")


@_attrs_define
class TopicAssistantKeywordsHTTPValidationError:
    """
    Attributes:
        detail (Union[Unset, list['TopicAssistantKeywordsValidationError']]):
    """

    detail: Union[Unset, list["TopicAssistantKeywordsValidationError"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.detail, Unset):
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()
                detail.append(detail_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.topic_assistant_keywords_validation_error import TopicAssistantKeywordsValidationError

        d = src_dict.copy()
        detail = []
        _detail = d.pop("detail", UNSET)
        for detail_item_data in _detail or []:
            detail_item = TopicAssistantKeywordsValidationError.from_dict(detail_item_data)

            detail.append(detail_item)

        topic_assistant_keywords_http_validation_error = cls(
            detail=detail,
        )

        topic_assistant_keywords_http_validation_error.additional_properties = d
        return topic_assistant_keywords_http_validation_error

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
