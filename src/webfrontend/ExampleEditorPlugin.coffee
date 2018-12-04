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

ez5.session_ready ->
	Editor.plugins.registerPlugin(ez5.ExampleEditorPlugin)
