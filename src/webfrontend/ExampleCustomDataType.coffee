class ExampleCustomDataType extends CustomDataType
	getCustomDataTypeName: ->
		"custom:base.example-plugin.slider"

	getCustomDataOptionsInDatamodelInfo: (custom_settings) ->
		if custom_settings.range
			[
				$$("example.custom.data.type.datamodel_info",
					from: custom_settings.range.from
					to: custom_settings.range.to
					)
			]
		else
			[]


	initData: (data) ->
		if not data[@name()]
			data[@name()] = {}

	renderDetailOutput: (data, top_level_data, opts) ->
		cdata = data[@name()]

		new CUI.Label
			class: @__getClass()
			text: cdata.value+" ["+cdata.description+"]"

	__getClass: ->
		mask_settings = @getCustomMaskSettings()
		[
			"ez5-example-custom-data-type"
			"ez5-example-custom-data-type--"+mask_settings.appearance.color
		].join(" ")

	renderEditorInput: (data, top_level_data, opts) ->
		custom_settings = @getCustomSchemaSettings()
		mask_settings = @getCustomMaskSettings()


		console.debug "mask settings:", @__getClass(), mask_settings

		@initData(data)

		cdata = data[@name()]

		form = new CUI.Form
			data: cdata
			class: @__getClass()
			fields: [
				form:
					label: $$("example.custom.data.type.input.value")
				type: CUI.Slider
				name: "value"
			,
				type: CUI.Input
				name: "description"
			]
			onDataChanged: =>
				CUI.Events.trigger
					node: form
					type: "editor-changed"
		.start()

		form

	getSaveData: (data, save_data, opts) ->
		cdata = data[@name()] or data._template?[@name()]
		save_data[@name()] = cdata
		return


CustomDataType.register(ExampleCustomDataType)
