class ExampleAssetDetail3D extends AssetDetail
	getButtonLocaKey: (asset) ->
		console.debug "class extension", asset.value.class_extension
		if asset.value.class_extension != "image.jpg"
			return

		huge = asset.value.versions.huge

		if huge?.status != "done"
			return

		"example.asset.detail.360degrees"


	createMarkup: ->
		# console.debug "creatingMarkup", @
		super()

		huge = @asset.value.versions.huge # original

		obj = CUI.dom.element("A-SCENE", embedded: true, class: "ez5-ascene")
		obj2 = CUI.dom.element("A-SKY", src: ez5.getAbsoluteURL(huge.url))

		obj.appendChild(obj2)

		CUI.dom.append(@outerDiv, obj)

		# lbl = new CUI.Label
		# 	class: "ez5-example-asset-detail-filename"
		# 	text: "360°"

		# CUI.dom.append(@outerDiv, lbl)

		console.debug "asset button", @, @asset, obj, obj2


ez5.session_ready =>
	# this moved to easydb-a-frame-plugin
	#
	# scriptNode = CUI.dom.element "SCRIPT",
	# 	src: "https://aframe.io/releases/0.7.1/aframe.min.js"
	# 	type: "text/javascript"
	# 	charset: "utf-8"

	# document.head.appendChild(scriptNode)
	# AssetBrowser.plugins.registerPlugin(ExampleAssetDetail3D)
