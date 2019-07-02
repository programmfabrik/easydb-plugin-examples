class ez5.ExampleEditorPlugin extends ez5.EditorPlugin
	checkForm: (opts) ->
		data = opts.resultObject.getData()
		problems = []

		ok = false
		for k, v of data[data._objecttype]
			if v == "Example"
				ok = true
				break;

		if !ok
			problems.push(new CheckDataProblem(text: "ExampleEditorPlugin: One field needs to be filled with **Example**."))

		return problems

	onSave: (opts) ->
		console.debug("ExampleEditorPlugin.onSave, data of the current object:", opts.resultObject.getData())
		# you can do data checks or changes here
		return CUI.confirm(text: "Do you really want to save?")


ez5.session_ready ->
	Editor.plugins.registerPlugin(ez5.ExampleEditorPlugin)
