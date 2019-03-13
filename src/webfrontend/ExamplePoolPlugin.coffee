class ez5.ExamplePoolPlugin extends ez5.PoolPlugin
	getTabs: (tabs) ->
		tabs.push
			name: "example-pool"
			text: "Example Add-On"
			content: =>
				form = new CUI.Form
					data: @_pool.data.pool
					name: "custom_data"
					fields: [
						type: CUI.Input
						textarea: true
						name: "example_add_on"
						form:
							label: "Add-On Info"
							hint: "Add some info here."
					]

				return form.start()

		return tabs

	getInfoDivRows: (rows) ->
		add_on_info = @_pool.data.pool.custom_data.example_add_on
		if add_on_info
			rows.push
				key: "Add-On Info"
				value: add_on_info
		return

	getInfoDiv: (nodes) ->
		nodes.push(new CUI.Label(
			padded: true
			text: "The ExamplePoolPlugin is **active**."
			markdown: true
			multiline: true
		))
		return

	getSaveData: (save_data) ->

		save_data.pool.custom_data.example_add_on = @_pool.data.pool.custom_data.example_add_on
		return

# This needs immediate loading, so that the startup phase for pool manager already
# includes this plugin
Pool.plugins.registerPlugin(ez5.ExamplePoolPlugin)
