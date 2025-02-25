from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Entity")


@_attrs_define
class Entity:
    """
    Attributes:
        entity (str):
        start (int):
        end (int):
        score (float):
        categories (list[str]):
    """

    entity: str
    start: int
    end: int
    score: float
    categories: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity = self.entity

        start = self.start

        end = self.end

        score = self.score

        categories = self.categories

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity": entity,
                "start": start,
                "end": end,
                "score": score,
                "categories": categories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        entity = d.pop("entity")

        start = d.pop("start")

        end = d.pop("end")

        score = d.pop("score")

        categories = cast(list[str], d.pop("categories"))

        entity = cls(
            entity=entity,
            start=start,
            end=end,
            score=score,
            categories=categories,
        )

        entity.additional_properties = d
        return entity

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
