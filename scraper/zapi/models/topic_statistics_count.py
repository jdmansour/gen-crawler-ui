from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TopicStatisticsCount")


@_attrs_define
class TopicStatisticsCount:
    """
    Attributes:
        total (int):
        editorially_confirmed (int):
    """

    total: int
    editorially_confirmed: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        editorially_confirmed = self.editorially_confirmed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "editorially_confirmed": editorially_confirmed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        total = d.pop("total")

        editorially_confirmed = d.pop("editorially_confirmed")

        topic_statistics_count = cls(
            total=total,
            editorially_confirmed=editorially_confirmed,
        )

        topic_statistics_count.additional_properties = d
        return topic_statistics_count

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
