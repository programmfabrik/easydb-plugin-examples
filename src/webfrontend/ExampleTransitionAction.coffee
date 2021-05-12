class ExampleTransitionAction extends TransitionActionAction

	getListViewColumn: ->
		type: CUI.Output
		text: "Example Plugin Action: set timestamp in text field"

	getSaveData: ->
		sd =
			type: ExampleTransitionAction.getType()
			info: {}

	@getType: ->
		"plugin.base.example-plugin.example_transition_action"

	@getDisplayName: ->
		"Example Plugin Action"

TransitionAction.registerAction(ExampleTransitionAction)
