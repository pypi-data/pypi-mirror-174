import requests

from .. import shared
from . import remote_objects



class BaseConnection:
	def __init__(self, server_address: str, port: int):
		"""
		Connects to a NoApi server

		:param server_address: address/ip of the server
		:param port: a unique port for your program (use the same one on server)
		"""
		if not server_address.startswith('http'):  # TODO figure out https
			server_address = 'http://' + server_address
		self.server_address = f"{server_address}:{port}"
		self.session = requests.Session()


	def call_server(self, method: str, function: str, data=None, **params):
		method = getattr(self.session, method)
		url = f'{self.server_address}/{function}'
		response = method(url, json=data, params=params)
		json = response.json()

		match response.status_code:
			case 200:
				return json
			case 404:
				raise ObjectNotFoundError(response)
			case _:
				raise InternalNoApiError(response)


	def test(self):
		try:
			self.call_server('get', 'test')
			return True
		except:
			return False




class Connection(BaseConnection):
	def call_server(self, method: str, function: str, data=None, **params):
		json = super().call_server(method, function, data, **params)

		def parse(data: dict):
			object = shared.models.ObjectInfo(**data)
			if object.basic:
				return object.value
			else:
				return remote_objects.RemoteObject(object.id, self)

		if isinstance(json, dict):
			return parse(json)
		elif isinstance(json, list):
			return [parse(i) for i in json]






class ServerError(BaseException):
	message: str

	def __init__(self, server_response: requests.Response):
		super().__init__(f"{self.message} (message: {server_response.json()['detail']})")


class ObjectNotFoundError(ServerError):
	message = "object not found on server"


class InternalNoApiError(ServerError):
	def __init__(self, response: requests.Response):
		self.message = f"Internal error with NoApi server - {response.status_code}"
		super().__init__(response)
