//const { Client, Intents } = require('discord.js');
//const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

const Discord = require('discord.js');
const intents = new Discord.Intents(32767);
const client = new Discord.Client({ intents });
const config = require('./config.json');
const command = require('./command');

// when the client is ready, run this code
// this event will only trigger one time after logging in
client.once('ready', () => {
	console.log('Ready!');
})

client.on("messageCreate", message => {
	//console.log(message.content);
	//message.reply("Hello!");
	if (!message.content.startsWith(config.prefix)) return;
	const args = message.content.substring(config.prefix.length).split(/ +/);
	console.log(args);
	
	switch(args[0]){
		case "hello":
		message.reply("Hello!");
		break;
		
		case "say":
		//console.log(args.slice(1));
		message.reply(args.slice(1).join(" "));
		break;
	}
});

// login to Discord with your app's token
client.login(config.token);