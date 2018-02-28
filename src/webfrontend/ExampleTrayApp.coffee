class ExampleTrayApp extends TrayApp
	is_allowed: =>
		# always allow this
		true

	getDisplay: =>
		new LocaButton
			loca_key: "example.tray.app.button"
			onClick: =>
				CUI.alert(text: $$("example.tray.app.thank_you.md"), markdown: true)

ez5.session_ready ->
	ez5.tray.registerApp(new ExampleTrayApp())


CUI.alert(text: "yo tray app")