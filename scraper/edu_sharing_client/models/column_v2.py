# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.  # noqa: E501

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class ColumnV2(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'format': 'str',
        'show_default': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'format': 'format',
        'show_default': 'showDefault'
    }

    def __init__(self, id=None, format=None, show_default=False):  # noqa: E501
        """ColumnV2 - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._format = None
        self._show_default = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if format is not None:
            self.format = format
        if show_default is not None:
            self.show_default = show_default

    @property
    def id(self):
        """Gets the id of this ColumnV2.  # noqa: E501


        :return: The id of this ColumnV2.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ColumnV2.


        :param id: The id of this ColumnV2.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def format(self):
        """Gets the format of this ColumnV2.  # noqa: E501


        :return: The format of this ColumnV2.  # noqa: E501
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this ColumnV2.


        :param format: The format of this ColumnV2.  # noqa: E501
        :type: str
        """

        self._format = format

    @property
    def show_default(self):
        """Gets the show_default of this ColumnV2.  # noqa: E501


        :return: The show_default of this ColumnV2.  # noqa: E501
        :rtype: bool
        """
        return self._show_default

    @show_default.setter
    def show_default(self, show_default):
        """Sets the show_default of this ColumnV2.


        :param show_default: The show_default of this ColumnV2.  # noqa: E501
        :type: bool
        """

        self._show_default = show_default

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ColumnV2, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ColumnV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
