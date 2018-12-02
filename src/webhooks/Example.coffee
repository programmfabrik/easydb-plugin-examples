ez5 = require('ez5')

class Example
	sayHello: ->
		info = JSON.parse(process.argv[2])

		info.paths = module.paths
		info.env = process.env

		ez5.returnJsonBody(info)
(->
	new Example().sayHello()
)()