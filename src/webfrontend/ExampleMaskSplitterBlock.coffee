class ez5.ExampleMaskSplitterBlock extends CustomMaskSplitter

	isSimpleSplit: ->
		false

	getOptions: ->
		[
			form:
				label: "Color"
			type: CUI.Select
			options: [
				value: "black"
			,
				value: "red"
			,
				value: "green"
			,
				value: "yellow"
			]
			name: "color"
		,
			form:
				label: "Style"
			type: CUI.Select
			options: [
				value: "solid"
			,
				value: "dotted"
			,
				value: "dashed"
			]
			name: "style"

		]

	getDefaultOptions: ->
		return {
			color: "black"
			style: "solid"
		}

	renderField: (opts) ->
		color = @getDataOptions().color
		style = @getDataOptions().style

		console.debug @, "ExampleMaskSplitterBlock.renderField", opts, color, style

		div = CUI.dom.element("div", class: "ez5-example-mask-splitter")
		CUI.dom.setStyle div,
			border: "4px "+style+" "+color
		return CUI.dom.append(div, @renderInnerFields(opts))

	isEnabledForNested: ->
		return true



MaskSplitter.plugins.registerPlugin(ez5.ExampleMaskSplitterBlock)
