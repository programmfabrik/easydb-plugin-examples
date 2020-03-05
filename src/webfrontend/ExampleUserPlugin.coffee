class ez5.ExampleUserPlugin extends ez5.UserPlugin

	getTabs: (tabs) ->
		tabs.push
			name: "example"
			text: "Example"
			content: =>
				form = new CUI.Form
					data: @_user.data.user
					name: "custom_data"
					fields: [
						type: CUI.Input
						name: "my_field"
						form:
							label: "My field"
							hint: "Write some data! This is a hint"
					]
				return form.start()
		return

	getSaveData: (saveData) ->
		saveData.user.custom_data.my_field = @_user.data.user.custom_data.my_field
		return

	isAllowed: ->
		return @_user.data.user.type in ["easydb", "system"] # Allow plugin just for 'easydb' and 'system' users.

User.plugins.registerPlugin(ez5.ExampleUserPlugin)