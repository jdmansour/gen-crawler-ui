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


class Login(object):
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
        'remote_authentications': 'dict(str, RemoteAuthDescription)',
        'is_valid_login': 'bool',
        'is_admin': 'bool',
        'current_scope': 'str',
        'user_home': 'str',
        'session_timeout': 'int',
        'tool_permissions': 'list[str]',
        'status_code': 'str',
        'authority_name': 'str',
        'is_guest': 'bool'
    }

    attribute_map = {
        'remote_authentications': 'remoteAuthentications',
        'is_valid_login': 'isValidLogin',
        'is_admin': 'isAdmin',
        'current_scope': 'currentScope',
        'user_home': 'userHome',
        'session_timeout': 'sessionTimeout',
        'tool_permissions': 'toolPermissions',
        'status_code': 'statusCode',
        'authority_name': 'authorityName',
        'is_guest': 'isGuest'
    }

    def __init__(self, remote_authentications=None, is_valid_login=False, is_admin=False, current_scope=None, user_home=None, session_timeout=None, tool_permissions=None, status_code=None, authority_name=None, is_guest=False):  # noqa: E501
        """Login - a model defined in Swagger"""  # noqa: E501
        self._remote_authentications = None
        self._is_valid_login = None
        self._is_admin = None
        self._current_scope = None
        self._user_home = None
        self._session_timeout = None
        self._tool_permissions = None
        self._status_code = None
        self._authority_name = None
        self._is_guest = None
        self.discriminator = None
        if remote_authentications is not None:
            self.remote_authentications = remote_authentications
        self.is_valid_login = is_valid_login
        self.is_admin = is_admin
        self.current_scope = current_scope
        if user_home is not None:
            self.user_home = user_home
        self.session_timeout = session_timeout
        if tool_permissions is not None:
            self.tool_permissions = tool_permissions
        if status_code is not None:
            self.status_code = status_code
        if authority_name is not None:
            self.authority_name = authority_name
        self.is_guest = is_guest

    @property
    def remote_authentications(self):
        """Gets the remote_authentications of this Login.  # noqa: E501


        :return: The remote_authentications of this Login.  # noqa: E501
        :rtype: dict(str, RemoteAuthDescription)
        """
        return self._remote_authentications

    @remote_authentications.setter
    def remote_authentications(self, remote_authentications):
        """Sets the remote_authentications of this Login.


        :param remote_authentications: The remote_authentications of this Login.  # noqa: E501
        :type: dict(str, RemoteAuthDescription)
        """

        self._remote_authentications = remote_authentications

    @property
    def is_valid_login(self):
        """Gets the is_valid_login of this Login.  # noqa: E501


        :return: The is_valid_login of this Login.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid_login

    @is_valid_login.setter
    def is_valid_login(self, is_valid_login):
        """Sets the is_valid_login of this Login.


        :param is_valid_login: The is_valid_login of this Login.  # noqa: E501
        :type: bool
        """
        if is_valid_login is None:
            raise ValueError("Invalid value for `is_valid_login`, must not be `None`")  # noqa: E501

        self._is_valid_login = is_valid_login

    @property
    def is_admin(self):
        """Gets the is_admin of this Login.  # noqa: E501


        :return: The is_admin of this Login.  # noqa: E501
        :rtype: bool
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        """Sets the is_admin of this Login.


        :param is_admin: The is_admin of this Login.  # noqa: E501
        :type: bool
        """
        if is_admin is None:
            raise ValueError("Invalid value for `is_admin`, must not be `None`")  # noqa: E501

        self._is_admin = is_admin

    @property
    def current_scope(self):
        """Gets the current_scope of this Login.  # noqa: E501


        :return: The current_scope of this Login.  # noqa: E501
        :rtype: str
        """
        return self._current_scope

    @current_scope.setter
    def current_scope(self, current_scope):
        """Sets the current_scope of this Login.


        :param current_scope: The current_scope of this Login.  # noqa: E501
        :type: str
        """
        if current_scope is None:
            raise ValueError("Invalid value for `current_scope`, must not be `None`")  # noqa: E501

        self._current_scope = current_scope

    @property
    def user_home(self):
        """Gets the user_home of this Login.  # noqa: E501


        :return: The user_home of this Login.  # noqa: E501
        :rtype: str
        """
        return self._user_home

    @user_home.setter
    def user_home(self, user_home):
        """Sets the user_home of this Login.


        :param user_home: The user_home of this Login.  # noqa: E501
        :type: str
        """

        self._user_home = user_home

    @property
    def session_timeout(self):
        """Gets the session_timeout of this Login.  # noqa: E501


        :return: The session_timeout of this Login.  # noqa: E501
        :rtype: int
        """
        return self._session_timeout

    @session_timeout.setter
    def session_timeout(self, session_timeout):
        """Sets the session_timeout of this Login.


        :param session_timeout: The session_timeout of this Login.  # noqa: E501
        :type: int
        """
        if session_timeout is None:
            raise ValueError("Invalid value for `session_timeout`, must not be `None`")  # noqa: E501

        self._session_timeout = session_timeout

    @property
    def tool_permissions(self):
        """Gets the tool_permissions of this Login.  # noqa: E501


        :return: The tool_permissions of this Login.  # noqa: E501
        :rtype: list[str]
        """
        return self._tool_permissions

    @tool_permissions.setter
    def tool_permissions(self, tool_permissions):
        """Sets the tool_permissions of this Login.


        :param tool_permissions: The tool_permissions of this Login.  # noqa: E501
        :type: list[str]
        """

        self._tool_permissions = tool_permissions

    @property
    def status_code(self):
        """Gets the status_code of this Login.  # noqa: E501


        :return: The status_code of this Login.  # noqa: E501
        :rtype: str
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """Sets the status_code of this Login.


        :param status_code: The status_code of this Login.  # noqa: E501
        :type: str
        """

        self._status_code = status_code

    @property
    def authority_name(self):
        """Gets the authority_name of this Login.  # noqa: E501


        :return: The authority_name of this Login.  # noqa: E501
        :rtype: str
        """
        return self._authority_name

    @authority_name.setter
    def authority_name(self, authority_name):
        """Sets the authority_name of this Login.


        :param authority_name: The authority_name of this Login.  # noqa: E501
        :type: str
        """

        self._authority_name = authority_name

    @property
    def is_guest(self):
        """Gets the is_guest of this Login.  # noqa: E501


        :return: The is_guest of this Login.  # noqa: E501
        :rtype: bool
        """
        return self._is_guest

    @is_guest.setter
    def is_guest(self, is_guest):
        """Sets the is_guest of this Login.


        :param is_guest: The is_guest of this Login.  # noqa: E501
        :type: bool
        """
        if is_guest is None:
            raise ValueError("Invalid value for `is_guest`, must not be `None`")  # noqa: E501

        self._is_guest = is_guest

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
        if issubclass(Login, dict):
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
        if not isinstance(other, Login):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
