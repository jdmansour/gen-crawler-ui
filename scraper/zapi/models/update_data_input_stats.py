from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDataInputStats")


@_attrs_define
class UpdateDataInputStats:
    """
    Attributes:
        topic_uri (str):
        topic_url (str):
        group_by_fields (Union[None, Unset, list[Fields]]):
    """

    topic_uri: str
    topic_url: str
    group_by_fields: Union[None, Unset, list[Fields]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic_uri = self.topic_uri

        topic_url = self.topic_url

        group_by_fields: Union[None, Unset, list[str]]
        if isinstance(self.group_by_fields, Unset):
            group_by_fields = UNSET
        elif isinstance(self.group_by_fields, list):
            group_by_fields = []
            for group_by_fields_type_0_item_data in self.group_by_fields:
                group_by_fields_type_0_item = group_by_fields_type_0_item_data.value
                group_by_fields.append(group_by_fields_type_0_item)

        else:
            group_by_fields = self.group_by_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic_uri": topic_uri,
                "topic_url": topic_url,
            }
        )
        if group_by_fields is not UNSET:
            field_dict["group_by_fields"] = group_by_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        topic_uri = d.pop("topic_uri")

        topic_url = d.pop("topic_url")

        def _parse_group_by_fields(data: object) -> Union[None, Unset, list[Fields]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                group_by_fields_type_0 = []
                _group_by_fields_type_0 = data
                for group_by_fields_type_0_item_data in _group_by_fields_type_0:
                    group_by_fields_type_0_item = Fields(group_by_fields_type_0_item_data)

                    group_by_fields_type_0.append(group_by_fields_type_0_item)

                return group_by_fields_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Fields]], data)

        group_by_fields = _parse_group_by_fields(d.pop("group_by_fields", UNSET))

        update_data_input_stats = cls(
            topic_uri=topic_uri,
            topic_url=topic_url,
            group_by_fields=group_by_fields,
        )

        update_data_input_stats.additional_properties = d
        return update_data_input_stats

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
