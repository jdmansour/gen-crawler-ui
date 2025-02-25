from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PredictionScore")


@_attrs_define
class PredictionScore:
    """An individual prediction for a particular target.

    Attributes:
        id (str):
        name (str):
        mean_prob (float):
        median_prob (float):
        baseline_diff (float):
        prob_interval (list[float]):
    """

    id: str
    name: str
    mean_prob: float
    median_prob: float
    baseline_diff: float
    prob_interval: list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        mean_prob = self.mean_prob

        median_prob = self.median_prob

        baseline_diff = self.baseline_diff

        prob_interval = self.prob_interval

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "mean_prob": mean_prob,
                "median_prob": median_prob,
                "baseline_diff": baseline_diff,
                "prob_interval": prob_interval,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        mean_prob = d.pop("mean_prob")

        median_prob = d.pop("median_prob")

        baseline_diff = d.pop("baseline_diff")

        prob_interval = cast(list[float], d.pop("prob_interval"))

        prediction_score = cls(
            id=id,
            name=name,
            mean_prob=mean_prob,
            median_prob=median_prob,
            baseline_diff=baseline_diff,
            prob_interval=prob_interval,
        )

        prediction_score.additional_properties = d
        return prediction_score

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
