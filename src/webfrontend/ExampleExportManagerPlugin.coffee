class ExampleExportManagerPlugin extends ExportManagerPlugin
	name: ->
		"example_export"

	nameLocalized: ->
		$$("example.export.manager.plugin.name")

	# renderForm: ->

	getExportData: ->
		exportData = super()
		console.debug "export data:", exportData

		# exportData.produce_options.eaf_type = @data.eaf_type
		exportData

	saveAllowed: ->
		true

ez5.session_ready ->
	ExportManager.registerPlugin(new ExampleExportManagerPlugin())

