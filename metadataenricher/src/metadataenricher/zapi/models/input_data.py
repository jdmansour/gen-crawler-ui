from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InputData")


@_attrs_define
class InputData:
    """
    Attributes:
        text (str):
        reading_speed (Union[Unset, float]):  Default: 200.0.
        generate_embeddings (Union[Unset, bool]):  Default: False.
    """

    text: str
    reading_speed: Union[Unset, float] = 200.0
    generate_embeddings: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        reading_speed = self.reading_speed

        generate_embeddings = self.generate_embeddings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if reading_speed is not UNSET:
            field_dict["reading_speed"] = reading_speed
        if generate_embeddings is not UNSET:
            field_dict["generate_embeddings"] = generate_embeddings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text")

        reading_speed = d.pop("reading_speed", UNSET)

        generate_embeddings = d.pop("generate_embeddings", UNSET)

        input_data = cls(
            text=text,
            reading_speed=reading_speed,
            generate_embeddings=generate_embeddings,
        )

        input_data.additional_properties = d
        return input_data

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
