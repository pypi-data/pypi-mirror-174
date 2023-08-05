
# 連立方程式/不等式の求解ライブラリ [equid]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
# 連立方程式/不等式の求解ライブラリ [equid]
equid = load_develop("equid", "../", develop_flag = True)

# import equid as eq
eq = equid

# 求解
res = eq.solve(cond = (eq.x ** 2 == -1))
print(res)
res = eq.solve(cond = (eq.x ** 2 - 10 * eq.x + 21 == 0))
print(res)
res = eq.solve(cond = (3 * eq.x - eq.y == 0),
	loss = (eq.y - 1) ** 2)
print(res)
cond = (
	(3 * eq.x - eq.y == 1) &
	(2 * eq.x + 5 * eq.y == 12)
)
res = eq.solve(cond = cond)
print(res)
# 局所解があるので残念ながら解けない例
cond = (
	((eq.x ** 2 - 10 * eq.x + 21)*(1/100) == 0) &
	(eq.x >= 4)
)
res = eq.solve(cond = cond)
print(res)
sys.exit()

# import random
# var_ls = ["x_%d"%i for i in range(30)]
# loss = 0
# for var_name in var_ls:
# 	loss += (19 * eq[var_name] - random.random()) ** 4

# diff_loss_vec = [
# 	loss.diff(var_name, simplify = False)
# 	for var_name in var_ls
# ]

# sout(diff_loss_vec, None)
# print(len(str(diff_loss_vec)))	# 74190 -> 1430
# sys.exit()

# f = (eq.x ** 3).diff("x").diff("x")
# print(f)
# print(f(x = 5))

# sys.exit()
########## 以下、最適化のテスト

# 3 * x == 6
loss = (19 * eq.x - 7) ** 4

def func(arg_vec):
	x = arg_vec[0]
	return loss.fix(x = x)

import scipy
res = scipy.optimize.minimize(
	func, [0], method = "Powell")
print(res)
print("■■■■■■■■■■■")

diff_loss = loss.diff("x")

def jac(arg_vec):
	value = diff_loss.fix(x = arg_vec[0])
	return [value]

res = scipy.optimize.minimize(
	func, [0], jac = jac, method = "Newton-CG")
print(res)
print("■■■■■■■■■■■")
res = scipy.optimize.minimize(
	func, [0], jac = jac, method = "BFGS")
print(res)
print("■■■■■■■■■■■")


import random
var_ls = ["x_%d"%i for i in range(60)]
loss = 0
for var_name in var_ls:
	loss += (19 * eq[var_name] - random.random()) ** 4

# 各変数の束縛値辞書の生成
def gen_value_dic(arg_vec):
	return {
		var_name: arg_vec[idx]
		for idx, var_name in enumerate(var_ls)
	}

def func(arg_vec):
	# 各変数の束縛値辞書の生成
	value_dic = gen_value_dic(arg_vec)
	return loss.fix(**value_dic)

diff_loss_vec = [
	loss.diff(var_name)
	for var_name in var_ls
]

def jac(arg_vec):
	# 各変数の束縛値辞書の生成
	value_dic = gen_value_dic(arg_vec)
	# 各偏微分に変数を束縛して返す
	return [
		one_diff.fix(**value_dic)
		for one_diff in diff_loss_vec
	]

x0 = [0 for _ in var_ls]

res = scipy.optimize.minimize(
	func, x0, jac = jac, method = "BFGS")
print("■■■■■■■■■■■")
res = scipy.optimize.minimize(
	func, x0, method = "Powell")
print("■■■■■■■■■■■")
