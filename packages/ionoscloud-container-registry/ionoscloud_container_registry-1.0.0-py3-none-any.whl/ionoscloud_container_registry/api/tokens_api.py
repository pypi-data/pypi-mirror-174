from __future__ import absolute_import

import re  # noqa: F401
import six

from ionoscloud_container_registry.api_client import ApiClient
from ionoscloud_container_registry.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class TokensApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def registries_tokens_delete(self, registry_id, token_id, **kwargs):  # noqa: E501
        """Delete token  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_delete(registry_id, token_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
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
        return self.registries_tokens_delete_with_http_info(registry_id, token_id, **kwargs)  # noqa: E501

    def registries_tokens_delete_with_http_info(self, registry_id, token_id, **kwargs):  # noqa: E501
        """Delete token  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_delete_with_http_info(registry_id, token_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
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
            'registry_id',
            'token_id'
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
                    " to method registries_tokens_delete" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_delete`")  # noqa: E501
        # verify the required parameter 'token_id' is set
        if self.api_client.client_side_validation and ('token_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_id` when calling `registries_tokens_delete`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_delete`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'token_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['token_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `token_id` when calling `registries_tokens_delete`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'token_id' in local_var_params:
            path_params['tokenId'] = local_var_params['token_id']  # noqa: E501

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
            '/registries/{registryId}/tokens/{tokenId}', 'DELETE',
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

    def registries_tokens_find_by_id(self, registry_id, token_id, **kwargs):  # noqa: E501
        """Get token information  # noqa: E501

        Gets all information for a specific token used to access a container registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_find_by_id(registry_id, token_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
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
        :rtype: TokenResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_tokens_find_by_id_with_http_info(registry_id, token_id, **kwargs)  # noqa: E501

    def registries_tokens_find_by_id_with_http_info(self, registry_id, token_id, **kwargs):  # noqa: E501
        """Get token information  # noqa: E501

        Gets all information for a specific token used to access a container registry  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_find_by_id_with_http_info(registry_id, token_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
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
        :rtype: tuple(TokenResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'token_id'
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
                    " to method registries_tokens_find_by_id" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_find_by_id`")  # noqa: E501
        # verify the required parameter 'token_id' is set
        if self.api_client.client_side_validation and ('token_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_id` when calling `registries_tokens_find_by_id`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_find_by_id`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'token_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['token_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `token_id` when calling `registries_tokens_find_by_id`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'token_id' in local_var_params:
            path_params['tokenId'] = local_var_params['token_id']  # noqa: E501

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

        response_type = 'TokenResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/tokens/{tokenId}', 'GET',
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

    def registries_tokens_get(self, registry_id, **kwargs):  # noqa: E501
        """List all tokens for the container registry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_get(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param offset: The first element (from the complete list of the elements) to include in the response (used together with limit for pagination)
        :type offset: str
        :param limit: The maximum number of elements to return (used together with offset for pagination)
        :type limit: str
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
        :rtype: TokensResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_tokens_get_with_http_info(registry_id, **kwargs)  # noqa: E501

    def registries_tokens_get_with_http_info(self, registry_id, **kwargs):  # noqa: E501
        """List all tokens for the container registry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_get_with_http_info(registry_id, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param offset: The first element (from the complete list of the elements) to include in the response (used together with limit for pagination)
        :type offset: str
        :param limit: The maximum number of elements to return (used together with offset for pagination)
        :type limit: str
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
        :rtype: tuple(TokensResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'offset',
            'limit'
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
                    " to method registries_tokens_get" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_get`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_get`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())
        if 'offset' in local_var_params and local_var_params['offset'] is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'TokensResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/tokens', 'GET',
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

    def registries_tokens_patch(self, registry_id, token_id, patch_token_input, **kwargs):  # noqa: E501
        """Update token  # noqa: E501

        Update token properties, for example: - change status to 'enabled' or 'disabled' - change expiry date  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_patch(registry_id, token_id, patch_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
        :param patch_token_input: (required)
        :type patch_token_input: PatchTokenInput
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
        :rtype: TokenResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_tokens_patch_with_http_info(registry_id, token_id, patch_token_input, **kwargs)  # noqa: E501

    def registries_tokens_patch_with_http_info(self, registry_id, token_id, patch_token_input, **kwargs):  # noqa: E501
        """Update token  # noqa: E501

        Update token properties, for example: - change status to 'enabled' or 'disabled' - change expiry date  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_patch_with_http_info(registry_id, token_id, patch_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
        :param patch_token_input: (required)
        :type patch_token_input: PatchTokenInput
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
        :rtype: tuple(TokenResponse, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'token_id',
            'patch_token_input'
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
                    " to method registries_tokens_patch" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_patch`")  # noqa: E501
        # verify the required parameter 'token_id' is set
        if self.api_client.client_side_validation and ('token_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_id` when calling `registries_tokens_patch`")  # noqa: E501
        # verify the required parameter 'patch_token_input' is set
        if self.api_client.client_side_validation and ('patch_token_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['patch_token_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `patch_token_input` when calling `registries_tokens_patch`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_patch`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'token_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['token_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `token_id` when calling `registries_tokens_patch`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'token_id' in local_var_params:
            path_params['tokenId'] = local_var_params['token_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'patch_token_input' in local_var_params:
            body_params = local_var_params['patch_token_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'TokenResponse'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/tokens/{tokenId}', 'PATCH',
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

    def registries_tokens_post(self, registry_id, post_token_input, **kwargs):  # noqa: E501
        """Create token  # noqa: E501

        Create a token - password is only available once in the POST response  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_post(registry_id, post_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param post_token_input: (required)
        :type post_token_input: PostTokenInput
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
        :rtype: PostTokenOutput
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_tokens_post_with_http_info(registry_id, post_token_input, **kwargs)  # noqa: E501

    def registries_tokens_post_with_http_info(self, registry_id, post_token_input, **kwargs):  # noqa: E501
        """Create token  # noqa: E501

        Create a token - password is only available once in the POST response  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_post_with_http_info(registry_id, post_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param post_token_input: (required)
        :type post_token_input: PostTokenInput
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
        :rtype: tuple(PostTokenOutput, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'post_token_input'
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
                    " to method registries_tokens_post" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_post`")  # noqa: E501
        # verify the required parameter 'post_token_input' is set
        if self.api_client.client_side_validation and ('post_token_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['post_token_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `post_token_input` when calling `registries_tokens_post`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_post`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'post_token_input' in local_var_params:
            body_params = local_var_params['post_token_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'PostTokenOutput'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/tokens', 'POST',
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

    def registries_tokens_put(self, registry_id, token_id, put_token_input, **kwargs):  # noqa: E501
        """Create or replace token  # noqa: E501

        Create/replace a token - password is only available once in the create response - \"name\" cannot be changed  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_put(registry_id, token_id, put_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
        :param put_token_input: (required)
        :type put_token_input: PutTokenInput
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
        :rtype: PutTokenOutput
        """
        kwargs['_return_http_data_only'] = True
        return self.registries_tokens_put_with_http_info(registry_id, token_id, put_token_input, **kwargs)  # noqa: E501

    def registries_tokens_put_with_http_info(self, registry_id, token_id, put_token_input, **kwargs):  # noqa: E501
        """Create or replace token  # noqa: E501

        Create/replace a token - password is only available once in the create response - \"name\" cannot be changed  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.registries_tokens_put_with_http_info(registry_id, token_id, put_token_input, async_req=True)
        >>> result = thread.get()

        :param registry_id: The unique ID of the registry (required)
        :type registry_id: str
        :param token_id: The unique ID of the token (required)
        :type token_id: str
        :param put_token_input: (required)
        :type put_token_input: PutTokenInput
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
        :rtype: tuple(PutTokenOutput, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'registry_id',
            'token_id',
            'put_token_input'
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
                    " to method registries_tokens_put" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'registry_id' is set
        if self.api_client.client_side_validation and ('registry_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['registry_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `registry_id` when calling `registries_tokens_put`")  # noqa: E501
        # verify the required parameter 'token_id' is set
        if self.api_client.client_side_validation and ('token_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['token_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `token_id` when calling `registries_tokens_put`")  # noqa: E501
        # verify the required parameter 'put_token_input' is set
        if self.api_client.client_side_validation and ('put_token_input' not in local_var_params or  # noqa: E501
                                                        local_var_params['put_token_input'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `put_token_input` when calling `registries_tokens_put`")  # noqa: E501

        if self.api_client.client_side_validation and 'registry_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['registry_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `registry_id` when calling `registries_tokens_put`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'token_id' in local_var_params and not re.search(r'^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', local_var_params['token_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `token_id` when calling `registries_tokens_put`, must conform to the pattern `/^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'registry_id' in local_var_params:
            path_params['registryId'] = local_var_params['registry_id']  # noqa: E501
        if 'token_id' in local_var_params:
            path_params['tokenId'] = local_var_params['token_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'put_token_input' in local_var_params:
            body_params = local_var_params['put_token_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'PutTokenOutput'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/registries/{registryId}/tokens/{tokenId}', 'PUT',
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
