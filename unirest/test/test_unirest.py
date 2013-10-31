import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import unirest

class UnirestTestCase(unittest.TestCase):
	def test_get(self):
		response = unirest.get('http://httpbin.org/get?name=Mark', params={"nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 2)
		self.assertEqual(response.body['args']['name'], "Mark")
		self.assertEqual(response.body['args']['nick'], "thefosk")

	def test_post(self):
		response = unirest.post('http://httpbin.org/post', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 0)
		self.assertEqual(len(response.body['form']), 2)
		self.assertEqual(response.body['form']['name'], "Mark")
		self.assertEqual(response.body['form']['nick'], "thefosk")

	def test_delete(self):
		response = unirest.delete('http://httpbin.org/delete', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['data'], "nick=thefosk&name=Mark")

	def test_put(self):
		response = unirest.put('http://httpbin.org/put', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 0)
		self.assertEqual(len(response.body['form']), 2)
		self.assertEqual(response.body['form']['name'], "Mark")
		self.assertEqual(response.body['form']['nick'], "thefosk")

	def test_patch(self):
		response = unirest.patch('http://httpbin.org/patch', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 0)
		self.assertEqual(len(response.body['form']), 2)
		self.assertEqual(response.body['form']['name'], "Mark")
		self.assertEqual(response.body['form']['nick'], "thefosk")

	def test_post_entity(self):
		response = unirest.post('http://httpbin.org/post', params="hello this is custom data")
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['data'], "hello this is custom data")

	def test_gzip(self):
		response = unirest.get('http://httpbin.org/gzip', params={"name":"Mark"})
		self.assertEqual(response.code, 200)
		self.assertTrue(response.body['gzipped'])

	def test_basicauth(self):
		response = unirest.get('http://httpbin.org/gzip', auth=('marco', 'password'))
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['headers']['Authorization'], "Basic bWFyY286cGFzc3dvcmQ=")

if __name__ == '__main__':
	unittest.main()