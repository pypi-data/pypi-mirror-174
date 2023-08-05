# coding: utf-8

"""
    DocuSign Click API

    DocuSign Click lets you capture consent to standard agreement terms with a single click: terms and conditions, terms of service, terms of use, privacy policies, and more. The Click API lets you include this customizable clickwrap solution in your DocuSign integrations.  # noqa: E501

    OpenAPI spec version: v1
    Contact: devcenter@docusign.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from docusign_click.client.configuration import Configuration


class ClickwrapRequest(object):
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
        'clickwrap_name': 'str',
        'data_fields': 'list[DataField]',
        'display_settings': 'DisplaySettings',
        'documents': 'list[Document]',
        'fields_to_null': 'str',
        'is_major_version': 'bool',
        'is_shared': 'bool',
        'name': 'str',
        'require_reacceptance': 'bool',
        'scheduled_date': 'object',
        'scheduled_reacceptance': 'ClickwrapScheduledReacceptance',
        'status': 'str',
        'transfer_from_user_id': 'str',
        'transfer_to_user_id': 'str'
    }

    attribute_map = {
        'clickwrap_name': 'clickwrapName',
        'data_fields': 'dataFields',
        'display_settings': 'displaySettings',
        'documents': 'documents',
        'fields_to_null': 'fieldsToNull',
        'is_major_version': 'isMajorVersion',
        'is_shared': 'isShared',
        'name': 'name',
        'require_reacceptance': 'requireReacceptance',
        'scheduled_date': 'scheduledDate',
        'scheduled_reacceptance': 'scheduledReacceptance',
        'status': 'status',
        'transfer_from_user_id': 'transferFromUserId',
        'transfer_to_user_id': 'transferToUserId'
    }

    def __init__(self, _configuration=None, **kwargs):  # noqa: E501
        """ClickwrapRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._clickwrap_name = None
        self._data_fields = None
        self._display_settings = None
        self._documents = None
        self._fields_to_null = None
        self._is_major_version = None
        self._is_shared = None
        self._name = None
        self._require_reacceptance = None
        self._scheduled_date = None
        self._scheduled_reacceptance = None
        self._status = None
        self._transfer_from_user_id = None
        self._transfer_to_user_id = None
        self.discriminator = None

        setattr(self, "_{}".format('clickwrap_name'), kwargs.get('clickwrap_name', None))
        setattr(self, "_{}".format('data_fields'), kwargs.get('data_fields', None))
        setattr(self, "_{}".format('display_settings'), kwargs.get('display_settings', None))
        setattr(self, "_{}".format('documents'), kwargs.get('documents', None))
        setattr(self, "_{}".format('fields_to_null'), kwargs.get('fields_to_null', None))
        setattr(self, "_{}".format('is_major_version'), kwargs.get('is_major_version', None))
        setattr(self, "_{}".format('is_shared'), kwargs.get('is_shared', None))
        setattr(self, "_{}".format('name'), kwargs.get('name', None))
        setattr(self, "_{}".format('require_reacceptance'), kwargs.get('require_reacceptance', None))
        setattr(self, "_{}".format('scheduled_date'), kwargs.get('scheduled_date', None))
        setattr(self, "_{}".format('scheduled_reacceptance'), kwargs.get('scheduled_reacceptance', None))
        setattr(self, "_{}".format('status'), kwargs.get('status', None))
        setattr(self, "_{}".format('transfer_from_user_id'), kwargs.get('transfer_from_user_id', None))
        setattr(self, "_{}".format('transfer_to_user_id'), kwargs.get('transfer_to_user_id', None))

    @property
    def clickwrap_name(self):
        """Gets the clickwrap_name of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The clickwrap_name of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._clickwrap_name

    @clickwrap_name.setter
    def clickwrap_name(self, clickwrap_name):
        """Sets the clickwrap_name of this ClickwrapRequest.

          # noqa: E501

        :param clickwrap_name: The clickwrap_name of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._clickwrap_name = clickwrap_name

    @property
    def data_fields(self):
        """Gets the data_fields of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The data_fields of this ClickwrapRequest.  # noqa: E501
        :rtype: list[DataField]
        """
        return self._data_fields

    @data_fields.setter
    def data_fields(self, data_fields):
        """Sets the data_fields of this ClickwrapRequest.

          # noqa: E501

        :param data_fields: The data_fields of this ClickwrapRequest.  # noqa: E501
        :type: list[DataField]
        """

        self._data_fields = data_fields

    @property
    def display_settings(self):
        """Gets the display_settings of this ClickwrapRequest.  # noqa: E501


        :return: The display_settings of this ClickwrapRequest.  # noqa: E501
        :rtype: DisplaySettings
        """
        return self._display_settings

    @display_settings.setter
    def display_settings(self, display_settings):
        """Sets the display_settings of this ClickwrapRequest.


        :param display_settings: The display_settings of this ClickwrapRequest.  # noqa: E501
        :type: DisplaySettings
        """

        self._display_settings = display_settings

    @property
    def documents(self):
        """Gets the documents of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The documents of this ClickwrapRequest.  # noqa: E501
        :rtype: list[Document]
        """
        return self._documents

    @documents.setter
    def documents(self, documents):
        """Sets the documents of this ClickwrapRequest.

          # noqa: E501

        :param documents: The documents of this ClickwrapRequest.  # noqa: E501
        :type: list[Document]
        """

        self._documents = documents

    @property
    def fields_to_null(self):
        """Gets the fields_to_null of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The fields_to_null of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._fields_to_null

    @fields_to_null.setter
    def fields_to_null(self, fields_to_null):
        """Sets the fields_to_null of this ClickwrapRequest.

          # noqa: E501

        :param fields_to_null: The fields_to_null of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._fields_to_null = fields_to_null

    @property
    def is_major_version(self):
        """Gets the is_major_version of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The is_major_version of this ClickwrapRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_major_version

    @is_major_version.setter
    def is_major_version(self, is_major_version):
        """Sets the is_major_version of this ClickwrapRequest.

          # noqa: E501

        :param is_major_version: The is_major_version of this ClickwrapRequest.  # noqa: E501
        :type: bool
        """

        self._is_major_version = is_major_version

    @property
    def is_shared(self):
        """Gets the is_shared of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The is_shared of this ClickwrapRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_shared

    @is_shared.setter
    def is_shared(self, is_shared):
        """Sets the is_shared of this ClickwrapRequest.

          # noqa: E501

        :param is_shared: The is_shared of this ClickwrapRequest.  # noqa: E501
        :type: bool
        """

        self._is_shared = is_shared

    @property
    def name(self):
        """Gets the name of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The name of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ClickwrapRequest.

          # noqa: E501

        :param name: The name of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def require_reacceptance(self):
        """Gets the require_reacceptance of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The require_reacceptance of this ClickwrapRequest.  # noqa: E501
        :rtype: bool
        """
        return self._require_reacceptance

    @require_reacceptance.setter
    def require_reacceptance(self, require_reacceptance):
        """Sets the require_reacceptance of this ClickwrapRequest.

          # noqa: E501

        :param require_reacceptance: The require_reacceptance of this ClickwrapRequest.  # noqa: E501
        :type: bool
        """

        self._require_reacceptance = require_reacceptance

    @property
    def scheduled_date(self):
        """Gets the scheduled_date of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The scheduled_date of this ClickwrapRequest.  # noqa: E501
        :rtype: object
        """
        return self._scheduled_date

    @scheduled_date.setter
    def scheduled_date(self, scheduled_date):
        """Sets the scheduled_date of this ClickwrapRequest.

          # noqa: E501

        :param scheduled_date: The scheduled_date of this ClickwrapRequest.  # noqa: E501
        :type: object
        """

        self._scheduled_date = scheduled_date

    @property
    def scheduled_reacceptance(self):
        """Gets the scheduled_reacceptance of this ClickwrapRequest.  # noqa: E501


        :return: The scheduled_reacceptance of this ClickwrapRequest.  # noqa: E501
        :rtype: ClickwrapScheduledReacceptance
        """
        return self._scheduled_reacceptance

    @scheduled_reacceptance.setter
    def scheduled_reacceptance(self, scheduled_reacceptance):
        """Sets the scheduled_reacceptance of this ClickwrapRequest.


        :param scheduled_reacceptance: The scheduled_reacceptance of this ClickwrapRequest.  # noqa: E501
        :type: ClickwrapScheduledReacceptance
        """

        self._scheduled_reacceptance = scheduled_reacceptance

    @property
    def status(self):
        """Gets the status of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The status of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ClickwrapRequest.

          # noqa: E501

        :param status: The status of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def transfer_from_user_id(self):
        """Gets the transfer_from_user_id of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The transfer_from_user_id of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._transfer_from_user_id

    @transfer_from_user_id.setter
    def transfer_from_user_id(self, transfer_from_user_id):
        """Sets the transfer_from_user_id of this ClickwrapRequest.

          # noqa: E501

        :param transfer_from_user_id: The transfer_from_user_id of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._transfer_from_user_id = transfer_from_user_id

    @property
    def transfer_to_user_id(self):
        """Gets the transfer_to_user_id of this ClickwrapRequest.  # noqa: E501

          # noqa: E501

        :return: The transfer_to_user_id of this ClickwrapRequest.  # noqa: E501
        :rtype: str
        """
        return self._transfer_to_user_id

    @transfer_to_user_id.setter
    def transfer_to_user_id(self, transfer_to_user_id):
        """Sets the transfer_to_user_id of this ClickwrapRequest.

          # noqa: E501

        :param transfer_to_user_id: The transfer_to_user_id of this ClickwrapRequest.  # noqa: E501
        :type: str
        """

        self._transfer_to_user_id = transfer_to_user_id

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
        if issubclass(ClickwrapRequest, dict):
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
        if not isinstance(other, ClickwrapRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClickwrapRequest):
            return True

        return self.to_dict() != other.to_dict()
