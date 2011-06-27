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
import urllib
import json
from mashape.exception.clientException import MashapeClientException

class TokenUtil:

	def requestToken(self, devKey):
		TOKEN_URL="https://api.mashape.com/requestToken"
		data = {'devkey' : devKey}
		jsonToken = urllib2.urlopen(TOKEN_URL, urllib.urlencode(data)).read()
		answer = json.loads(jsonToken)
		if "error" in answer:
			error = answer["error"]
			raise MashapeClientException(error["message"], error["code"])
		else:
			return answer['token']
