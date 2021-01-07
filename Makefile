PLUGIN_NAME = example-plugin

INSTALL_FILES = \
	$(WEB)/l10n/cultures.json \
	$(WEB)/l10n/de-DE.json \
	$(WEB)/l10n/en-US.json \
	$(CSS) \
	$(WEB)/example-plugin.js \
	build/node_modules \
	example-plugin.config.yml

# XXX: unavailable languages
#	$(WEB)/l10n/es-ES.json \
#	$(WEB)/l10n/it-IT.json \

L10N_FILES = l10n/example-plugin.csv

L10N_GOOGLE_KEY = 1Z3UPJ6XqLBp-P8SUf-ewq4osNJ3iZWKJB83tc6Wrfn0
L10N_GOOGLE_GID = 1105524345

SCSS_FILES = src/webfrontend/example-plugin.scss

WEBHOOK_NAME = example
WEBHOOK_FILES = src/webhooks/Example.coffee

COFFEE_FILES = \
	src/webfrontend/ExampleTrayApp.coffee \
	src/webfrontend/ExampleBaseConfig.coffee \
	src/webfrontend/ExamplePoolPlugin.coffee \
	src/webfrontend/ExampleUserPlugin.coffee \
	src/webfrontend/ExampleAssetDetail3D.coffee \
	src/webfrontend/ExampleCustomDataType.coffee \
	src/webfrontend/ExampleMaskSplitterSimple.coffee \
	src/webfrontend/ExampleMaskSplitterBlock.coffee \
	src/webfrontend/ExampleDetailSidebarPlugin.coffee \
	src/webfrontend/ExampleExportManagerPlugin.coffee \
	src/webfrontend/ExampleRootApp.coffee

# EditorPlugin is not built in per default, its to annoying during testing.
# src/webfrontend/ExampleEditorPlugin.coffee

all: build

include easydb-library/tools/base-plugins.make

build: code css npm_install updater

updater:
	./node_modules/webpack/bin/webpack.js --config src/update/webpack.config.js

npm_install:
	npm install
	cp -r node_modules build/node_modules

code: $(JS) $(L10N) $(WEBHOOK_JS)

clean: clean-base
