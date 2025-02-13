from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TopicAssistantEmbeddingsTopic")


@_attrs_define
class TopicAssistantEmbeddingsTopic:
    """
    Attributes:
        weight (float):
        uri (str):
        label (Union[None, Unset, str]):
        match (Union[None, Unset, str]):
    """

    weight: float
    uri: str
    label: Union[None, Unset, str] = UNSET
    match: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        weight = self.weight

        uri = self.uri

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        match: Union[None, Unset, str]
        if isinstance(self.match, Unset):
            match = UNSET
        else:
            match = self.match

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "weight": weight,
                "uri": uri,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if match is not UNSET:
            field_dict["match"] = match

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        weight = d.pop("weight")

        uri = d.pop("uri")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_match(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        match = _parse_match(d.pop("match", UNSET))

        topic_assistant_embeddings_topic = cls(
            weight=weight,
            uri=uri,
            label=label,
            match=match,
        )

        topic_assistant_embeddings_topic.additional_properties = d
        return topic_assistant_embeddings_topic

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
