import uuid
import hmac
import hashlib
import base64

class AuthUtils:

	@staticmethod
	def generate_authentication_header(public_key, private_key):
		newuuid = str(uuid.uuid4())
		digest_maker = hmac.new(private_key, newuuid, hashlib.sha1)
		uuid_hash = digest_maker.hexdigest()
		return { "X-Mashape-Authorization" : base64.b64encode(public_key + ":" + uuid_hash + newuuid) }

