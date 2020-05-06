class ExampleAssetDetailPDF extends AssetDetail
	getButtonLocaKey: (asset) ->
		if asset.value.class_extension != "office.pdf"
			return

		orig = asset.value.versions.original

		if orig.status != "done"
			return

		"example.asset.detail.pdf"

	createMarkup: ->
		# console.debug "creatingMarkup", @
		super()

		orig = @asset.value.versions.original

		obj = CUI.dom.element("OBJECT", class: "ez5-example-asset-detail-pdf")

		obj.data = orig.url
		obj.type = "application/pdf"

		CUI.dom.append(@outerDiv, obj)

		lbl = new CUI.Label
			class: "ez5-example-asset-detail-filename"
			text: @asset.value.original_filename_basename

		CUI.dom.append(@outerDiv, lbl)

		console.debug "asset button", @, @asset, obj



ez5.session_ready =>
	AssetBrowser.plugins.registerPlugin(ExampleAssetDetailPDF)
