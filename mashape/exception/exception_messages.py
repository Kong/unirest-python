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


class ExceptionMessages(object):
    EXCEPTION_NOTSUPPORTED_HTTPMETHOD_CODE = 1003
    EXCEPTION_NOTSUPPORTED_HTTPMETHOD = "HTTP method not supported. Only \
            DELETE, GET, POST, PUT are supported"

    EXCEPTION_OAUTH1_AUTHORIZE_CODE = 1007
    EXCEPTION_OAUTH1_AUTHORIZE = "Before consuming an OAuth endpoint, you \
            must invoke the authorize('access_token', 'access_secret') \
            function with non-null values"

    EXCEPTION_OAUTH2_AUTHORIZE_CODE = 1008
    EXCEPTION_OAUTH2_AUTHORIZE = "Before consuming an OAuth endpoint, you \
            must invoke the authorize('access_token') function with a \
            non-null value"

    EXCEPTION_SYSTEM_ERROR_CODE = 2000
    EXCEPTION_EMPTY_REQUEST = "A request attempt was made to the component, \
            but the response was empty. The component's URL may be wrong or \
            the firewall may be blocking your outbound HTTP requests"
    EXCEPTION_INVALID_REQUEST = "The component returned an invalid response"
