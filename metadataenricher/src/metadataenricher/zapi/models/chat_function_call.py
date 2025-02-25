from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.json_node import JsonNode


T = TypeVar("T", bound="ChatFunctionCall")


@_attrs_define
class ChatFunctionCall:
    """
    Attributes:
        name (Union[Unset, str]):
        arguments (Union[Unset, JsonNode]):
    """

    name: Union[Unset, str] = UNSET
    arguments: Union[Unset, "JsonNode"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        arguments: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.arguments, Unset):
            arguments = self.arguments.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if arguments is not UNSET:
            field_dict["arguments"] = arguments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.json_node import JsonNode

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _arguments = d.pop("arguments", UNSET)
        arguments: Union[Unset, JsonNode]
        if isinstance(_arguments, Unset):
            arguments = UNSET
        else:
            arguments = JsonNode.from_dict(_arguments)

        chat_function_call = cls(
            name=name,
            arguments=arguments,
        )

        chat_function_call.additional_properties = d
        return chat_function_call

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
