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
import json
import threading
from urlparse import urlparse
from mashape.auth.header_auth import HeaderAuth
from mashape.auth.query_auth import QueryAuth
from mashape.http.url_utils import UrlUtils
from mashape.http.mashape_response import MashapeResponse 
from mashape.http.multipart_post_handler import MultipartPostHandler
from mashape.http.content_type import ContentType 
from mashape.exception.client_exception import MashapeClientException


class HttpClient:
    def do_call(self, http_method, url, parameters, auth_handlers, content_type, callback=None, parse_json=True):

        # for asynchronous calls
        if(callback is not None):
            def thread_function(http_method, url, parameters, auth_handlers, content_type, parse_json):
                result = self._do_call(http_method, url, parameters, auth_handlers, parse_json)
                callback(result)
            thread = threading.Thread(target=thread_function, args=(http_method, url, parameters, auth_handlers, content_type, parse_json))
            thread.start()
            return thread
        else:
            return self._do_call(http_method, url, parameters, auth_handlers, content_type, parse_json)

    def _do_call(self, http_method, url, parameters, auth_handlers, content_type, parse_json):
        if parameters is None:
            parameters = {}
        else:
            for key in parameters.keys():
                if parameters[key] is None:
                    parameters.pop(key)

        headers = {}
        if parse_json:
            headers["Accept"] = "application/json"

        headers.update(UrlUtils.generate_client_headers())

        for handler in auth_handlers:
            if isinstance(handler, HeaderAuth):
                headers.update(handler.handleHeader())
            if isinstance(handler, QueryAuth):
                parameters.update(handler.handleParams())

        parsedQuery = urlparse(url).query
        # get all the constant query parameters and add them to the parameters dict 
        parameters.update(UrlUtils.get_query_string_parameters(parsedQuery))
        # get rid of all the placeholder url parameters
        url = UrlUtils.replace_base_url_parameters(url, parameters)


        if content_type is ContentType.MULTIPART:
            params = parameters
            opener = urllib2.build_opener(MultipartPostHandler)
        else:
            headers["Content-type"] = "application/x-www-form-urlencoded";
            opener = urllib2.build_opener(urllib2.HTTPHandler)

            # If we still have parameters, it means that they were part of the url
            # but not placeholders. We need to add them back to the url.
            params = urllib.urlencode(parameters)
            if len(params) != 0:
                qpos = url.find("?")
                if (http_method == "GET") or parsedQuery is not None:
                    if (qpos > 0):
                        url += "&" + params
                    else:
                        url += "?" + params
                
                if (http_method == "GET"):
                    params = None

        request = urllib2.Request(url, params, headers)
        request.get_method = lambda: http_method
        try:
            response = opener.open(request)
        except urllib2.HTTPError, e:
            if e.getcode() == 500:
                response = e
            else:
                import sys
                raise MashapeClientException("Error executing the request "
                    + str(sys.exc_info()[1]))

        return MashapeResponse(response, parse_json)
