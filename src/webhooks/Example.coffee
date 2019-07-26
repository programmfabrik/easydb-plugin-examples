fs = require('fs')
asciify = require('asciify')

class Example
	main: (info) ->
		info.paths = module.paths
		info.env = process.env

		queryStringParameters = info.request.query_string_parameters
		dumpfile = queryStringParameters?.dump_request?[0]
		if dumpfile
			fs.appendFileSync(dumpfile, info.request.body)
			body = "Info was successfully stored into file: "+dumpfile+"."
			ez5.respondSuccess(body)
		else if asciiText = queryStringParameters?.ascii?[0]
			text = asciiText or "Hello!"
			asciify( text, color:'green', (err, res) =>
				ez5.respondSuccess(res)
			);
		else if pretty = queryStringParameters?.pretty?[0]
			ez5.respondSuccess(JSON.stringify(JSON.parse(info.request.body), null, 4) + "\n")
		else
			ez5.respondSuccess(info)

module.exports = new Example()