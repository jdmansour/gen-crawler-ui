from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_data_count import UpdateDataCount
    from ..models.update_data_field_counts import UpdateDataFieldCounts


T = TypeVar("T", bound="UpdateDataOutputStats")


@_attrs_define
class UpdateDataOutputStats:
    """
    Attributes:
        total (UpdateDataCount):
        by_fields (Union[None, Unset, list['UpdateDataFieldCounts']]):
    """

    total: "UpdateDataCount"
    by_fields: Union[None, Unset, list["UpdateDataFieldCounts"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total.to_dict()

        by_fields: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.by_fields, Unset):
            by_fields = UNSET
        elif isinstance(self.by_fields, list):
            by_fields = []
            for by_fields_type_0_item_data in self.by_fields:
                by_fields_type_0_item = by_fields_type_0_item_data.to_dict()
                by_fields.append(by_fields_type_0_item)

        else:
            by_fields = self.by_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
            }
        )
        if by_fields is not UNSET:
            field_dict["by_fields"] = by_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.update_data_count import UpdateDataCount
        from ..models.update_data_field_counts import UpdateDataFieldCounts

        d = src_dict.copy()
        total = UpdateDataCount.from_dict(d.pop("total"))

        def _parse_by_fields(data: object) -> Union[None, Unset, list["UpdateDataFieldCounts"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_fields_type_0 = []
                _by_fields_type_0 = data
                for by_fields_type_0_item_data in _by_fields_type_0:
                    by_fields_type_0_item = UpdateDataFieldCounts.from_dict(by_fields_type_0_item_data)

                    by_fields_type_0.append(by_fields_type_0_item)

                return by_fields_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["UpdateDataFieldCounts"]], data)

        by_fields = _parse_by_fields(d.pop("by_fields", UNSET))

        update_data_output_stats = cls(
            total=total,
            by_fields=by_fields,
        )

        update_data_output_stats.additional_properties = d
        return update_data_output_stats

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
