ez5 = require('ez5')
fs = require('fs')

class Example
	sayHello: ->
		info = JSON.parse(process.argv[2])

		info.paths = module.paths
		info.env = process.env

		dumpfile = info.request.query_string_parameters?.dump_request?[0]
		# console.debug "hellO:", dumpfile
		if dumpfile
			fs.appendFileSync(dumpfile, info.request.body)
			console.log JSON.stringify
				headers:
					"Content-Type": "text/html; charset: utf-8"
				body: "Info was successfully stored into file: "+dumpfile+"."
		else
			ez5.returnJsonBody(info)
(->
	new Example().sayHello()
)()