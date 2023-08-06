import fastapi

from .. import shared


requested_objects = {}
"""Previously requested objects, from where they can be (re-)retrieved by id"""


def get_object(id: int):
	try:
		return requested_objects[id]
	except KeyError as e:
		raise fastapi.HTTPException(404, str(e))



def generate_functions(fastapi_server: fastapi.FastAPI, namespace):

	@fastapi_server.get('/root')
	def root():
		"""Get the id of the root object"""
		return shared.models.ObjectInfo.generate(namespace)

	@fastapi_server.get('/getattr')
	def get_object_attr(id: int, attribute: str):
		try:
			object = getattr(get_object(id), attribute)
		except AttributeError as e:
			raise fastapi.HTTPException(404, str(e))
		return shared.models.ObjectInfo.generate(object)

	@fastapi_server.post('/setattr')
	def set_object_attr(id: int, attribute: str, value: shared.models.Value):
		setattr(get_object(id), attribute, value.parse())

	@fastapi_server.get('/iterate')
	def iterate_object(id: int):
		object = get_object(id)
		return [shared.models.ObjectInfo.generate(i) for i in object]

	@fastapi_server.post('/call')
	def call_object(id: int, params: shared.models.CallParameters):
		object = get_object(id)
		result = params.use_on(object)
		return shared.models.ObjectInfo.generate(result)
