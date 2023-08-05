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


class ClickwrapTransferRequest(object):
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
        'transfer_from_user_id': 'str',
        'transfer_to_user_id': 'str'
    }

    attribute_map = {
        'transfer_from_user_id': 'transferFromUserId',
        'transfer_to_user_id': 'transferToUserId'
    }

    def __init__(self, _configuration=None, **kwargs):  # noqa: E501
        """ClickwrapTransferRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._transfer_from_user_id = None
        self._transfer_to_user_id = None
        self.discriminator = None

        setattr(self, "_{}".format('transfer_from_user_id'), kwargs.get('transfer_from_user_id', None))
        setattr(self, "_{}".format('transfer_to_user_id'), kwargs.get('transfer_to_user_id', None))

    @property
    def transfer_from_user_id(self):
        """Gets the transfer_from_user_id of this ClickwrapTransferRequest.  # noqa: E501

          # noqa: E501

        :return: The transfer_from_user_id of this ClickwrapTransferRequest.  # noqa: E501
        :rtype: str
        """
        return self._transfer_from_user_id

    @transfer_from_user_id.setter
    def transfer_from_user_id(self, transfer_from_user_id):
        """Sets the transfer_from_user_id of this ClickwrapTransferRequest.

          # noqa: E501

        :param transfer_from_user_id: The transfer_from_user_id of this ClickwrapTransferRequest.  # noqa: E501
        :type: str
        """

        self._transfer_from_user_id = transfer_from_user_id

    @property
    def transfer_to_user_id(self):
        """Gets the transfer_to_user_id of this ClickwrapTransferRequest.  # noqa: E501

          # noqa: E501

        :return: The transfer_to_user_id of this ClickwrapTransferRequest.  # noqa: E501
        :rtype: str
        """
        return self._transfer_to_user_id

    @transfer_to_user_id.setter
    def transfer_to_user_id(self, transfer_to_user_id):
        """Sets the transfer_to_user_id of this ClickwrapTransferRequest.

          # noqa: E501

        :param transfer_to_user_id: The transfer_to_user_id of this ClickwrapTransferRequest.  # noqa: E501
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
        if issubclass(ClickwrapTransferRequest, dict):
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
        if not isinstance(other, ClickwrapTransferRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClickwrapTransferRequest):
            return True

        return self.to_dict() != other.to_dict()
