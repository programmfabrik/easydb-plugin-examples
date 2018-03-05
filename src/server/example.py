# coding=utf8

import os
import json
import yaml

from datetime import datetime, date
import calendar
import locale
from dateutil.relativedelta import relativedelta

from time import sleep
from threading import Thread

from context import EasydbException
from context import InvalidValueError
from context import get_json_value


# called from easydb
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

	# register a callback that is called after data was exported
	# export objects as YML
	easydb_context.register_callback('export_produce', {'callback': 'export_as_yml'})

	# register a process callback
	# check objects for expiration date and send mails
	easydb_context.register_callback('process', {'name': 'check_expiration_date'})


# helper method to generate a unique id for an object
def generate_unique_id(easydb_context):
	# get a unused id from the database and add a (optional) prefix
	return easydb_context.next_unique_id_prefixed('medium_nummer', 16, 'medium_')


# helper method to perform a search using an EasydbContext
def perform_search_easydb(easydb_context, query, logger = None):
	# get the user id from the current session
	user_id = None
	try:
		session = easydb_context.get_session()
		user_id = get_json_value(session, "user.user._id")
		if not isinstance(user_id, int):
			logger.error("Could not get user id from session")
			return None
	except Exception as e:
		logger.error("Could not get user id from session: %s" % e)
		return None
	search_result = easydb_context.search("user", user_id, search_query)
	if logger is not None:
		logger.debug("Search Result: %s" % json.dumps(search_result, indent = 4))

	return search_result


# helper method to perform a search using an EasydbProcessContext
def perform_search_process(easydb_context, connection, session_identifier, query, logger = None):
	search_result = easydb_context.search(connection, "user", session_identifier, query)
	if logger is not None:
		logger.debug("Search Result: %s" % json.dumps(search_result, indent = 4))

	return search_result


# helper method that creates a elasticsearch request for the name of a medienart object
def search_for_medienart(easydb_context, name):
	logger = easydb_context.get_logger('example-plugin.search_for_medienart')
	logger.info("Search for medienart '%s'" % name)

	# define the search query
	search_query = {
		"type": "object",
		"generate_rights": False,
		"include_fields": ["medienart._id"], # the field that we want to get as a search result
		"search": [{
			"type": "in", # search on of the values in 'in'
			"bool": "should",
			"fields": ["medienart.name"], # the name of the field that we search for
			"in": [name] # list of values that the field should have (only on in this case)
		}]
	}
	logger.debug("Search Request: %s" % json.dumps(search_query, indent = 4))

	# perform the search and return the result
	search_result = perform_search_easydb(easydb_context, search_query, logger)

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


# called after data was exported
# load the exported json files and save the content as YML
def export_as_yml(easydb_context, parameters):
	logger = easydb_context.get_logger('example-plugin.export_as_yml')

	# get the exporter definition
	exporter = easydb_context.get_exporter()

	# check if the export definition fits to this plugin
	produce_options = get_json_value(exporter.getExport(), "export.produce_options", False)
	if str(get_json_value(produce_options, "plugin", False)) != "example_export":
		return

	# check if the produce option for exporting the YML with or without tags is a boolean, else set it to false
	with_tags = get_json_value(produce_options, "with_tags", False)
	if not isinstance(with_tags, bool):
		with_tags = False

	# load exported files (need to be exported as JSON files)
	export_dir = exporter.getFilesPath()
	logger.debug("Export Dir: %s" % export_dir)

	files = exporter.getFiles()
	if not isinstance(files, list) or len(files) < 1:
		logger.warn("No valid file list!")
		return

	# iterate over the definitions of the exported files and parse the json content
	for f in files:
		file_path = str(get_json_value(f, "path", False))
		if file_path.lower().endswith(".json"):
			# absolute path to the original file
			file_path = os.path.abspath(export_dir + "/" + file_path)

			# path of the new file
			file_name = str(f["path"].split(".")[0] + ".yml")

			logger.debug("Converting JSON file %s to YML" % file_path)

			try:
				# load and parse the json file
				file = open(file_path, "r")
				content = json.loads(file.read().decode('utf-8'))
				file.close()

				# convert the objects that are defined in a json array to YML and save it in a file next to the original file
				objects = get_json_value(content, "objects", False)
				if isinstance(objects, list) and len(objects) > 0:

					# save the file in the temporary folder and add it later to the exported files
					tmp_filename = os.path.abspath("%s/../tmp/objects.yml" % export_dir)

					with open(tmp_filename, "w") as yml_file:
						# define the final dict that will be converted to YML
						object_output = {
							"objects": objects
						}

						# depending on the produce options, export the YML with or without tags
						if with_tags:
							yaml.dump(object_output, yml_file, default_flow_style = False)
						else:
							yaml.safe_dump(object_output, yml_file, default_flow_style = False)

						yml_file.close()

						logger.debug("Saved objects as %s" % tmp_filename)

						# add the new YML file to the export so it can be opened or downloaded from the frontend
						exporter.addFile(tmp_filename, file_name)

						# remove the old JSON file
						exporter.removeFile(f["path"])

				else:
					logger.debug("Found no 'objects' array")
			except Exception as e:
				logger.warn("Could not convert JSON to YML: %s" % str(e))


# run method to start threads for process plugins
# method is called at server start
def run(easydb_context):
	logger = easydb_context.get_logger('example-plugin.process')
	logger.info("run")

	# set up a thread that runs once a day and checks if the expiration
	t = Thread(target=check_expiration_date, args=(easydb_context,))
	t.start()
	t.join()


# repeatedly check the expiration date of objects
# easydb_context: EasydbProcessContext
def check_expiration_date(easydb_context):

	logger = easydb_context.get_logger('example-plugin.check_expiration_date')

	# connect to the database
	connection = easydb_context.db_connect('check_expiration_date')

	# load the configuration
	config = easydb_context.get_config(connection)

	# search all objects of the type 'medium', using a SQL query, where the expiration data is in less then a week
	while True:

		# create and format a date that is 7 days in the future
		days_in_future = 7
		date = datetime.now() + relativedelta(days = days_in_future)
		date_str = date.strftime("%Y-%m-%d")

		# get a database cursor
		cursor = connection.cursor()

		# build the Postgres statement
		sql = """
			SELECT m."id:pkey", m.titel, m.identifier, m.ablaufdatum, m.":owner:ez_user:id",
				u.login, u.name, u.firstname, u.displayname, u.frontend_language,
				e.address
			FROM medium m JOIN ez_user u ON m.":owner:ez_user:id" = u."ez_user:id"
			AND ablaufdatum <= '%s'
			JOIN "ez_user:email" e ON e."ez_user:id" = u."ez_user:id"
			AND e.is_primary AND e.use_for_email AND e.send_email AND address IS NOT NULL
		"""

		# perform the request and save the result
		connection.cursor().execute(sql % date_str)
		result = connection.cursor().fetchall()

		mails_to_send = {}

		logger.debug("%s results found" % len(result))
		for row in result:
			try:
				# information about the object
				identifier = row["identifier"]
				titel = row["titel"]
				ablaufdatum = datetime.strptime(row["ablaufdatum"], "%Y-%m-%d")

				# mail address
				address = row["address"] if len(row["address"]) else None

				if address is None:
					continue

				# user information
				user_displayname = row["displayname"]
				if user_displayname is None or len(user_displayname) < 1:
					user_displayname = ""
					user_displayname += row["firstname"] if row["firstname"] is not None else ""
					user_displayname += " " if len(user_displayname) > 0 else ""
					user_displayname += row["name"] if row["name"] is not None else ""

					if len(user_displayname) < 1:
						user_displayname = row["login"] if row["login"] is not None else ""

						if len(user_displayname) < 1:
							user_displayname = address

				# set the locale according to the user language
				user_lang = row["frontend_language"]

				# write the text for the mail in german or english
				# TODO get the l10n translations from the server
				mail_text = None

				if user_lang == "de-DE":
					locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
					mail_text = "Medium %s (%s) laeuft am %s ab" % (
						identifier,
						titel,
						"%s, den %s" % (
							calendar.day_name[ablaufdatum.weekday()],
							ablaufdatum.strftime("%d.%m.%Y")
						)
					)
				else:
					locale.setlocale(locale.LC_ALL, 'en_US.utf8')
					mail_text = "Medium %s (%s) expires %s" % (
						identifier,
						titel,
						"%s, %s" % (
							calendar.day_name[ablaufdatum.weekday()],
							ablaufdatum.strftime("%Y-%m-%d")
						)
					)

				logger.info(mail_text)

				if not address in mails_to_send:
					mails_to_send[address] = {
						"language": user_lang,
						"name": user_displayname,
						"mail_text": []
					}

				mails_to_send[address]["mail_text"].append(mail_text)

			except Exception as e:
				raise e

		for adr in mails_to_send:

			mail = None
			if mails_to_send[adr]["language"] == "de-DE":
				mail = "Hallo %s,\n\ndie folgenden Objekte laufen innerhalb der nächsten %d Tage ab:\n\n%s\n\nMit freundlichen Gruessen"
			else:
				mail = "Hello %s,\n\nthe following objects expire during the next %d days:\n\n%s\n\nRegards"

			logger.debug("Mail to %s:\n%s" % (
				adr, mail % (
					mails_to_send[adr]["name"],
					days_in_future,
					"\n - ".join(mails_to_send[adr]["mail_text"])
				)
			))

			# TODO send the mail instead of logging the mail text

		# sleep for one hour
		sleep(60 * 60)

		# TODO dont send more then one mail for each object


# method to cleanup process plugin resources before the server stops
def stop(easydb_context):
	logger = easydb_context.get_logger('example-plugin.process')
	logger.info("stop")


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

