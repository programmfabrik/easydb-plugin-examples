class ExampleRootApp extends RootMenuApp
	@is_allowed: ->
		true

	@group: ->
		"zzz_zexample"

	@label: ->
		"example.app.label"

	@isStartApp: ->
		false

	@path: ->
		["example"]

	allow_unload: ->
		CUI.confirm(text: "Leave?")

	unload: ->
		ez5.rootLayout.empty("center")
		delete(@__plugin)

		super()

	load: ->
		super()

		@__plugin = ez5.pluginManager.getPlugin("example-plugin")
		console.debug "plugin:", @__plugin

		@__plugin_url = @__plugin.getPluginURL()

		il = new CUI.ItemList
			items: [
				active: true
				loca_key: "example.root.app.button.base_config"
				onClick: =>
					@showBaseConfig()
			,
				loca_key: "example.root.app.button.system_right"
				onClick: =>
					@showSystemRight()
			,
				loca_key: "example.root.app.button.server_echo"
				onClick: =>
					@server("echo", "text")
			,
				loca_key: "example.root.app.button.server_config"
				onClick: =>
					@server("config")
			,
				loca_key: "example.root.app.button.server_session"
				onClick: =>
					@server("session")
			,
				loca_key: "example.root.app.button.server_tmp"
				onClick: =>
					@server("tmp", "text")
			,
				loca_key: "example.root.app.button.server_instance"
				onClick: =>
					@server("instance")
			]

		il.render()

		@__hl = new CUI.HorizontalLayout
			left:
				class: "ez5-example-plugin-hl-left"
				content: il

		ez5.rootLayout.replace(@__hl, "center")
		@showBaseConfig()

		CUI.resolvedPromise()

	showBaseConfig: ->
		od = new CUI.ObjectDumper
			parse_json: true
			object: ez5.session.getBaseConfig().system.example_plugin

		@__hl.replace(od, "center")

	showSystemRight: ->
		od = new CUI.ObjectDumper
			object: ez5.session.system_rights

		@__hl.replace(od, "center")

	server: (call, type = "json") ->
		switch type
			when "json"
				dataType = undefined
			when "text"
				dataType = ""

		ez5.server
			dataType: dataType
			local_url: @__plugin_url+"/"+call
		.done (result, status, xhr) =>
			if CUI.isString(result)
				content = new CUI.Label
					multiline: true
					text: result
			else
				content = new CUI.ObjectDumper
					object: result

			@__hl.replace(content, "center")


ez5.session_ready =>
	ez5.rootMenu.registerApp(ExampleRootApp)
