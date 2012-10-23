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

import urllib2
import threading
#from urlparse import urlparse
from mashape.http.url_utils import UrlUtils
from mashape.http.http_utils import HttpUtils
from mashape.http.mashape_response import MashapeResponse
from mashape.exception.client_exception import MashapeClientException


class HttpClient:
    def do_call(self, http_method, url, parameters, auth_handlers,
            content_type, callback=None, parse_json=True):

        parameters = HttpUtils.clean_parameters(parameters)

        # for asynchronous calls
        if(callback is not None):
            return self._async_call(http_method, url, parameters,
                    auth_handlers, content_type, parse_json, callback)
        else:
            return self._do_call(http_method, url, parameters,
                    auth_handlers, content_type, parse_json)

    def _async_call(self, http_method, url, parameters, auth_handlers,
            content_type, parse_json, callback):
        def thread_function(http_method, url, parameters, auth_handlers,
                content_type, parse_json):
            result = self._do_call(http_method, url, parameters, auth_handlers,
                    parse_json)
            callback(result)
        thread = threading.Thread(target=thread_function, args=(http_method,
            url, parameters, auth_handlers, content_type, parse_json))
        thread.start()
        return thread

    def _do_call(self, http_method, url, parameters, auth_handlers,
            content_type, parse_json):

        headers, auth_params = HttpUtils.handle_authentication(auth_handlers, url)
        parameters.update(auth_params)
        if parse_json:
            headers["Accept"] = "application/json"

        headers.update(UrlUtils.generate_client_headers())

        data = None
        opener = HttpUtils.get_http_opener(content_type)
        if (http_method == "GET"):
            url = UrlUtils.build_url_with_query_string(url, parameters)
        else:
            data, additional_headers = HttpUtils.build_data_for_content_type(
                    content_type, parameters, headers)
            headers.update(additional_headers)

        request = urllib2.Request(url, data, headers)
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
