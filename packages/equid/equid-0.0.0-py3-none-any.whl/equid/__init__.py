
# 連立方程式/不等式の求解ライブラリ [equid]

import sys
import scipy
import random
from sout import sout

# 条件式 (conditional expression) の演算子一覧
cond_exp_operators = ["==", ">=", "and", "or"]
# 数値式 (numerical expression) の演算子一覧
num_exp_operators = ["+", "-", "neg", "*", "**", "min", "max", "unit_step"]

# 条件式 / 数値式 を判別
def judge_exp_type(formula):
	if type(formula) == type(True): return "cond_exp"
	if type(formula) != Formula: return "num_exp"
	if formula._type in num_exp_operators: return "num_exp"
	if formula._type in cond_exp_operators: return "cond_exp"
	# 未定義の演算子の場合
	raise Exception("[equid error] invalid formula type.")

# 条件式をlossの形に変換
def cond_to_loss(cond):
	if cond._type == "==":
		a, b = cond._args
		cond_loss = (a - b) ** 2
	elif cond._type == ">=":
		a, b = cond._args
		cond_loss = Formula("max", b - a, 0)
	elif cond._type == "and":
		a, b = cond._args
		cond_loss = cond_to_loss(a) + cond_to_loss(b)
	elif cond._type == "or":
		a, b = cond._args
		cond_loss = cond_to_loss(a) * cond_to_loss(b)
	else:
		raise Exception("[equid error] unsupported operator.")
	return cond_loss

# scipyによる最適化
def scipy_opt(loss_formula, x0, var_ls, method):
	# ベクトルを変数辞書に変換
	def vec_to_dic(arg_vec):
		return {var_name: value
			for var_name, value in zip(var_ls, arg_vec)}
	# 最適化対象関数
	def opt_func(arg_vec):
		return Formula.fix(loss_formula, **vec_to_dic(arg_vec))
	# 各変数での偏微分
	diff_loss_vec = [
		loss_formula.diff(var_name)
		for var_name in var_ls]
	# ヤコビアン
	def jac(arg_vec):
		return [Formula.fix(one_diff, **vec_to_dic(arg_vec))
			for one_diff in diff_loss_vec]
	# x0の形式を変換
	x0_vec = [x0[var_name] for var_name in var_ls]
	# scipyによる最適化
	scipy_res = scipy.optimize.minimize(
		opt_func, x0_vec, jac = jac, method = method)
	# 結果の形式変換
	opt_res = {var_name: float(e)
		for var_name, e in zip(var_ls, scipy_res.x)}
	return opt_res

# 数式型のクラスメソッドの定義
class MetaFormula(type):
	# 単独変数の生成
	def var(cls, var_name):
		return Formula("var", var_name)
	# 単独変数の生成 (略記)
	def __getitem__(cls, var_name):
		return Formula.var(var_name)
	# 単独変数の生成 (略記その2)
	def __getattr__(cls, var_name):
		return Formula.var(var_name)
	# 求解
	def solve(cls,
		cond,	# 条件式 (真理値を返す型)
		x0 = "norm_rand",	# 初期値 (辞書指定, "norm_rand"指定で標準正規乱数が初期値になる, "zeros"指定で自動的に全変数ゼロになる)
		loss = 1,	# loss関数 (省略可能; condが満たされる中でできるだけlossの小さい解を見つける)
		method = "BFGS",	# 求解に用いる最適化手法 (BFGS, ...)
		cond_alpha = 1e6,	# cond_lossをlossに対してどれだけ優先するかの係数
		cond_eps = 1e-5	# 条件が満たされているとする許容誤差
	):
		# cond, lossの型チェック
		if judge_exp_type(cond) != "cond_exp": raise Exception("[equid error] The cond must be a conditional expression, not an expression that returns a number. (e.g. x - 3 == 7)")	# 条件式 / 数値式 を判別
		if judge_exp_type(loss) != "num_exp": raise Exception("[equid error] The loss must be a numerical expression, not a conditional expression. (e.g. (x - 3) ** 2)")	# 条件式 / 数値式 を判別
		# 条件式をlossの形に変換
		cond_loss = cond_to_loss(cond)
		# lossを合成
		concat_loss = Formula.simplify(loss + cond_alpha * cond_loss)
		# 変数列挙
		var_ls = Formula.listup_vars(concat_loss)	# 全変数列挙
		# x0 の特殊指定の解決
		if x0 == "zeros": x0 = {var_name: 0 for var_name in var_ls}
		if x0 == "norm_rand": x0 = {var_name: random.gauss(0, 1) for var_name in var_ls}
		# scipyによる最適化
		opt_res = scipy_opt(concat_loss, x0, var_ls, method)
		# condが0かどうかを判別
		if Formula.fix(cond_loss, **opt_res) > cond_eps: return "Solution_Not_Found"
		return opt_res

# 演算子の評価 (arg_valuesは全て数値)
def op_eval(op, *arg_values):
	# 演算子によって分岐
	if op == "+":
		return sum(arg_values)
	elif op == "-":
		a, b = arg_values
		return a - b
	elif op == "neg":
		a, = arg_values
		return -a
	elif op == "*":
		a, b = arg_values
		return a * b
	elif op == "**":
		a, b = arg_values
		return a ** b
	elif op == "min":
		return min(arg_values)
	elif op == "max":
		return max(arg_values)
	elif op == "unit_step":
		a, = arg_values
		return (1 if a > 0 else 0)
	elif op == "==":
		a, b = arg_values
		return (a == b)
	elif op == ">=":
		a, b = arg_values
		return (a >= b)
	elif op == "and":
		a, b = arg_values
		if type(a) != type(True) or type(b) != type(True): raise Exception("[equid error] The and operation can only be performed on bool values.")
		return (a and b)
	elif op == "or":
		a, b = arg_values
		if type(a) != type(True) or type(b) != type(True): raise Exception("[equid error] The or operation can only be performed on bool values.")
		return (a or b)
	else:
		raise Exception("[equid error] invalid operator (%s)."%op)

# 代入 (数値の簡略化は実施せず)
def raw_fix(formula, **kw_args):
	if formula._type == "var":
		# 変数の単項の場合
		var_name = formula._args[0]
		# kw_argsにある場合は束縛値を返す
		if var_name in kw_args:
			return kw_args[var_name]
		# ない場合はそのまま返す
		return formula
	else:
		# 再帰的にfix
		return Formula(formula._type, *[
			(raw_fix(e, **kw_args) if type(e) == Formula else e)
			for e in formula._args
		])

# 微分 (数値の簡略化は実施せず)
def raw_diff(formula, var_name):
	# 数値の場合
	if type(formula) != Formula: return 0
	# 演算子で分岐
	if formula._type == "var":
		a, = formula._args
		if a == var_name: return 1
		return 0
	elif formula._type == "+":
		return Formula("+", *[
			raw_diff(e, var_name)
			for e in formula._args
		])
	elif formula._type == "-":
		a, b = formula._args
		return Formula("-",
			raw_diff(a, var_name),
			raw_diff(b, var_name),
		)
	elif formula._type == "neg":
		a, = formula._args
		return Formula("neg", raw_diff(a, var_name))
	elif formula._type == "*":
		a, b = formula._args
		return Formula("+",
			Formula("*", raw_diff(a, var_name), b),
			Formula("*", a, raw_diff(b, var_name)),
		)
	elif formula._type == "**":
		a, b = formula._args
		if type(b) == Formula: raise Exception("[equid error] The derivative of an expression with a variable in the exponential part of the power is not supported in the current version.")
		return Formula("*",
			Formula("*", b, Formula("**", a, b - 1)),
			raw_diff(a, var_name)
		)
	elif formula._type == "max":
		a, b = formula._args
		return Formula("+",
			Formula("*", raw_diff(a, var_name), Formula("unit_step", Formula("-", a, b))),
			Formula("*", raw_diff(b, var_name), Formula("unit_step", Formula("-", b, a))),
		)
	else:
		raise Exception("[equid error] invalid type formula.")

# 数式簡略化ルール (プロトタイプ宣言: 定義部は後述)
simplify_rules = {}

# テンプレートマッチング
def template_matching(formula, template):
	# typeも含むタプル
	ele_ls = (formula._type, ) + formula._args
	# 一致を見る
	if len(ele_ls) != len(template): return None
	ret_dic = {}
	for e, t in zip(ele_ls, template):
		# テンプレートの場合: 無条件受理
		if type(t) == type("") and t.startswith("_TMP_"):
			ret_dic[t] = e
			continue
		# 受理しない場合を弾く
		if type(e) == Formula:
			return None
		else:
			if e != t: return None	# eがFormulaではないため、==で一致を判定できる
	return ret_dic

# 再帰的に変数をリストアップし、辞書に登録
def rec_listup_vars(formula, listup_pool):
	# Formula型以外の場合は無視
	if type(formula) != Formula: return None
	# 変数型の場合は登録 (再帰終了条件)
	if formula._type == "var":
		var_name = formula._args[0]
		listup_pool[var_name] = True
	# 再帰的にlistup
	for e in formula._args:
		rec_listup_vars(e, listup_pool)

# 数式型
class Formula(metaclass = MetaFormula):
	# 初期化処理
	def __init__(self, _type, *_args):
		self._type = _type	# 種類
		self._args = _args	# 値を規定するもの
	# 代入 (変数固定)
	def fix(self, simplify = True, **kw_args):
		if type(self) != Formula: return self	# Formula.fix(23)のような呼ばれ方の場合の処理
		# 代入 (数値の簡略化は実施せず)
		raw_res = raw_fix(self, **kw_args)
		# 簡略化しない場合
		if simplify is False: return raw_res
		# 数値の簡略化
		if type(raw_res) != Formula: return raw_res
		return raw_res.simplify()
	# 代入 (変数固定) の略記
	def __call__(self, **kw_args):
		return self.fix(**kw_args)
	# 文字列化
	def __str__(self):
		ele_ls = [self._type] + list(self._args)
		return "(%s)"%(" ".join([
			str(e) for e in ele_ls	# 再帰呼び出し
		]))
	# 文字列化 その2
	def __repr__(self):
		return str(self)
	# 微分
	def diff(self, var_name, simplify = True):
		if type(self) != Formula: return 0	# Formula.diff(23)のような呼ばれ方の場合の処理
		# 微分 (数値の簡略化は実施せず)
		raw_res = raw_diff(self, var_name)
		# 簡略化しない場合
		if simplify is False: return raw_res
		# 数値の簡略化
		if type(raw_res) != Formula: return raw_res
		return raw_res.simplify()
	# 数値の簡略化
	def simplify(self):
		if type(self) != Formula: return self	# Formula.simplify(23)のような呼ばれ方の場合の処理
		# varはそのまま返す
		if self._type == "var": return self
		# argsを再帰的にsimplifyしておく
		simplified_args = [
			Formula.simplify(e) for e in self._args]
		# argsが数値だけで構成されている場合は評価して返す
		types = [type(e) for e in simplified_args]
		if Formula not in types:
			return op_eval(self._type, *simplified_args)	# 演算子の評価 (arg_valuesは全て数値)
		# simplify_rulesを適用
		args_simple_f = Formula(self._type, *simplified_args)
		for template in simplify_rules:
			# テンプレートマッチング
			res = template_matching(args_simple_f, template)
			# マッチしない場合はスキップ
			if res is None: continue
			# マッチする場合は置き換え
			post_f = simplify_rules[template]
			if type(post_f) != Formula: return post_f	# 数値の場合はそのまま返す
			return post_f.fix(**res, simplify = False)
		# どのルールも適用されなかった場合
		return args_simple_f
	# 全変数列挙
	def listup_vars(self):
		if type(self) != Formula: return []	# Formula.listup_vars(23)のような呼ばれ方の場合の処理
		listup_pool = {}
		# 再帰的に変数をリストアップし、辞書に登録
		rec_listup_vars(self, listup_pool)
		# まとめて返す
		var_ls = list(listup_pool)
		return var_ls
	# 演算子
	def __add__(self, e): return Formula("+", self, e)	# 加算
	def __sub__(self, e): return Formula("-", self, e)	# 減算
	def __mul__(self, e): return Formula("*", self, e)	# 乗算
	def __pow__(self, e): return Formula("**", self, e)	# べき乗
	def __and__(self, e): return Formula("and", self, e)	# 条件式同士の論理積
	def __or__(self, e): return Formula("or", self, e)	# 条件式同士の論理和
	def __ge__(self, e): return Formula(">=", self, e)	# 比較演算子
	def __eq__(self, e): return Formula("==", self, e)	# 同一性演算子 (__req__というものはなく、__eq__自身が呼ばれる)
	def __neg__(self): return Formula("neg", self)	# 負号
	def __radd__(self, e): return Formula("+", e, self)	# 加算 (逆向き)
	def __rsub__(self, e): return Formula("-", e, self)	# 減算 (逆向き)
	def __rmul__(self, e): return Formula("*", e, self)	# 乗算 (逆向き)
	def __rpow__(self, e): return Formula("**", e, self)	# べき乗 (逆向き)
	def __rand__(self, e): return Formula("and", e, self)	# 条件式同士の論理積 (逆向き)
	def __ror__(self, e): return Formula("or", e, self)	# 条件式同士の論理和 (逆向き)

# 数式簡略化ルール (定義順の関係上ここに記載)
simplify_rules[("+", "_TMP_0", 0)] = Formula._TMP_0
simplify_rules[("+", 0, "_TMP_0")] = Formula._TMP_0
simplify_rules[("*", "_TMP_0", 1)] = Formula._TMP_0
simplify_rules[("*", 1, "_TMP_0")] = Formula._TMP_0
simplify_rules[("*", "_TMP_0", 0)] = 0
simplify_rules[("*", 0, "_TMP_0")] = 0
simplify_rules[("**", "_TMP_0", 0)] = 1
simplify_rules[("**", "_TMP_0", 1)] = Formula._TMP_0
simplify_rules[("*", "_TMP_0", -1)] = Formula("neg", Formula._TMP_0)
simplify_rules[("*", -1, "_TMP_0")] = Formula("neg", Formula._TMP_0)
simplify_rules[("-", "_TMP_0", "_TMP_1")] = Formula("+", Formula._TMP_0, Formula("neg", Formula._TMP_1))

# 呼び出しの準備
sys.modules[__name__] = Formula	# モジュールオブジェクトと「Formula」クラスを同一視
