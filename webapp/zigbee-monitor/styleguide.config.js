const path = require('path')

module.exports = {
	// set your styleguidist configuration here
	title: 'ZigBee Monitor App',
	// components: 'src/components/**/[A-Z]*.vue',
	// defaultExample: true,
	// sections: [
	//   {
	//     name: 'First Section',
	//     components: 'src/components/**/[A-Z]*.vue'
	//   }
	// ],
	// webpackConfig: {
	//   // custom config goes here
	// },
	styleguideDir: '../../docs/vue-components',
	exampleMode: 'hide',
	usageMode: 'expand',
	renderRootJsx: path.join(__dirname, 'config/styleguide.root.js')
}
