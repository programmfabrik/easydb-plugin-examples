class ExampleBaseConfig extends BaseConfigPlugin
	getFieldDefFromParm: (baseConfig, pname, def, parent_def) ->
		if def.plugin_type != "example-base-config"
			return

		field =
			type: CUI.Form
			name: "example_base_config"
			fields: [
				type: CUI.Select
				name: "select"
				options: [
					value: "a"
				,
					value: "b"
				]
			,
				type: CUI.Input
				name: "input"
			]

		field

CUI.ready =>
	BaseConfig.registerPlugin(new ExampleBaseConfig())
