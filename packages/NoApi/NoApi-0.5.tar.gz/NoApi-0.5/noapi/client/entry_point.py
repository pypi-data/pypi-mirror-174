from . import connector, remote_objects



class Client(remote_objects.RemoteObject):

	def __init__(self, server_address: str, port: int):
		"""
		Gateway to variables and objects on a remote machine
		
		:param server_address: address/ip of the server
		:param port: a unique port for your program (use the same one on server)
		"""
		self.___cached_root_id___ = None
		super().__init__(0, connection=connector.Connection(server_address, port))


	@property
	def ___id___(self):
		if self.___cached_root_id___ is None:
			self.___cached_root_id___ = self.___connection___.call_server('get', 'root').___id___
		return self.___cached_root_id___

	@___id___.setter
	def ___id___(self, id: int):
		pass
