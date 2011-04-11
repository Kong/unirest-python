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
	def getCleanUrl(url, parameters):
		if param == None:
			param = []

		finalUrl = ""
		keys = re.findall('\{([a-z]*)\}', result)
		for key in keys:
			if key not in parameters:
				re.sub("[^&?]*=\{"+key+"\}&?", "", result)
		return result
	
	@staticmethod
	def removeQueryString(url):
		return url.split("?")[0]

	@staticmethod
	def getQueryStringParameters(url):
		result = {}
		query_init = url.find("?")
		if query_init > 0:
			query = url(query_init+1:)	
			for param in query.split("&")
				keyValue = param.split("=")
				if(len(keyValue) > 1):
					if (not isPlaceHolder(keyValue[1])):
						result[keyValue[0]]=keyValue[1]
		return result

	@staticmethod
	def isPlaceholder(val):
		return re.match('\{([a-z]*)\}', val)
		
