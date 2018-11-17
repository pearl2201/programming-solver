import asyncio
import bottom
import math
import argparse



def ep1(ep,bot,message):
	if '/' in message:
		try:
			x,y = [float(x) for x in message.split('/')]
			ret =  math.sqrt(x)*y
			print ("message: %s -- result: %f" %(message,ret))		
			bot.send('PRIVMSG', target='Candy', message="!%s -rep %.2f" %(ep,ret))
		except Exception as e:
			print ("Exception: %s from message: %s" %(e, message))
	else:
		print ("message: %s" %message)
		if 'password' in message:
			bot.disconnect()
			
def ep2(ep,bot,message):
	import base64
	print ("message: %s" %message)
	if 'password' in message:
		bot.disconnect()
		bot.loop.stop()
		return
	try:
		reply  = base64.b64decode(message).decode('utf-8')
		ret = "!ep2 -rep %s" %(reply)
		print (ret)
		bot.send('PRIVMSG', target='Candy', message=ret)

	except Exception as e:
		print ("%s" %e)
		bot.disconnect()

		# Signal a stop before disconnecting so that any reconnect
		# coros aren't run by the last run_forever sweep.
		bot.loop.stop()
		
def ep3(ep,bot,message):
	import codecs
	print ("message: %s" %message)
	if 'password' in message:
		bot.disconnect()
		bot.loop.stop()
		return
	try:
		reply  = codecs.decode(message,'rot_13')
		ret = "!ep3 -rep %s" %(reply)
		print (ret)
		bot.send('PRIVMSG', target='Candy', message=ret)

	except Exception as e:
		print ("%s" %e)
		bot.disconnect()

		# Signal a stop before disconnecting so that any reconnect
		# coros aren't run by the last run_forever sweep.
		bot.loop.stop()
		
def ep4(ep,bot,message):
	import base64
	import zlib
	print ("message: %s" %message)
	if 'password' in message:
		bot.disconnect()
		bot.loop.stop()
		return
	try:
		reply  = zlib.decompress(base64.b64decode(message)).decode('utf-8')
		ret = "!ep4 -rep %s" %(reply)
		print (ret)
		bot.send('PRIVMSG', target='Candy', message=ret)

	except Exception as e:
		print ("%s" %e)
		bot.disconnect()

		# Signal a stop before disconnecting so that any reconnect
		# coros aren't run by the last run_forever sweep.
		bot.loop.stop()
	

solutions = {
	'ep1':ep1,
	'ep2':ep2,
	'ep3':ep3,
	'ep4':ep4
}
			
parser = argparse.ArgumentParser("Parse data for Root me")
parser.add_argument('-ep',type=str, 
                    help='file excel name', required=True)
args = parser.parse_args()


host = 'irc.root-me.org'
port = 6697
ssl = True

NICK = "pearl2203"
CHANNEL = "#root-me_challenge"

bot = bottom.Client(host=host, port=port, ssl=ssl)

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
	bot.send('NICK', nick=NICK)
	bot.send('USER', user=NICK,
             realname='https://github.com/numberoverzero/bottom')

    # Don't try to join channels until the server has
    # sent the MOTD, or signaled that there's no MOTD.
	done, pending = await asyncio.wait(
        [bot.wait("RPL_ENDOFMOTD"),
         bot.wait("ERR_NOMOTD")],
        loop=bot.loop,
        return_when=asyncio.FIRST_COMPLETED
	)

    # Cancel whichever waiter's event didn't come in.
	for future in pending:
		future.cancel()

	bot.send('JOIN', channel=CHANNEL)
	bot.send('PRIVMSG', target='Candy', message='!%s' %args.ep)
	print ("Send message success")
	
@bot.on('PING')
def keepalive(message, **kwargs):
    bot.send('PONG', message=message)
	
@bot.on('PRIVMSG')
def message(nick, target, message, **kwargs):
	""" Echo all messages """

	# Don't echo ourselves
	if nick == NICK:
		return
	# Respond directly to direct messages
	print ("nick: %s - target: %s - messsage: %s" %(nick,target, message))
	if nick == 'Candy':
		solutions[args.ep](args.ep,bot, message)
		
		
bot.loop.run_until_complete(bot.connect())
bot.loop.run_forever()