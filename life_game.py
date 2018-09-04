import copy

class Cell():
	def __init__(self,height,width):
		self.coordinate = (height,width)
		self.state = False
		self.data = {
								False:'▓',#dead
								True:'█'#live
								}
								
	def now(self):
		return self.data[self.state]
	
	def __str__(self):
		return self.now()
		
	def __add__(self,y):#これを使って周りを足して条件で状態変化
		if type(self)==type(y):
			return self.state+y.state
		else:
			raise TypeError('Cell requier')
		
class Bace():
	def __init__(self,h=34,w=34):
		self.width = w
		self.height = h
		self.bace = [
			[Cell(h,w) for w in range(self.width)]
				for h in range(self.height)]
		
	def __str__(self):
		temp = '\n'.join([''.join([str(j) for j in i]) for i in self.bace])
		return temp
		
	def __call__(self):
		return self.bace
		
class World():
	def __init__(self,h=34,w=34,loop=False):
		self.index ='0123456789abcdefghijklmnopqrstuvwx'
		self.bace = Bace(h,w)
		self.loop = loop
		self.body = self.__make_body(self.loop)
		
	def __str__(self):
		# XXX : discordで破壊される
		index='•'+self.index
		temp= '\n'.join([index[num+1]+''.join([str(j[0]) for j in i]) for num,i in enumerate(self.body)])
		return index+'\n'+temp
		
	def __make_body(self,flg):
		bace = self.bace
		h_max = bace.height
		w_max = bace.width
		
		body = [
			[
				[
					bace()[h][w],
					[
						bace()[h+s][w+t]
						for s in range(-1,2)
							for t in range(-1,2)
								if -1<h+s< h_max 
								and -1<w+t< w_max 
								and not s==t==0 
								and not None
					]+(
						[]
						if not flg
						else []+(
							[
								bace()[h_max-1][w+t]
									for t in range(-1,2)
										if -1< w+t < w_max
							] if h==0 else []
						)+(
							[
								bace()[0][w+t]
									for t in range(-1,2)
										if -1< w+t < w_max
							] if h==h_max-1 else []
						)+(
							[
								bace()[h+s][w_max-1]
									for s in range(-1,2)
										if -1< h+s < h_max
							] if w==0 else []
						)+(
							[
							bace()[h+s][0]
								for s in range(-1,2)
									if -1< h+s < h_max
							] if w==w_max-1 else []
						)
					)
				] for w in range(bace.width)
			]for h in range(bace.height)]
		# height→width→[cell,[neighboars]]
		return body
		
	def make_step(self):
		next_steps = []
		def do_step(steps=[[],],fix_state=None):
			next_body = copy.deepcopy(self.body)
			nonlocal next_steps
			while True:
				for step in steps:
					if fix_state is None:
						amount=sum(
								[i.state for i in self.body[step[0]][step[1]][1]])
						state=self.law(
							amount,
							self.body[step[0]][step[1]][0].state)
					else:
						state=fix_state
					
					next_body[step[0]][step[1]][0].state = state
					
					next_steps += [
						c.coordinate for c 
						in self.body[step[0]][step[1]][1]
						]+[tuple(step)] if state else[]
					state=None
			
				self.body = copy.deepcopy(next_body)
				steps = list(set(next_steps))
				fix_state=yield str(self)
		return do_step
		
	def law(self,neig,now):
		
		if neig>4:
			return False
		elif 2<= neig <=3:
			if now:
				return True
			else:
				if neig==3:
					return True
				else:
					return False
		else:
			return False
			

def load_set(step_source,cells_set,coord=(0,0)):
	choose_cells = lambda source,select:[
		[h,w] for h,i in enumerate(source) for w,j in enumerate(source[h]) if j==select
	]
	dead_cells = choose_cells(cells_set.split('\n'),'▓')
	living_cells = choose_cells(cells_set.split('\n'),'█')
	step_source([(i[0]+coord[0],i[1]+coord[1]) for i in dead_cells],fix_state=False).__next__()
	return step_source([(i[0]+coord[0],i[1]+coord[1]) for i in living_cells],fix_state=True)