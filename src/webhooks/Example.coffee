ez5 = require('ez5')
fs = require('fs')

class Example
	main: (info) ->
		info.paths = module.paths
		info.env = process.env

		dumpfile = info.request.query_string_parameters?.dump_request?[0]
		if dumpfile
			fs.appendFileSync(dumpfile, info.request.body)
			body = "Info was successfully stored into file: "+dumpfile+"."
			respondSuccess(body)
		else
			respondSuccess(info)

module.exports = new Example()