#
# Mashape Python Client library.
# Copyright (C) 2011 Mashape, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# The author of this software is Mashape, Inc.
# For any question or feedback please contact us at: support@mashape.com
#
import urllib
import urllib2
from mashape.auth.header_auth import HeaderAuth
from mashape.auth.query_auth import QueryAuth
from mashape.auth.oauth10a_auth import OAuth10aAuth
from mashape.auth.oauth2_auth import OAuth2Auth
from mashape.http.content_type import ContentType
from mashape.http.multipart_post_handler import MultipartPostHandler


class HttpUtils:

    @staticmethod
    def clean_parameters(parameters):
        if parameters is None:
            parameters = {}
        else:
            for key in parameters.keys():
                if parameters[key] is None:
                    parameters.pop(key)
        return parameters

    @staticmethod
    def handle_authentication(auth_handlers, url):
        headers = {}
        parameters = {}
        for handler in auth_handlers:
            if isinstance(handler, HeaderAuth):
                headers.update(handler.handle_headers())
            elif isinstance(handler, QueryAuth):
                parameters.update(handler.handle_params())
            elif isinstance(handler, OAuth10aAuth):
                headers.update(handler.handle_headers(url))
            elif isinstance(handler, OAuth2Auth):
                parameters.update(handler.handle_params(url))

        return headers, parameters

    @staticmethod
    def get_http_opener(content_type):
        if content_type is ContentType.MULTIPART:
            opener = urllib2.build_opener(MultipartPostHandler)
        else:
            opener = urllib2.build_opener(MultipartPostHandler)
        return opener

    @staticmethod
    def build_data_for_content_type(content_type, parameters, headers):
        headers = {}
        if content_type is ContentType.MULTIPART:
            data = parameters
        elif content_type is ContentType.JSON:
            headers["Content-type"] = "application/json"
            data = parameters
        else:
            headers["Content-type"] = "application/x-www-form-urlencoded"
            data = urllib.urlencode(parameters)
        return data, headers
