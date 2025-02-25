from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prediction_result_predictions import PredictionResultPredictions


T = TypeVar("T", bound="PredictionResult")


@_attrs_define
class PredictionResult:
    """The output of the prediction.

    Attributes:
        predictions (PredictionResultPredictions):
        version (Union[Unset, str]):  Default: '0.2.4'.
    """

    predictions: "PredictionResultPredictions"
    version: Union[Unset, str] = "0.2.4"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        predictions = self.predictions.to_dict()

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "predictions": predictions,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.prediction_result_predictions import PredictionResultPredictions

        d = src_dict.copy()
        predictions = PredictionResultPredictions.from_dict(d.pop("predictions"))

        version = d.pop("version", UNSET)

        prediction_result = cls(
            predictions=predictions,
            version=version,
        )

        prediction_result.additional_properties = d
        return prediction_result

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
