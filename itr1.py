import mip
d = ((0,1,2,3,4,6,8),
	 (0,1,2,3,4,5,6,7),
	 (0,1,2,3,4,6,7),
	 (0,1,2,3,4,6,7),
	 (0,1,2,3,4,5,6,7),
	 (1,4,6),
	 (0,1,2,3,4,5,6,7),
	 (1,2,3,4,6),
	 (0,8))

n = len(d)
V = range(n)
m = mip.Model(solver_name="CBC")

x = [m.add_var(var_type=mip.BINARY, name=f'x_{i}') for i in range(n)]
wout = [m.add_var(var_type=mip.BINARY, name=f'wout_{i}') for i in range(n)]
win = [m.add_var(var_type=mip.BINARY, name=f'win_{i}') for i in range(n)]
for i in V:
    m += mip.xsum(x[d[i][j]] for j in range(len(d[i]))) >= 1

m.objective = mip.minimize(mip.xsum(
    x[i]
    for i in range(n)
))
solver_status = m.optimize()
objective_value= m.objective_value
print(f"Estimated future profit: {objective_value}")
for i in range(n):
	var_value = m.var_by_name(f'x_{i}').x
	print(f"Value of var_name: {var_value} _ {i}")