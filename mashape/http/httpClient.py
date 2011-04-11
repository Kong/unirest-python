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

	def doCall(self, url, httpMethod, token, parameters):
		if parameters == None:
			parameters = {};
		else:
			for key in parameters.keys():
				if parameters[key] == None:
					parameters.pop(key)
		
		parameters[ModuleInfo.TOKEN] = token
		parameters[ModuleInfo.LANGUAGE] = ModuleInfo.CLIENT_LIBRARY_LANGUAGE;
		parameters[ModuleInfo.VERSION] = ModuleInfo.CLIENT_LIBRARY_VERSION;
		

		params = urllib.urlencode(parameters)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		parsedUrl = urlparse(url)

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
		
