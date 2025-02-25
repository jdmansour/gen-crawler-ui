from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topic_assistant_embeddings_topic import TopicAssistantEmbeddingsTopic


T = TypeVar("T", bound="TopicAssistantEmbeddingsResult")


@_attrs_define
class TopicAssistantEmbeddingsResult:
    """
    Attributes:
        topics (list['TopicAssistantEmbeddingsTopic']):
        version (Union[Unset, str]):  Default: '0.1.4'.
    """

    topics: list["TopicAssistantEmbeddingsTopic"]
    version: Union[Unset, str] = "0.1.4"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topics = []
        for topics_item_data in self.topics:
            topics_item = topics_item_data.to_dict()
            topics.append(topics_item)

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topics": topics,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.topic_assistant_embeddings_topic import TopicAssistantEmbeddingsTopic

        d = src_dict.copy()
        topics = []
        _topics = d.pop("topics")
        for topics_item_data in _topics:
            topics_item = TopicAssistantEmbeddingsTopic.from_dict(topics_item_data)

            topics.append(topics_item)

        version = d.pop("version", UNSET)

        topic_assistant_embeddings_result = cls(
            topics=topics,
            version=version,
        )

        topic_assistant_embeddings_result.additional_properties = d
        return topic_assistant_embeddings_result

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
