from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_function_call import ChatFunctionCall


T = TypeVar("T", bound="ChatToolCall")


@_attrs_define
class ChatToolCall:
    """
    Attributes:
        index (Union[Unset, int]):
        id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        function (Union[Unset, ChatFunctionCall]):
    """

    index: Union[Unset, int] = UNSET
    id: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    function: Union[Unset, "ChatFunctionCall"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        id = self.id

        type_ = self.type_

        function: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.function, Unset):
            function = self.function.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if index is not UNSET:
            field_dict["index"] = index
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if function is not UNSET:
            field_dict["function"] = function

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.chat_function_call import ChatFunctionCall

        d = src_dict.copy()
        index = d.pop("index", UNSET)

        id = d.pop("id", UNSET)

        type_ = d.pop("type", UNSET)

        _function = d.pop("function", UNSET)
        function: Union[Unset, ChatFunctionCall]
        if isinstance(_function, Unset):
            function = UNSET
        else:
            function = ChatFunctionCall.from_dict(_function)

        chat_tool_call = cls(
            index=index,
            id=id,
            type_=type_,
            function=function,
        )

        chat_tool_call.additional_properties = d
        return chat_tool_call

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
