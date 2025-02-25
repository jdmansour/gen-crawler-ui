from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PredictionData")


@_attrs_define
class PredictionData:
    """Input to be used for prediction.

    Attributes:
        text (str):
        num_samples (Union[Unset, int]):  Default: 500.
        num_predictions (Union[Unset, int]):  Default: 10.
        interval_size (Union[Unset, float]):  Default: 0.8.
    """

    text: str
    num_samples: Union[Unset, int] = 500
    num_predictions: Union[Unset, int] = 10
    interval_size: Union[Unset, float] = 0.8
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        num_samples = self.num_samples

        num_predictions = self.num_predictions

        interval_size = self.interval_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if num_predictions is not UNSET:
            field_dict["num_predictions"] = num_predictions
        if interval_size is not UNSET:
            field_dict["interval_size"] = interval_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text")

        num_samples = d.pop("num_samples", UNSET)

        num_predictions = d.pop("num_predictions", UNSET)

        interval_size = d.pop("interval_size", UNSET)

        prediction_data = cls(
            text=text,
            num_samples=num_samples,
            num_predictions=num_predictions,
            interval_size=interval_size,
        )

        prediction_data.additional_properties = d
        return prediction_data

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
