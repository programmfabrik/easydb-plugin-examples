# class ez5.ExamplePdfCreatorNode extends ez5.PdfCreator.Node

# 	@getName: ->
# 		"an-example-node"

# 	__renderPdfContent: (opts) ->
# 		object = opts.object
# 		if not object
# 			return

# 		data = @getData()

# 		content = new CUI.VerticalLayout
# 			top:
# 				content: new CUI.Label(text: data.title)
# 			center:
# 				content: new CUI.MultilineLabel(text: CUI.util.dump(object))

# 		return content

# 	__getSettingsFields: ->
# 		fields = [
# 			type: CUI.Input
# 			name: "title"
# 			form: label: $$("pdf-creator.node.an-example-node.settings.title")
# 		]
# 		return fields

# 	__getStyleSettings: ->
# 		return ["class-name", "background", "color"]

# ez5.PdfCreator.plugins.registerPlugin(ez5.ExamplePdfCreatorNode)