# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

from flywheel.models.data_view_name_filter_spec import DataViewNameFilterSpec  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class DataViewAnalysisFilterSpec(object):

    swagger_types = {
        'label': 'DataViewNameFilterSpec',
        'gear_name': 'DataViewNameFilterSpec',
        'gear_version': 'DataViewNameFilterSpec'
    }

    attribute_map = {
        'label': 'label',
        'gear_name': 'gear.name',
        'gear_version': 'gear.version'
    }

    rattribute_map = {
        'label': 'label',
        'gear.name': 'gear_name',
        'gear.version': 'gear_version'
    }

    def __init__(self, label=None, gear_name=None, gear_version=None):  # noqa: E501
        """DataViewAnalysisFilterSpec - a model defined in Swagger"""
        super(DataViewAnalysisFilterSpec, self).__init__()

        self._label = None
        self._gear_name = None
        self._gear_version = None
        self.discriminator = None
        self.alt_discriminator = None

        if label is not None:
            self.label = label
        if gear_name is not None:
            self.gear_name = gear_name
        if gear_version is not None:
            self.gear_version = gear_version

    @property
    def label(self):
        """Gets the label of this DataViewAnalysisFilterSpec.


        :return: The label of this DataViewAnalysisFilterSpec.
        :rtype: DataViewNameFilterSpec
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this DataViewAnalysisFilterSpec.


        :param label: The label of this DataViewAnalysisFilterSpec.  # noqa: E501
        :type: DataViewNameFilterSpec
        """

        self._label = label

    @property
    def gear_name(self):
        """Gets the gear_name of this DataViewAnalysisFilterSpec.


        :return: The gear_name of this DataViewAnalysisFilterSpec.
        :rtype: DataViewNameFilterSpec
        """
        return self._gear_name

    @gear_name.setter
    def gear_name(self, gear_name):
        """Sets the gear_name of this DataViewAnalysisFilterSpec.


        :param gear_name: The gear_name of this DataViewAnalysisFilterSpec.  # noqa: E501
        :type: DataViewNameFilterSpec
        """

        self._gear_name = gear_name

    @property
    def gear_version(self):
        """Gets the gear_version of this DataViewAnalysisFilterSpec.


        :return: The gear_version of this DataViewAnalysisFilterSpec.
        :rtype: DataViewNameFilterSpec
        """
        return self._gear_version

    @gear_version.setter
    def gear_version(self, gear_version):
        """Sets the gear_version of this DataViewAnalysisFilterSpec.


        :param gear_version: The gear_version of this DataViewAnalysisFilterSpec.  # noqa: E501
        :type: DataViewNameFilterSpec
        """

        self._gear_version = gear_version


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DataViewAnalysisFilterSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
