from __future__ import absolute_import

import re  # noqa: F401
import six

from ionoscloud_container_registry.api_client import ApiClient
from ionoscloud_container_registry.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class RegistriesApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def registries_delete(self, registry_id, **kwargs):  # noqa: E501
        """Delete registry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_delete(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_delete_with_http_info(registry_id, **kwargs)  # noqa: E501

    def registries_delete_with_http_info(self, registry_id, **kwargs):  # noqa: E501
        """Delete registry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_delete_with_http_info(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'registry_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_delete" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_delete`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_delete`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = None
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_find_by_id(self, registry_id, **kwargs):  # noqa: E501
        """Get a registry  # noqa: E501

        Get all information for a specific container registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_find_by_id(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: RegistryResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_find_by_id_with_http_info(registry_id, **kwargs)  # noqa: E501

    def registries_find_by_id_with_http_info(self, registry_id, **kwargs):  # noqa: E501
        """Get a registry  # noqa: E501

        Get all information for a specific container registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_find_by_id_with_http_info(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(RegistryResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_find_by_id" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_find_by_id`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_find_by_id`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'RegistryResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_get(self, **kwargs):  # noqa: E501
        """List all container registries  # noqa: E501

        List all managed container registries for your account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_get(async_req=True)
        >>> result = thread.get()

        :param filter_name: The registry name to search for
        :type filter_name: str
        :param limit: The maximum number of elements to return (used together with nextPageToken for pagination)
        :type limit: str
        :param next_page_token: The next page from the complete list of elements (used together with limit for pagination)
        :type next_page_token: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: RegistriesResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_get_with_http_info(**kwargs)  # noqa: E501

    def registries_get_with_http_info(self, **kwargs):  # noqa: E501
        """List all container registries  # noqa: E501

        List all managed container registries for your account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param filter_name: The registry name to search for
        :type filter_name: str
        :param limit: The maximum number of elements to return (used together with nextPageToken for pagination)
        :type limit: str
        :param next_page_token: The next page from the complete list of elements (used together with limit for pagination)
        :type next_page_token: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(RegistriesResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'filter_name',
            'limit',
            'next_page_token'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_get" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = list(local_var_params.get('query_params', {}).items())
        if 'filter_name' in local_var_params and local_var_params['filter_name'] is not None:  # noqa: E501
            query_params.append(('filter.name', local_var_params['filter_name']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'next_page_token' in local_var_params and local_var_params['next_page_token'] is not None:  # noqa: E501
            query_params.append(('nextPageToken', local_var_params['next_page_token']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'RegistriesResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_patch(self, registry_id, patch_registry_input, **kwargs):  # noqa: E501
        """Update the properties of a registry  # noqa: E501

        Update the properties of a registry - \"garbageCollectionSchedule\" time and days of the week for runs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_patch(registry_id, patch_registry_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param patch_registry_input: (required)
        :type patch_registry_input: PatchRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: RegistryResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_patch_with_http_info(registry_id, patch_registry_input, **kwargs)  # noqa: E501

    def registries_patch_with_http_info(self, registry_id, patch_registry_input, **kwargs):  # noqa: E501
        """Update the properties of a registry  # noqa: E501

        Update the properties of a registry - \"garbageCollectionSchedule\" time and days of the week for runs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_patch_with_http_info(registry_id, patch_registry_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param patch_registry_input: (required)
        :type patch_registry_input: PatchRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(RegistryResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'patch_registry_input'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_patch" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_patch`")  # noqa: E501
        # verify the required parameter 'patch_registry_input' is set
        if self.api_client.client_side_validation and ('patch_registry_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['patch_registry_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `patch_registry_input` when calling `registries_patch`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_patch`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'patch_registry_input' in local_var_params:
            body_params = local_var_params['patch_registry_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'RegistryResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_post(self, post_registry_input, **kwargs):  # noqa: E501
        """Create container registry  # noqa: E501

        Create a registry to hold container images or OCI compliant artifacts - \"name\" must have passed validation - \"location\" must be one of the available location IDs - \"garbageCollectionSchedule\" time and days of the week for runs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_post(post_registry_input, async_req=True)
        >>> result = thread.get()

        :param post_registry_input: (required)
        :type post_registry_input: PostRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PostRegistryOutput
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_post_with_http_info(post_registry_input, **kwargs)  # noqa: E501

    def registries_post_with_http_info(self, post_registry_input, **kwargs):  # noqa: E501
        """Create container registry  # noqa: E501

        Create a registry to hold container images or OCI compliant artifacts - \"name\" must have passed validation - \"location\" must be one of the available location IDs - \"garbageCollectionSchedule\" time and days of the week for runs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_post_with_http_info(post_registry_input, async_req=True)
        >>> result = thread.get()

        :param post_registry_input: (required)
        :type post_registry_input: PostRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PostRegistryOutput, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'post_registry_input'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_post" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'post_registry_input' is set
        if self.api_client.client_side_validation and ('post_registry_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['post_registry_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `post_registry_input` when calling `registries_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'post_registry_input' in local_var_params:
            body_params = local_var_params['post_registry_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'PostRegistryOutput'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def registries_put(self, registry_id, put_registry_input, **kwargs):  # noqa: E501
        """Create or replace a container registry  # noqa: E501

        Create/replace a registry to hold container images or OCI compliant artifacts  **On create** - \"name\" must have passed validation - \"location\" must be one of the available location IDs  **On update** - \"name\" cannot be changed - \"location\" cannot be changed  **On create or update** - \"garbageCollectionSchedule\": time and days of the week for runs   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_put(registry_id, put_registry_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param put_registry_input: (required)
        :type put_registry_input: PutRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PutRegistryOutput
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_put_with_http_info(registry_id, put_registry_input, **kwargs)  # noqa: E501

    def registries_put_with_http_info(self, registry_id, put_registry_input, **kwargs):  # noqa: E501
        """Create or replace a container registry  # noqa: E501

        Create/replace a registry to hold container images or OCI compliant artifacts  **On create** - \"name\" must have passed validation - \"location\" must be one of the available location IDs  **On update** - \"name\" cannot be changed - \"location\" cannot be changed  **On create or update** - \"garbageCollectionSchedule\": time and days of the week for runs   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_put_with_http_info(registry_id, put_registry_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param put_registry_input: (required)
        :type put_registry_input: PutRegistryInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(PutRegistryOutput, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'put_registry_input'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method registries_put" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_put`")  # noqa: E501
        # verify the required parameter 'put_registry_input' is set
        if self.api_client.client_side_validation and ('put_registry_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['put_registry_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `put_registry_input` when calling `registries_put`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_put`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'put_registry_input' in local_var_params:
            body_params = local_var_params['put_registry_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'PutRegistryOutput'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
