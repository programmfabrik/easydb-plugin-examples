PLUGIN_NAME = example-plugin

INSTALL_FILES = \
	$(WEB)/l10n/cultures.json \
	$(WEB)/l10n/de-DE.json \
	$(WEB)/l10n/en-US.json \
	$(WEB)/l10n/es-ES.json \
	$(WEB)/l10n/it-IT.json \
	$(WEB)/example-plugin.js \
	example-plugin.config.yml

L10N_FILES = l10n/example-plugin.csv

L10N_GOOGLE_KEY = 1Z3UPJ6XqLBp-P8SUf-ewq4osNJ3iZWKJB83tc6Wrfn0
L10N_GOOGLE_GID = 1105524345

COFFEE_FILES = \
	src/webfrontend/ExampleTrayApp.coffee

all: build

include easydb-library/tools/base-plugins.make

build: code # $(SCSS)

code: $(JS) $(L10N)

clean: clean-base
