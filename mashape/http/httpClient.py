#
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
#++

import urllib
import httplib
import json
from urlparse import urlparse
from mashape.config.init import ModuleInfo

class HttpClient:
	METHOD = "_method"
	TOKEN = "_token"
	LANGUAGE = "_language"
	VERSION = "_version"

	def doCall(self, baseUrl, httpMethod, method, token, parameters):
		if parameters == None:
			parameters = {};
		
		parameters[self.METHOD] = method
		parameters[self.TOKEN] = token
		parameters[self.LANGUAGE] = ModuleInfo.CLIENT_LIBRARY_LANGUAGE;
		parameters[self.VERSION] = ModuleInfo.CLIENT_LIBRARY_VERSION;
		params = urllib.urlencode(parameters)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		parsedUrl = urlparse(baseUrl)
		conn = httplib.HTTPConnection(parsedUrl.hostname, parsedUrl.port)
		try:
			url = "/" + parsedUrl.path
			if (httpMethod == "GET") and (len(params) > 1):
				url += "?" + params
			conn.request(httpMethod, url, params, headers)
			response = conn.getresponse()
			responseValue = response.read()
			conn.close()
		except:
			responseValue = None
		responseJson = None
		if responseValue != None:
			responseJson = json.loads(responseValue)
		return responseJson
		
