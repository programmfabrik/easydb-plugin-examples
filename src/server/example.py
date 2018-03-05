import json
import datetime
from context import EasydbException
from context import InvalidValueError
from context import get_json_value


## called from easydb
def easydb_server_start(easydb_context):
	# called when server starts (just once)
	logger = easydb_context.get_logger('example-plugin')
	logger.debug('server_start')
	logger.debug('instance information: {0}'.format(json.dumps(easydb_context.get_instance(), indent = 4)))

	# api callbacks that extend the api
	# the api url is <server>/api/plugin/base/<plugin name>/<callback name>
	easydb_context.register_callback('api', { 'name': 'echo', 'callback': 'echo'})
	easydb_context.register_callback('api', { 'name': 'config', 'callback': 'config'})
	easydb_context.register_callback('api', { 'name': 'session', 'callback': 'session'})
	easydb_context.register_callback('api', { 'name': 'tmp', 'callback': 'tmp'})
	easydb_context.register_callback('api', { 'name': 'instance', 'callback': 'instance'})

	# register a callback that is called before an object would be saved in the database
	# callback registered in the server as 'db_pre_update'
	# method name that is called: 'pre_update'
	easydb_context.register_callback('db_pre_update', {'callback': 'pre_update'})


# helper method to generate a unique id for an object
def generate_unique_id(easydb_context):
	# get a unused id from the database and add a (optional) prefix
	return easydb_context.next_unique_id_prefixed('medium_nummer', 16, 'medium_')


# helper method that creates a elasticsearch request for the name of a medienart object
def search_for_medienart(easydb_context, name):
	logger = easydb_context.get_logger('example-plugin.search_for_medienart')
	logger.info("Search for medienart '%s'" % name)

	# get the user id from the current session
	user_id = None
	try:
		session = easydb_context.get_session()
		user_id = get_json_value(session, "user.user._id")
		if not isinstance(user_id, int):
			logger.error("Could not get user id from session")
			return None
	except Exception as e:
		print e
		return None

	# define the search query
	search_query = {
		"type": "object",
		"generate_rights": False,
		"include_fields": ["medienart._id"],     # the field that we want to get as a search result
		"search": [{
			"type":   "in",                      # search on of the values in 'in'
			"bool":   "should",
			"fields": ["medienart.name"],        # the name of the field that we search for
			"in":     [name]                     # list of values that the field should have (only on in this case)
		}]
	}
	logger.debug("Search Request: %s" % json.dumps(search_query, indent = 4))

	# perform the search and return the result
	search_result = easydb_context.search("user", user_id, search_query)
	logger.debug("Search Result: %s" % json.dumps(search_result, indent = 4))

	return search_result


# helper method to create a linked medienart object from the search result
def link_medienart(easydb_context, data, search_result, name):
	# get the medienart id from the search result and set it in the object
	result_objects = get_json_value(search_result, "objects")
	if isinstance(result_objects, list) and len(result_objects) > 0:

		# there should only be on hit, but to be sure iterate through the list of result objects and find the one with the correct name
		for k in range(len(result_objects)):

			# check if the name is correct and there is a valid id
			medienart_name = get_json_value(result_objects[k], "medienart.name")
			print medienart_name, type(medienart_name)
			if isinstance(medienart_name, unicode) and medienart_name == unicode(name):
				medienart_id = get_json_value(result_objects[k], "medienart._id")
				print medienart_id, type(medienart_id)
				if isinstance(medienart_id, int):

					# the medienart id is valid, add a linked object to the data
					data["medium"]["medienart"] = {
							"medienart": {
								"_id": medienart_id
							},
							"_objecttype": "medienart",
							"_mask": "_all_fields"
						}

					return data
	return data


# method for the 'db_pre_update' callback
# this method should be used to check the validaty of the object data before saving
def pre_update(easydb_context, easydb_info):
	# get a logger
	logger = easydb_context.get_logger('example-plugin.pre_update')
	logger.info("pre_update was called")

	# get the object data
	data = get_json_value(easydb_info, "data")
	logger.debug("Object Data: %s" % json.dumps(data, indent = 4))
	logger.debug("%d Objects" % len(data))

	# check the data, and if there is invalid data, throw an InvalidValueError
	for i in range(len(data)):

		# depending on the mask, check if mandatory fields are set and set the linked object medienart
		if data[i]["_mask"] == "medium_cd":
			logger.debug("Checking mandatory fields for 'CD'")
			spieldauer_min = get_json_value(data[i], "medium.spieldauer_min")

			# check if the fields are valid
			if spieldauer_min is None or not isinstance(spieldauer_min, int) or spieldauer_min <= 0:
				raise InvalidValueError("spieldauer_min", str(spieldauer_min), "integer > 0")

			# format the time to hh:mm:ss. the decimal number is defined as an integer, so divide the value by 100 to get seconds
			hours, remainder = divmod(int(float(spieldauer_min) / 100.0), 3600)
			minutes, seconds = divmod(remainder, 60)
			data[i]["medium"]["spieldauer"] = "%02d:%02d:%02d" % (hours, minutes, seconds)

			# set the linked object medienart with the value 'CD'
			# perform an elasticsearch request to get the id of the medienart object
			search_result = search_for_medienart(easydb_context, "CD")
			data[i] = link_medienart(easydb_context, data[i], search_result, "CD")

		elif data[i]["_mask"] == "medium_buch":
			logger.debug("Checking mandatory fields for 'Buch'")
			seitenzahl = get_json_value(data[i], "medium.seitenzahl")

			# check if the fields are valid
			if seitenzahl is None or not isinstance(seitenzahl, int) or seitenzahl <= 0:
				raise InvalidValueError("seitenzahl", str(seitenzahl), "integer > 0")

			# set the linked object medienart with the value 'Buch'
			# perform an elasticsearch request to get the id of the medienart object
			search_result = search_for_medienart(easydb_context, "Buch")
			data[i] = link_medienart(easydb_context, data[i], search_result, "Buch")

		# to avoid confusion with masks and read/write settings in masks, always use the _all_fields mask
		data[i]["_mask"] = "_all_fields"

		# generate a unique id for this object, if there is none (when the object was just created)
		if get_json_value(data[i], "medium.identifier") is None:
			new_id = str(generate_unique_id(easydb_context))
			logger.debug("Generating new ID for Object %d: %s" % (i, new_id))
			data[i]["medium"]["identifier"] = new_id


	# always return if no exception was thrown, so the server and frontend are not blocked
	print json.dumps(data, indent=4)
	return data


# method that is called when API Endpoint <server>/api/plugin/base/example-plugin/config is called
def config(easydb_context, parameters):
	return json_response(easydb_context.get_config())


# method that is called when API Endpoint <server>/api/plugin/base/example-plugin/session is called
def session(easydb_context, parameters):
	return json_response(easydb_context.get_session())


# method that is called when API Endpoint <server>/api/plugin/base/example-plugin/tmp is called
def tmp(easydb_context, parameters):
	tmp_dir = easydb_context.get_temp_dir()
	return text_response('temp dir: {0}'.format(tmp_dir))


# method that is called when API Endpoint <server>/api/plugin/base/example-plugin/instance is called
def instance(easydb_context, parameters):
	instance = easydb_context.get_instance()
	return json_response(easydb_context.get_instance())


# method that is called when API Endpoint <server>/api/plugin/base/example-plugin/echo is called
def echo(easydb_context, parameters):
	status_code = 200
	content_type = '<undefined>'
	lines = []

	lines.append('*** Request Information ***')
	lines.append('')
	lines.append(u'{0} {1}'.format(parameters['method'], parameters['path']))
	query_string = parameters['query_string']
	if len(query_string) > 0:
		lines.append('Query String Parameters:')
		for part in query_string.split('&'):
			part_parts = part.split('=')
			key = part_parts[0]
			if len(part_parts) > 1:
				value = part_parts[1]
			else:
				value = '<undefined>'
			lines.append(u'* {0} = {1}'.format(key, value))
			if key == 'status_code':
				status_code = int(value)
	else:
		lines.append('Query String: <empty>')
	lines.append('')
	lines.append('Headers:')
	for key, value in parameters['headers'].items():
		lines.append('* {0}: {1}'.format(key, value))
		if key.lower() == 'content-type':
			content_type = value
	lines.append('')
	body = parameters['body']
	if len(body) > 0:
		if 'text' in content_type or 'json' in content_type:
			lines.append('Body:')
			lines.append('')
			lines.append(body)
		else:
			lines.append('Body: {0} bytes'.format(len(body)))
	else:
			lines.append('Body: none')
	lines.append('')
	return text_response('\n'.join(lines), status_code=status_code)


def json_response(js):
	return {
		"status_code": 200,
		"body": json.dumps(js, indent=4),
		"headers": {
			"Content-Type": "application/json; charset=utf-8"
		}
	}


def text_response(text, status_code=200):
	return {
		"status_code": status_code,
		"body": text,
		"headers": {
			"Content-Type": "text/plain; charset=utf-8"
		}
	}

