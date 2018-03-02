class ExampleCustomDataType extends CustomDataType
	getCustomDataTypeName: ->
		"custom:base.example-plugin.slider"


CustomDataType.register(ExampleCustomDataType)
