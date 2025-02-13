from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistant_message_audio import AssistantMessageAudio
    from ..models.chat_function_call import ChatFunctionCall
    from ..models.chat_tool_call import ChatToolCall


T = TypeVar("T", bound="AssistantMessage")


@_attrs_define
class AssistantMessage:
    """
    Attributes:
        text_content (Union[Unset, str]):
        name (Union[Unset, str]):
        role (Union[Unset, str]):
        content (Union[Unset, str]):
        refusal (Union[Unset, str]):
        audio (Union[Unset, AssistantMessageAudio]):
        tool_calls (Union[Unset, list['ChatToolCall']]):
        function_call (Union[Unset, ChatFunctionCall]):
    """

    text_content: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    refusal: Union[Unset, str] = UNSET
    audio: Union[Unset, "AssistantMessageAudio"] = UNSET
    tool_calls: Union[Unset, list["ChatToolCall"]] = UNSET
    function_call: Union[Unset, "ChatFunctionCall"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text_content = self.text_content

        name = self.name

        role = self.role

        content = self.content

        refusal = self.refusal

        audio: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.audio, Unset):
            audio = self.audio.to_dict()

        tool_calls: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tool_calls, Unset):
            tool_calls = []
            for tool_calls_item_data in self.tool_calls:
                tool_calls_item = tool_calls_item_data.to_dict()
                tool_calls.append(tool_calls_item)

        function_call: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.function_call, Unset):
            function_call = self.function_call.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text_content is not UNSET:
            field_dict["textContent"] = text_content
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role
        if content is not UNSET:
            field_dict["content"] = content
        if refusal is not UNSET:
            field_dict["refusal"] = refusal
        if audio is not UNSET:
            field_dict["audio"] = audio
        if tool_calls is not UNSET:
            field_dict["tool_calls"] = tool_calls
        if function_call is not UNSET:
            field_dict["function_call"] = function_call

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.assistant_message_audio import AssistantMessageAudio
        from ..models.chat_function_call import ChatFunctionCall
        from ..models.chat_tool_call import ChatToolCall

        d = src_dict.copy()
        text_content = d.pop("textContent", UNSET)

        name = d.pop("name", UNSET)

        role = d.pop("role", UNSET)

        content = d.pop("content", UNSET)

        refusal = d.pop("refusal", UNSET)

        _audio = d.pop("audio", UNSET)
        audio: Union[Unset, AssistantMessageAudio]
        if isinstance(_audio, Unset):
            audio = UNSET
        else:
            audio = AssistantMessageAudio.from_dict(_audio)

        tool_calls = []
        _tool_calls = d.pop("tool_calls", UNSET)
        for tool_calls_item_data in _tool_calls or []:
            tool_calls_item = ChatToolCall.from_dict(tool_calls_item_data)

            tool_calls.append(tool_calls_item)

        _function_call = d.pop("function_call", UNSET)
        function_call: Union[Unset, ChatFunctionCall]
        if isinstance(_function_call, Unset):
            function_call = UNSET
        else:
            function_call = ChatFunctionCall.from_dict(_function_call)

        assistant_message = cls(
            text_content=text_content,
            name=name,
            role=role,
            content=content,
            refusal=refusal,
            audio=audio,
            tool_calls=tool_calls,
            function_call=function_call,
        )

        assistant_message.additional_properties = d
        return assistant_message

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
