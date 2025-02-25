from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entity import Entity


T = TypeVar("T", bound="Result")


@_attrs_define
class Result:
    """
    Attributes:
        text (str):
        entities (list['Entity']):
        essential_categories (list[str]):
        version (Union[Unset, str]):  Default: '0.1.0'.
    """

    text: str
    entities: list["Entity"]
    essential_categories: list[str]
    version: Union[Unset, str] = "0.1.0"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        entities = []
        for entities_item_data in self.entities:
            entities_item = entities_item_data.to_dict()
            entities.append(entities_item)

        essential_categories = self.essential_categories

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "entities": entities,
                "essentialCategories": essential_categories,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entity import Entity

        d = src_dict.copy()
        text = d.pop("text")

        entities = []
        _entities = d.pop("entities")
        for entities_item_data in _entities:
            entities_item = Entity.from_dict(entities_item_data)

            entities.append(entities_item)

        essential_categories = cast(list[str], d.pop("essentialCategories"))

        version = d.pop("version", UNSET)

        result = cls(
            text=text,
            entities=entities,
            essential_categories=essential_categories,
            version=version,
        )

        result.additional_properties = d
        return result

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
