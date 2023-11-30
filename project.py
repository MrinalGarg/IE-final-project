import mip
# d = [[0,1,2,3,4,6,8],
# 	 [0,1,2,3,4,5,6,7],
# 	 [0,1,2,3,4,6,7],
# 	 [0,1,2,3,4,6,7],
# 	 [0,1,2,3,4,5,6,7],
# 	 [1,4,6],
# 	 [0,1,2,3,4,5,6,7],
# 	 [1,2,3,4,6],
# 	 [0,8]]
# costi= [1,2,3,4,5,6,7,8,9]
# costs= [0.5,1,1.5,2,2.5,3,3.5,4,4.5]
# allowed = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
# demand= [[9,8,7,6,5,4,3,2,1,0],[8,7,6,5,4,3,2,1,0,9],[7,6,5,4,3,2,1,0,9,8],
# [6,5,4,3,2,1,0,9,8,7],[5,4,3,2,1,0,9,8,7,6],[4,3,2,1,0,9,8,7,6,5],[3,2,1,0,9,8,7,6,5,4],[2,1,0,9,8,7,6,5,4,3],[1,0,9,8,7,6,5,4,3,2]]
# budget = int(3)
d = [[1],[0]]
costi= [1,1]
costs= [0,0]
allowed = [1,1]
demand= [[1],[2]]
budget = int(1)
n = len(d) # number of nodes
k = len(demand[0]) #number of items
M=10 # allowed[i]*M is the max number of items that can be kept at the ith node
superdemand = [[0 for _ in range(k)] for _ in range(n)]
for i in range(n):
	for j in range(k):
		for l in range(len(d[i])):
			superdemand[i][j]+=demand[d[i][l]][j] # superdemand[i][j] is the sum of the demand of all the nodes in range of jth item for ith node

V = range(n) # nodes
m = mip.Model(solver_name="CBC")

r = [m.add_var(var_type='C', name=f'x_{i}') for i in range(n)] # 1 if ith node has instamart otherwise 0
x = [m.add_var(var_type=mip.BINARY, name=f'x_{i}') for i in range(n)] # x=r
y = [[m.add_var(var_type='C', name=f'y_{i}_{j}') for j in range(k)] for i in range(n)] # y[i][j] is the max amount of jth item that can be kept in ith node
z = [[m.add_var(var_type='C', name=f'z_{i}_{j}') for j in range(k)] for i in range(n)] # z[i][j] is the amount of jth item that the ith node is finally supplying, so , obviously z[i][j]<=y[i][j]
jalu = [m.add_var(var_type='C', name=f'jalu_{i}')for i in range(n)] # amount of items ith node is finally supplying
nihar = [m.add_var(var_type='C', name=f'nihar_{i}')for i in range(n)]
q = [m.add_var(var_type='C', name=f'q')] # total cost of installation of all the instamarts 
#Z is the minimum of max demand or max supply
for i in range(n):
	r[i]=m.var_by_name(f'x_{i}').x
#print(x[0])

for i in range(n):
	for j in range(k):
		superdemand[i][j]=0
for i in range(n):
	for j in range(k):
		# z[i][j] = min(superdemand[i][j], y[i][j])
		m+= z[i][j]<=superdemand[i][j] #wannabe maxdemand on that node
		m+= z[i][j]<=y[i][j]*M#wannabe maxsupply
for i in range(n):
	jalu[i]=mip.xsum(z[i][j] for j in range(k))#jalu[i] is the sum of all zs over all the items of one instamart

for i in range(n):
	m+= mip.xsum(y[i][j] for j in range(k)) <= x[i]*k #if there is an instamart x[i] becomes 1

for i in range(n):
	m+= mip.xsum(y[i][j] for j in range(k)) <= allowed[i]*k#total instamart through all the items is acc to the allowed i
	# q is the total cost of installation of all the instamarts
q = mip.xsum(x[i]*costi[i] for i in range(n)) + mip.xsum(costs[i]*(mip.xsum(y[i][j] for j in range(k))/k) for i in range(n))#costi is the basic cost incurred upon construction and costs[i] is the slope further
m+= q <= budget#total cost<=budget
for i in V:#set of nodes
    m += mip.xsum(x[d[i][j]] for j in range(len(d[i]))) <= 1#no intersection
for i in range(n):
	nihar[i]<=jalu[i]
	nihar[i]<=x[i]*M*n*k
#objective function::max(if instamart maximize jalu-cost....maximising profit) 
m.objective = mip.maximize(mip.xsum(nihar[i] for i in range(n))-q)
solver_status = m.optimize()
objective_value= m.objective_value
print(f"Estimated future profit: {objective_value}")
for i in range(n):
	var_value = m.var_by_name(f'x_{i}').x
	print(f"Value of var_name: {var_value} _ {i}")