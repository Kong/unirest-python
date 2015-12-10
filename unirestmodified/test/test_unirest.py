# -*- coding:utf-8 -*-

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

	def test_get2(self):
		response = unirest.get('http://httpbin.org/get?name=Mark', params={"nick":"the fosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 2)
		self.assertEqual(response.body['args']['name'], "Mark")
		self.assertEqual(response.body['args']['nick'], "the fosk")

	def test_get_unicode_param(self):
		response = unirest.get('http://httpbin.org/get?name=Shimada', params={"nick":u"しまりん"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 2)
		self.assertEqual(response.body['args']['name'], "Shimada")
		self.assertEqual(response.body['args']['nick'], u"しまりん")

	def test_get_none_param(self):
		response = unirest.get('http://httpbin.org/get?name=Mark', params={"nick":"thefosk", "age": None, "third":""})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 3)
		self.assertEqual(response.body['args']['name'], "Mark")
		self.assertEqual(response.body['args']['nick'], "thefosk")
		self.assertEqual(response.body['args']['third'], "")

	def test_post(self):
		response = unirest.post('http://httpbin.org/post', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 0)
		self.assertEqual(len(response.body['form']), 2)
		self.assertEqual(response.body['form']['name'], "Mark")
		self.assertEqual(response.body['form']['nick'], "thefosk")

	def test_post_none_param(self):
		response = unirest.post('http://httpbin.org/post', params={"name":"Mark", "nick":"thefosk", "age": None, "third":""})
		self.assertEqual(response.code, 200)
		self.assertEqual(len(response.body['args']), 0)
		self.assertEqual(len(response.body['form']), 3)
		self.assertEqual(response.body['form']['name'], "Mark")
		self.assertEqual(response.body['form']['nick'], "thefosk")
		self.assertEqual(response.body['form']['third'], "")

	def test_delete(self):
		response = unirest.delete('http://httpbin.org/delete', params={"name":"Mark", "nick":"thefosk"})
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['form']['name'], "Mark")
                self.assertEqual(response.body['form']['nick'], "thefosk")

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
		response = unirest.post('http://httpbin.org/post', headers={'Content-Type':'text/plain'}, params="hello this is custom data")
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['data'], "hello this is custom data")

	def test_gzip(self):
		response = unirest.get('http://httpbin.org/gzip', params={"name":"Mark"})
		self.assertEqual(response.code, 200)
		self.assertTrue(response.body['gzipped'])

	def test_basicauth(self):
		response = unirest.get('http://httpbin.org/get', auth=('marco', 'password'))
		self.assertEqual(response.code, 200)
		self.assertEqual(response.body['headers']['Authorization'], "Basic bWFyY286cGFzc3dvcmQ=")

	def test_defaultheaders(self):
		unirest.default_header('custom','custom header')
		response = unirest.get('http://httpbin.org/get')
		self.assertEqual(response.code, 200)
		self.assertTrue('Custom' in response.body['headers']);
		self.assertEqual(response.body['headers']['Custom'], "custom header")

		# Make another request
		response = unirest.get('http://httpbin.org/get')
		self.assertEqual(response.code, 200)
		self.assertTrue('Custom' in response.body['headers']);
		self.assertTrue(response.body['headers']['Custom'], "custom header")

		# Clear the default headers
		unirest.clear_default_headers()
		response = unirest.get('http://httpbin.org/get')
		self.assertEqual(response.code, 200)
		self.assertFalse('Custom' in response.body['headers']);

	def test_timeout(self):
		unirest.timeout(3)
		response = unirest.get('http://httpbin.org/delay/1')
		self.assertEqual(response.code, 200)

		unirest.timeout(1)
		try:
			response = unirest.get('http://httpbin.org/delay/3')
			self.fail("The timeout didn't work")
		except:
								pass

if __name__ == '__main__':
	unittest.main()
