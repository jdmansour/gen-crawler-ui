from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.text_statistics_result_classification_type_0 import TextStatisticsResultClassificationType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="TextStatisticsResult")


@_attrs_define
class TextStatisticsResult:
    """
    Attributes:
        flesch_ease (Union[None, float]):
        classification (Union[None, TextStatisticsResultClassificationType0]):
        wiener_index (Union[None, float]):
        reading_time (Union[None, float]):
        embeddings (Union[None, list[float]]):
        version (Union[Unset, str]):  Default: '1.1.0'.
    """

    flesch_ease: Union[None, float]
    classification: Union[None, TextStatisticsResultClassificationType0]
    wiener_index: Union[None, float]
    reading_time: Union[None, float]
    embeddings: Union[None, list[float]]
    version: Union[Unset, str] = "1.1.0"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flesch_ease: Union[None, float]
        flesch_ease = self.flesch_ease

        classification: Union[None, str]
        if isinstance(self.classification, TextStatisticsResultClassificationType0):
            classification = self.classification.value
        else:
            classification = self.classification

        wiener_index: Union[None, float]
        wiener_index = self.wiener_index

        reading_time: Union[None, float]
        reading_time = self.reading_time

        embeddings: Union[None, list[float]]
        if isinstance(self.embeddings, list):
            embeddings = self.embeddings

        else:
            embeddings = self.embeddings

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flesch_ease": flesch_ease,
                "classification": classification,
                "wiener_index": wiener_index,
                "reading_time": reading_time,
                "embeddings": embeddings,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_flesch_ease(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        flesch_ease = _parse_flesch_ease(d.pop("flesch_ease"))

        def _parse_classification(data: object) -> Union[None, TextStatisticsResultClassificationType0]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                classification_type_0 = TextStatisticsResultClassificationType0(data)

                return classification_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TextStatisticsResultClassificationType0], data)

        classification = _parse_classification(d.pop("classification"))

        def _parse_wiener_index(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        wiener_index = _parse_wiener_index(d.pop("wiener_index"))

        def _parse_reading_time(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        reading_time = _parse_reading_time(d.pop("reading_time"))

        def _parse_embeddings(data: object) -> Union[None, list[float]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                embeddings_type_0 = cast(list[float], data)

                return embeddings_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[float]], data)

        embeddings = _parse_embeddings(d.pop("embeddings"))

        version = d.pop("version", UNSET)

        text_statistics_result = cls(
            flesch_ease=flesch_ease,
            classification=classification,
            wiener_index=wiener_index,
            reading_time=reading_time,
            embeddings=embeddings,
            version=version,
        )

        text_statistics_result.additional_properties = d
        return text_statistics_result

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
