from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.topic_statistics_category_count import TopicStatisticsCategoryCount


T = TypeVar("T", bound="TopicStatisticsFieldCounts")


@_attrs_define
class TopicStatisticsFieldCounts:
    """
    Attributes:
        field (str):
        counts (list['TopicStatisticsCategoryCount']):
    """

    field: str
    counts: list["TopicStatisticsCategoryCount"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        counts = []
        for counts_item_data in self.counts:
            counts_item = counts_item_data.to_dict()
            counts.append(counts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "counts": counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.topic_statistics_category_count import TopicStatisticsCategoryCount

        d = src_dict.copy()
        field = d.pop("field")

        counts = []
        _counts = d.pop("counts")
        for counts_item_data in _counts:
            counts_item = TopicStatisticsCategoryCount.from_dict(counts_item_data)

            counts.append(counts_item)

        topic_statistics_field_counts = cls(
            field=field,
            counts=counts,
        )

        topic_statistics_field_counts.additional_properties = d
        return topic_statistics_field_counts

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
