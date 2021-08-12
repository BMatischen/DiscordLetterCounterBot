const { prefix } = require('./config.json');



//Export function with parameter client (bot), alaises (commands), callback (function)
module.exports = (client, aliases, callback) => {
	if (typeof aliases === 'string'){
		aliases = [aliases]
	}
	
	client.on('message', message => {
		const { content } = message;
		
		aliases.forEach(alias => {
			const command = '${prefix}${alias}'
			
			if (content.startsWith('${command} ') || content === command){
				console.log('Run ${command}')
				callback(message)
			}
		})
	})
}