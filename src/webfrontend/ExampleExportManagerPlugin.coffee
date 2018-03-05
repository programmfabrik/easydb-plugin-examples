class ExampleExportManagerPlugin extends ExportManagerPlugin
	name: ->
		"example_export"

	nameLocalized: ->
		$$("example.export.manager.plugin.name")

	getExportData: ->
		exportData = super()

		if not exportData.produce_options
			exportData.produce_options = {}
		exportData.produce_options.with_tags = @__data.with_tags

		return exportData

	renderForm: ->
		@__data = @__initData()

		form = new CUI.Form
			data: @__data
			fields: [
				type: CUI.Checkbox
				name: "with_tags"
				form:
					label: $$("example.export.manager.form.with_tags.label")
				text: $$("example.export.manager.form.with_tags.text")
			]
		return form.start()

	saveAllowed: ->
		true

	__initData: ->
		data =
			with_tags: false

		exportData = @_export.data?.export
		if exportData
			data.with_tags = exportData.produce_options?.with_tags

		return data

ez5.session_ready ->
	ExportManager.registerPlugin(new ExampleExportManagerPlugin())
