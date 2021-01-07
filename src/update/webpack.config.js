const path = require('path');
const directory = path.join(__dirname, '../../build')

module.exports = {
	mode: 'production',
	entry: './src/update/ExampleUpdate.coffee',
	output: {
		path: path.resolve(directory, 'update'),
		filename: 'example-update.js',
		library: 'ExampleUpdate',
		libraryTarget: 'umd',
		globalObject: 'this'
	},
	module: {
		rules: [
			{
				test: /\.coffee$/,
				loader: 'coffee-loader',
			},
		],
	},
};
