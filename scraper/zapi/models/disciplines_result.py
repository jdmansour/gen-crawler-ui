from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.discipline import Discipline


T = TypeVar("T", bound="DisciplinesResult")


@_attrs_define
class DisciplinesResult:
    """
    Attributes:
        disciplines (list['Discipline']):
        version (Union[Unset, str]):  Default: '0.1.0'.
    """

    disciplines: list["Discipline"]
    version: Union[Unset, str] = "0.1.0"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        disciplines = []
        for disciplines_item_data in self.disciplines:
            disciplines_item = disciplines_item_data.to_dict()
            disciplines.append(disciplines_item)

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disciplines": disciplines,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.discipline import Discipline

        d = src_dict.copy()
        disciplines = []
        _disciplines = d.pop("disciplines")
        for disciplines_item_data in _disciplines:
            disciplines_item = Discipline.from_dict(disciplines_item_data)

            disciplines.append(disciplines_item)

        version = d.pop("version", UNSET)

        disciplines_result = cls(
            disciplines=disciplines,
            version=version,
        )

        disciplines_result.additional_properties = d
        return disciplines_result

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
