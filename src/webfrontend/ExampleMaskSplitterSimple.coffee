class ez5.ExampleMaskSplitterSimple extends CustomMaskSplitter

	isSimpleSplit: ->
		true

	getOptions: ->
		[
			form:
				label: "Splitter Title"
			type: CUI.Input
			name: "title"
		]

	renderField: (opts) ->
		return new CUI.Label(appearance: "title", text: @getDataOptions().title or "<no title>")

	isEnabledForNested: ->
		return true

MaskSplitter.plugins.registerPlugin(ez5.ExampleMaskSplitterSimple)
