import pydantic, typing, types
from .. import server, client



basic_types = {str, int, float, bool, None, types.NoneType}
"""Basic immutable types that can be sent as-is over the network"""



class ObjectInfo(pydantic.BaseModel):

	id: int
	basic: bool
	value: typing.Any

	@classmethod
	def generate(cls, object):
		object_id = id(object)
		basic = (type(object) in basic_types)

		server.object_controller.requested_objects[object_id] = object

		return cls(
			id=object_id,
			basic=basic,
			value=object if basic else None
		)



class Value(pydantic.BaseModel):

	value: typing.Any
	remote_object: bool = False

	@classmethod
	def generate(cls, value):
		if isinstance(value, client.remote_objects.RemoteObject):
			return cls(value=value.___id___, remote_object=True)
		else:
			return cls(value=value, remote_object=False)

	def parse(self):
		if self.remote_object:
			return server.object_controller.requested_objects[self.value]
		else:
			return self.value



class CallParameters(pydantic.BaseModel):

	args: list[Value]
	kwargs: dict[str, Value]

	def use_on(self, object):
		args = [a.parse() for a in self.args]
		kwargs = {key: arg.parse() for (key, arg) in self.kwargs.items()}
		return object(*args, **kwargs)
