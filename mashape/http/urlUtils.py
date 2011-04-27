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
from mashape.config.init import ModuleInfo

import re

class UrlUtils:
	
	@staticmethod
	def removeQueryString(url):
		return url.split("?")[0]

	@staticmethod
	def getQueryStringParameters(query):
		result = {}
		if len(query) > 0:
			for param in query.split("&"):
				keyValue = param.split("=")
				if(len(keyValue) > 1):
					if (not UrlUtils.isPlaceHolder(keyValue[1])):
						result[keyValue[0]]=keyValue[1]
		return result

	@staticmethod
	def isPlaceHolder(val):
		return re.match('\{([a-zA-Z0-9_\\.]*)\}', val)
		
	@staticmethod
	def replaceBaseUrlParameters(url, parameters):
		finalUrl = url
		keys = re.findall('\{([a-zA-Z0-9_\\.]*)\}', finalUrl)
		for key in keys:
			if key in parameters:
				finalUrl = re.sub("\{"+key+"\}&?", parameters[key], finalUrl)
				parameters.pop(key)
		return finalUrl
		
