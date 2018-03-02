class ExampleDetailSidebarPlugin extends DetailSidebarPlugin

	prefName: ->
		"example_detail_sidebar_plugin"

	getPane: ->
		"top"

	getButtonLocaKey: ->
		"example.detail.sidebar.plugin.button"

	render: ->
		console.info("ExampleDetailSidebarPlugin.render():", @_detailSidebar)

	renderObject: ->
		console.info("ExampleDetailSidebarPlugin.renderObject():", @_detailSidebar, @__currentObject)

	isAvailable: ->
		true

	hideDetail: ->
		@_detailSidebar.mainPane.empty("top")

	showDetail: ->
		obj = @_detailSidebar.object
		for field in obj.mask.getFields("all")
			console.debug "Field:", field.fullName(), field, "custom settings:", field.FieldSchema?.custom_settings

		od = new CUI.ObjectDumper(object: obj.getData())
		@_detailSidebar.mainPane.replace([
			new CUI.Label(text: "More info dumped to console!")
			od
		], "top")
		@


ez5.session_ready =>
	DetailSidebar.plugins.registerPlugin(ExampleDetailSidebarPlugin)
