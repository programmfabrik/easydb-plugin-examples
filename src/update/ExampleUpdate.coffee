# This is an example of the updater, using webpack and making a bundle with all the dependencies.
# Webpack configuration is at webpack.config.js

# This is just a random library, just for showing that it is included in the bundle.
exactMath = require('exact-math');

class ExampleUpdate

	__start_update: ({server_config, plugin_config}) ->
		ez5.respondSuccess({
			# NOTE:
			# 'state' object can contain any data the update script might need between updates.
			# the easydb server will save this and send it with any 'update' request
			state: {
				"start_update": new Date().toUTCString()
			}
		})

	__updateData: ({objects, plugin_config}) ->
		timeout = plugin_config.update?.timeout or 0 # This is how we can access to the timeout value.

		value = exactMath.add(5, 5) # This should work.

		# Do something with the objects and keep track of the ones that were updated.
		# In this case I just return that the first one was updated.
		objectsToUpdate = [objects[0]]

		# Finish the update, this should be the last line.
		ez5.respondSuccess({payload: objectsToUpdate})

		# In case of an error, it is possible to use:
#		ez5.respondError("example.update.error.generic", {error: "Some error message"})

	main: (data) ->
		if not data
			ez5.respondError("example.update.error.payload-missing")
			return

		for key in ["action", "server_config", "plugin_config"]
			if (!data[key])
				ez5.respondError("example.update.error.payload-key-missing", {key: key})
				return

		if (data.action == "start_update")
			@__start_update(data)
			return

		else if (data.action == "update")
			if (!data.objects)
				ez5.respondError("example.update.error.objects-missing")
				return

			if (!(data.objects instanceof Array))
				ez5.respondError("example.update.error.objects-not-array")
				return

			# NOTE: state for all batches
			# this contains any arbitrary data the update script might need between batches
			# it should be sent to the server during 'start_update' and is included in each batch
			if (!data.state)
				ez5.respondError("example.update.error.state-missing")
				return

			# NOTE: information for this batch
			# this contains information about the current batch, espacially:
			#   - offset: start offset of this batch in the list of all collected values for this custom type
			#   - total: total number of all collected custom values for this custom type
			# it is included in each batch
			if (!data.batch_info)
				ez5.respondError("example.update.error.batch_info-missing")
				return

			@__updateData(data)
			return
		else
			ez5.respondError("example.update.error.invalid-action", {action: data.action})

module.exports = new ExampleUpdate()