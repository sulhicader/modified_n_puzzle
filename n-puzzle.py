import sys
import time
x = sys.argv[1]
y = sys.argv[2]

xfo = open( x , 'r')
yfo = open( y , 'r')

xfo = xfo.read()
yfo = yfo.read()

instate = xfo.split('\n')
for i in range(len(instate)):
	m = instate[i].split("\t")
	m[-1] = m[-1][0]
	instate[i] = m
del(m)
finalstate = yfo.split('\n')
for j in range(len(finalstate)):
	m = finalstate[j].split("\t")
	m[-1] = m[-1][0]
	finalstate[j] = m
del(m)
def is_goal_state(in_map , out_map):
	return in_map==out_map

def hamming( grid, target):
	dim = len(instate)
	counter = 0;
	for i in range(dim):
		for j in range(dim):
			if (not (grid[i][j] == target[i][j] or target[i][j] == '-')):
				counter += 1;
	return (counter);

def manhattan( grid, target):
	dim = len(instate)
	result = 0;
	for i in range (dim):
		for j in range (dim):
			if (target[i][j] == '-'):
				continue;
			cou = 0
			for l in range (dim):
				for m in range (dim):
					if (target[i][j] == grid[l][m]):
						result += (abs (m - j) + abs (l - i));
						cou = 1
						break;
				if cou==1:
					break;
	return result
class State:
	def __init__(self ,curstate ,  step_seq , h_type , cost_to_n):
		self.cost_to_n = cost_to_n
		self.step_seq = step_seq
		self.curstate = curstate
		if h_type=='manhattan':
			self.heu_cost = manhattan(self.curstate , finalstate)
		elif h_type=='hamming':
			self.heu_cost = hamming(self.curstate , finalstate)

	def cost(self):
		return self.cost_to_n + self.heu_cost

	def makesuccessors(self):
		temp_list = []
		cords = []
		for i in range(len(self.curstate)):
			for j in range(len(self.curstate[0])):
				if self.curstate[i][j]=='-':
					tt = [[i,j]]
					t = [[i-1,j,'down'],[i+1,j,'up'],[i,j-1,'right'],[i,j+1,'left']]
					for m in t:
						if -1 not in m and len(self.curstate) not in m:
							tt.append(m)
					cords.append(tt)

		for i in range(2):
			for j in range(1,len(cords[i])):
				t1 = self.curstate[cords[i][j][0]][cords[i][j][1]]
				t2 = self.curstate[cords[i][0][0]][cords[i][0][1]]
				new_state = []
				for o in range(len(self.curstate)):
					tempp = []
					for p in range(len(self.curstate)):
						tempp.append(str(self.curstate[o][p]))
					new_state.append(tempp)
				new_state[cords[i][j][0]][cords[i][j][1]]=t2
				new_state[cords[i][0][0]][cords[i][0][1]]=t1
				count=0
				q=0
				for q in range(len(closed)):
					if closed[q].curstate==new_state:
						count=1
						q=q
						break
				if count==0:
					count1=0
					r=0
					for r in range(len(open_successor)):
						if open_successor[r].curstate==new_state:
							count1=1
							r=r
							break
				if count==0 and count1==0:
					new_seq = self.step_seq+[[t1,cords[i][j][2]]]
					temp_list.append(State(new_state , new_seq,heuristic , self.cost_to_n+1))
				elif count==1:
					if closed[q].cost_to_n>self.cost_to_n+1:
						closed.pop(q)
						new_seq = self.step_seq+[[t1,cords[i][j][2]]]
						temp_list.append(State(new_state , new_seq,heuristic , self.cost_to_n+1))
				elif count1==1:
					if open_successor[r].cost_to_n>self.cost_to_n+1:
						new_seq = self.step_seq+[[t1,cords[i][j][2]]]
						open_successor[q]=State(new_state , new_seq,heuristic , self.cost_to_n+1)

		return temp_list


open_successor =[]
closed =[]
heuristic = 'hamming'
st_state = State(instate, [] , heuristic , 0)
open_successor.append(st_state)
conf = 0
time1  = time.time()
while len(open_successor)!=0:
	mini = float('inf')
	n = 0
	for i in range(len(open_successor)):
		x = open_successor[i].cost()
		if x<mini:
			mini = x
			n = i
	temp_s = open_successor.pop(n)
	if is_goal_state(finalstate , temp_s.curstate):
		conf = 1
		break;
	closed.append(temp_s)
	print temp_s.cost_to_n
	temp_list = temp_s.makesuccessors()
	open_successor += temp_list
	print (len(open_successor))
	print (len(closed))

if conf==1:
	print_list = temp_s.step_seq
	print print_list
	for j in range(len(print_list)):
		print_list[j]=tuple(print_list[j])
	fop= open("Sample_Output.txt","w")
	fop.write(str(print_list)[1:-1])
	fop.close()

else:
	print "failed"

print time.time()-time1