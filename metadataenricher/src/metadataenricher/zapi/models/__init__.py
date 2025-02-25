"""Contains all the data models used in inputs/outputs"""

from .arge_berufe_net_request import ArgeBerufeNetRequest
from .arge_berufe_net_response import ArgeBerufeNetResponse
from .arge_berufe_net_response_page import ArgeBerufeNetResponsePage
from .assistant_message import AssistantMessage
from .assistant_message_audio import AssistantMessageAudio
from .bayesian_predictions_http_validation_error import BayesianPredictionsHTTPValidationError
from .bayesian_predictions_validation_error import BayesianPredictionsValidationError
from .binary import Binary
from .chat_function_call import ChatFunctionCall
from .chat_message import ChatMessage
from .chat_tool_call import ChatToolCall
from .create_api_key_request import CreateApiKeyRequest
from .create_qa_entry_request_dto import CreateQAEntryRequestDTO
from .create_qa_node_request_dto import CreateQANodeRequestDTO
from .data import Data
from .discipline import Discipline
from .disciplines_data import DisciplinesData
from .disciplines_http_validation_error import DisciplinesHTTPValidationError
from .disciplines_result import DisciplinesResult
from .disciplines_validation_error import DisciplinesValidationError
from .entity import Entity
from .fields import Fields
from .function_message import FunctionMessage
from .get_default_widget_prompts_response_200 import GetDefaultWidgetPromptsResponse200
from .get_predefined_prompt_for_collection_mode import GetPredefinedPromptForCollectionMode
from .http_validation_error import HTTPValidationError
from .image_prompt_entity import ImagePromptEntity
from .input_data import InputData
from .json_node import JsonNode
from .methods import Methods
from .pageablenull import Pageablenull
from .prediction_data import PredictionData
from .prediction_result import PredictionResult
from .prediction_result_predictions import PredictionResultPredictions
from .prediction_score import PredictionScore
from .profession_description_entity import ProfessionDescriptionEntity
from .profession_profile_entity import ProfessionProfileEntity
from .profession_profile_info import ProfessionProfileInfo
from .professions_job_entity import ProfessionsJobEntity
from .public_prompt_1_body import PublicPrompt1Body
from .public_prompt_2_body import PublicPrompt2Body
from .public_prompt_3_body import PublicPrompt3Body
from .public_prompt_4_body import PublicPrompt4Body
from .public_prompt_body import PublicPromptBody
from .qa_entry import QAEntry
from .qa_node import QANode
from .result import Result
from .sortnull import Sortnull
from .system_message import SystemMessage
from .text_extraction_data import TextExtractionData
from .text_extraction_data_preference import TextExtractionDataPreference
from .text_extraction_http_validation_error import TextExtractionHTTPValidationError
from .text_extraction_result import TextExtractionResult
from .text_extraction_validation_error import TextExtractionValidationError
from .text_prompt_entity import TextPromptEntity
from .text_statistics_http_validation_error import TextStatisticsHTTPValidationError
from .text_statistics_result import TextStatisticsResult
from .text_statistics_result_classification_type_0 import TextStatisticsResultClassificationType0
from .text_statistics_validation_error import TextStatisticsValidationError
from .tool_message import ToolMessage
from .topic_assistant_embeddings_data import TopicAssistantEmbeddingsData
from .topic_assistant_embeddings_http_validation_error import TopicAssistantEmbeddingsHTTPValidationError
from .topic_assistant_embeddings_result import TopicAssistantEmbeddingsResult
from .topic_assistant_embeddings_topic import TopicAssistantEmbeddingsTopic
from .topic_assistant_embeddings_validation_error import TopicAssistantEmbeddingsValidationError
from .topic_assistant_keywords_data import TopicAssistantKeywordsData
from .topic_assistant_keywords_http_validation_error import TopicAssistantKeywordsHTTPValidationError
from .topic_assistant_keywords_result import TopicAssistantKeywordsResult
from .topic_assistant_keywords_topic import TopicAssistantKeywordsTopic
from .topic_assistant_keywords_validation_error import TopicAssistantKeywordsValidationError
from .topic_statistics_category_count import TopicStatisticsCategoryCount
from .topic_statistics_count import TopicStatisticsCount
from .topic_statistics_field_counts import TopicStatisticsFieldCounts
from .topic_statistics_http_validation_error import TopicStatisticsHTTPValidationError
from .topic_statistics_input_stats import TopicStatisticsInputStats
from .topic_statistics_input_update import TopicStatisticsInputUpdate
from .topic_statistics_output_stats import TopicStatisticsOutputStats
from .topic_statistics_validation_error import TopicStatisticsValidationError
from .update_data_category_count import UpdateDataCategoryCount
from .update_data_count import UpdateDataCount
from .update_data_field_counts import UpdateDataFieldCounts
from .update_data_http_validation_error import UpdateDataHTTPValidationError
from .update_data_input_stats import UpdateDataInputStats
from .update_data_input_update import UpdateDataInputUpdate
from .update_data_output_stats import UpdateDataOutputStats
from .update_data_validation_error import UpdateDataValidationError
from .update_public_prompt_1_body import UpdatePublicPrompt1Body
from .update_public_prompt_2_body import UpdatePublicPrompt2Body
from .update_public_prompt_3_body import UpdatePublicPrompt3Body
from .update_public_prompt_4_body import UpdatePublicPrompt4Body
from .update_public_prompt_body import UpdatePublicPromptBody
from .update_qa_entries_request_dto import UpdateQAEntriesRequestDTO
from .user_message import UserMessage
from .validation_error import ValidationError
from .widget_object import WidgetObject

__all__ = (
    "ArgeBerufeNetRequest",
    "ArgeBerufeNetResponse",
    "ArgeBerufeNetResponsePage",
    "AssistantMessage",
    "AssistantMessageAudio",
    "BayesianPredictionsHTTPValidationError",
    "BayesianPredictionsValidationError",
    "Binary",
    "ChatFunctionCall",
    "ChatMessage",
    "ChatToolCall",
    "CreateApiKeyRequest",
    "CreateQAEntryRequestDTO",
    "CreateQANodeRequestDTO",
    "Data",
    "Discipline",
    "DisciplinesData",
    "DisciplinesHTTPValidationError",
    "DisciplinesResult",
    "DisciplinesValidationError",
    "Entity",
    "Fields",
    "FunctionMessage",
    "GetDefaultWidgetPromptsResponse200",
    "GetPredefinedPromptForCollectionMode",
    "HTTPValidationError",
    "ImagePromptEntity",
    "InputData",
    "JsonNode",
    "Methods",
    "Pageablenull",
    "PredictionData",
    "PredictionResult",
    "PredictionResultPredictions",
    "PredictionScore",
    "ProfessionDescriptionEntity",
    "ProfessionProfileEntity",
    "ProfessionProfileInfo",
    "ProfessionsJobEntity",
    "PublicPrompt1Body",
    "PublicPrompt2Body",
    "PublicPrompt3Body",
    "PublicPrompt4Body",
    "PublicPromptBody",
    "QAEntry",
    "QANode",
    "Result",
    "Sortnull",
    "SystemMessage",
    "TextExtractionData",
    "TextExtractionDataPreference",
    "TextExtractionHTTPValidationError",
    "TextExtractionResult",
    "TextExtractionValidationError",
    "TextPromptEntity",
    "TextStatisticsHTTPValidationError",
    "TextStatisticsResult",
    "TextStatisticsResultClassificationType0",
    "TextStatisticsValidationError",
    "ToolMessage",
    "TopicAssistantEmbeddingsData",
    "TopicAssistantEmbeddingsHTTPValidationError",
    "TopicAssistantEmbeddingsResult",
    "TopicAssistantEmbeddingsTopic",
    "TopicAssistantEmbeddingsValidationError",
    "TopicAssistantKeywordsData",
    "TopicAssistantKeywordsHTTPValidationError",
    "TopicAssistantKeywordsResult",
    "TopicAssistantKeywordsTopic",
    "TopicAssistantKeywordsValidationError",
    "TopicStatisticsCategoryCount",
    "TopicStatisticsCount",
    "TopicStatisticsFieldCounts",
    "TopicStatisticsHTTPValidationError",
    "TopicStatisticsInputStats",
    "TopicStatisticsInputUpdate",
    "TopicStatisticsOutputStats",
    "TopicStatisticsValidationError",
    "UpdateDataCategoryCount",
    "UpdateDataCount",
    "UpdateDataFieldCounts",
    "UpdateDataHTTPValidationError",
    "UpdateDataInputStats",
    "UpdateDataInputUpdate",
    "UpdateDataOutputStats",
    "UpdateDataValidationError",
    "UpdatePublicPrompt1Body",
    "UpdatePublicPrompt2Body",
    "UpdatePublicPrompt3Body",
    "UpdatePublicPrompt4Body",
    "UpdatePublicPromptBody",
    "UpdateQAEntriesRequestDTO",
    "UserMessage",
    "ValidationError",
    "WidgetObject",
)
