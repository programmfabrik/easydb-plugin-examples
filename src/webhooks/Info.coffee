class Info
	sayHello: ->
		info = JSON.parse(process.argv[2])

		console.error(module)
		console.error(process.env)
		return
		
		# info.path = module.paths

		# ez5.returnJsonBody(info)

(->
	new Info().sayHello()
)()