import life_game
import logging
import discord
import asyncio

def make_world():
	return 
	
world = ...

ind=lambda h,w:(world.index.index(str(h)),world.index.index(str(w)))

add_glider=lambda source,h=0,w=0:source(((h,w),(h,w+2),(h+1,w+1),(h+1,w+2),(h+2,w+1)),fix_state=True)


import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
asyncio.set_event_loop(asyncio.new_event_loop())

client=discord.Client()
owner = None

@client.event
async def on_ready():
	print(f'Logged on as {client.user.name}!')
	global owner
	owner = [await client.application_info()][0].owner
	print(f'owner is {owner}')
	
res=...
flg=True
step_source = ...
step=...
@client.event
async def on_message(msg):
	if msg.author == owner:
		global world,flg,res,step_source,step
		ch = msg.channel
		com = msg.content
		if com == '...make world':
			world = life_game.World(34,34)
			res = await ch.send(f'```{str(world)}```')
			step_source = world.make_step()
		elif com.startswith('...add'):
			com = com[7:]
			if com=='glider':
				step = add_glider(step_source)
				await res.edit(content=f'```{next(step)}```')
			elif com == '':
				await ch.send('wait for cells set')
				msg = await client.wait_for('message',check=lambda msg:msg.author==owner)
				print(msg.content)
				await ch.send('wait for coord')
				coord = await client.wait_for('message',check=lambda msg:msg.author==owner)
				await ch.send('ok')
				step=life_game.load_set(step_source,msg.content,[int(i) for i in coord.content.split()])
				await res.edit(content=f'```{next(step)}```')
		elif com == '...next':
			await res.edit(content=f'```{next(step)}```')
		elif com == '...run':
			flg=True
			async def task():
				await client.wait_until_ready()
				while flg and not client.is_closed():
					await res.edit(content=f'```{next(step)}```')
					await asyncio.sleep(0.3)
			client.loop.create_task(task())
		elif com == '...stop':
			flg=False
		

client.run(token)