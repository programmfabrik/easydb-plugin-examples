PLUGIN_NAME = example-plugin

INSTALL_FILES = \
	$(WEB)/l10n/cultures.json \
	$(WEB)/l10n/de-DE.json \
	$(WEB)/l10n/en-US.json \
	$(WEB)/l10n/es-ES.json \
	$(WEB)/l10n/it-IT.json \
	$(CSS) \
	$(WEB)/example-plugin.js \
	example-plugin.config.yml

L10N_FILES = l10n/example-plugin.csv

L10N_GOOGLE_KEY = 1Z3UPJ6XqLBp-P8SUf-ewq4osNJ3iZWKJB83tc6Wrfn0
L10N_GOOGLE_GID = 1105524345

CSS = $(WEB)/example-plugin.css

SCSS_FILES = src/webfrontend/example-plugin.scss

COFFEE_FILES = \
	src/webfrontend/ExampleTrayApp.coffee \
	src/webfrontend/ExampleBaseConfig.coffee \
	src/webfrontend/ExampleCustomDataType.coffee \
	src/webfrontend/ExampleDetailSidebarPlugin.coffee \
	src/webfrontend/ExampleExportManagerPlugin.coffee \
	src/webfrontend/ExampleRootApp.coffee

call_scss = sass --scss --no-cache --sourcemap=inline

all: build

include easydb-library/tools/base-plugins.make

build: code css

$(CSS): $(SCSS_FILES)
	mkdir -p $(dir $@)
	cat $(SCSS_FILES) | $(call_scss) > $(CSS)

code: $(JS) $(L10N)

css: $(CSS)

clean: clean-base
