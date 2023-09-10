import sys
from fractions import Fraction
from itertools import permutations, product
import typing
from enum import Enum

__author__ = 'Github @customtea'
__version__ = '1.1.0'


class Operator(Enum):
    """Operator

    Parameters
    ----------
    Enum : int
    """
    NOP = 0
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4


class RPNCalc():
    """Reverse Polish Notation Calculator
    """
    def __init__(self) -> None:
        self.__stack: typing.List[Fraction] = []
        self.__formula: typing.List[str] = []

    def reset(self) -> None:
        """Reset Stack
        """
        self.__stack.clear()
        self.__formula.clear()
    
    def __push_num(self, num: Fraction) -> None:
        self.__stack.append(num)
        self.__formula.append(str(num.numerator))
    
    def __pre_calc(self) -> typing.Tuple[Fraction, Fraction]:
        num2 = self.__stack.pop()
        num1 = self.__stack.pop()
        return num1, num2
    
    def __plus(self) ->None:
        num1, num2 = self.__pre_calc()
        self.__stack.append(num1 + num2)
        self.__formula.append("+")
    
    def __minus(self) -> None:
        num1, num2 = self.__pre_calc()
        self.__stack.append(num1 - num2)
        self.__formula.append("-")

    def __times(self) -> None:
        num1, num2 = self.__pre_calc()
        self.__stack.append(num1 * num2)
        self.__formula.append("*")

    def __divide(self) -> None:
        num1, num2 = self.__pre_calc()
        try:
            t = num1 / num2
            self.__stack.append(t)
            self.__formula.append("/")
        except ZeroDivisionError:
            # とりあえず何もせず潰す
            # たぶん十中八九最後で破綻するので，実質無視される
            self.__push_num(num1)
            self.__push_num(num2)
    
    def result(self) -> typing.Union[None, Fraction]:
        """Calculation Result

        Returns
        -------
        typing.Union[None, Fraction]
            結果そのもの
            エラーはNoneを返す
        """
        if len(self.__stack) != 1:
            return None
        return self.__stack.pop()
    
    def postfix_formula(self) -> str:
        """postfix formula

        Returns
        -------
        str
            後置記法を出力する
        """
        return " ".join(self.__formula)
    
    def infix_formula(self) -> str:
        tmp_stack = []
        for op in self.__formula:
            if op == "+":
                f2 = tmp_stack.pop()
                f1 = tmp_stack.pop()
                tmp_stack.append(f"({f1} + {f2})")
            elif op == "-":
                f2 = tmp_stack.pop()
                f1 = tmp_stack.pop()
                tmp_stack.append(f"({f1} - {f2})")
            elif op == "*":
                f2 = tmp_stack.pop()
                f1 = tmp_stack.pop()
                tmp_stack.append(f"{f1} * {f2}")
            elif op == "/":
                f2 = tmp_stack.pop()
                f1 = tmp_stack.pop()
                tmp_stack.append(f"{f1} / {f2}")
            else:
                tmp_stack.append(str(op))
        return tmp_stack[0]

    def push(self, op: typing.Union[Operator, Fraction]) -> None:
        """push calculation

        Parameters
        ----------
        op : typing.Union[Operator, Fraction]
            値または演算子(OperatorのEnumで定義されたもの)
        """
        if type(op) == Fraction:
            self.__push_num(op)
            return None
        if op == Operator.NOP:
            return None
        elif op == Operator.PLUS:
            self.__plus()
        elif op == Operator.MINUS:
            self.__minus()
        elif op == Operator.TIMES:
            self.__times()
        elif op == Operator.DIVIDE:
            self.__divide()
        else:
            return None





def calc_operator(op: Operator, num1: Fraction, num2: Fraction) -> typing.Union[Fraction, None]:
    # print(op.name)
    if op == Operator.NOP:
        return None
    elif op == Operator.PLUS:
        return num1 + num2
    elif op == Operator.MINUS:
        return num1 - num2
    elif op == Operator.TIMES:
        return num1 * num2
    elif op == Operator.DIVIDE:
        return num1 / num2
    else:
        return None


def view_op(op: Operator) -> str:
    # print(op.name)
    if op == Operator.NOP:
        return ""
    elif op == Operator.PLUS:
        return "+"
    elif op == Operator.MINUS:
        return "-"
    elif op == Operator.TIMES:
        return "*"
    elif op == Operator.DIVIDE:
        return "/"
    else:
        return ""


def solve(targetnum: Fraction, numlist: typing.List[Fraction]):
    """solver ver01

    Parameters
    ----------
    targetnum : Fraction
        目標の値
    numlist : typing.List[Fraction]
        数値の配列
    
    Note
    ----
    最初のソルバ，先頭から順に処理する．
    結果の出力は，中置記法っぽい（カッコ記号はつかない）
    
    """
    opl = [Operator.PLUS, Operator.MINUS, Operator.TIMES, Operator.DIVIDE]
    op_all = product(opl, repeat=len(numlist)-1)
    # print(op_all)
    num_all = permutations(numlist)
    for num in num_all:
        # print(num)
        for op in product(opl, repeat=len(numlist)-1):
            # print(op)
            res = calc_operator(op[0], num[0], num[1])
            if res == None:
                continue
            else:
                for index in range(2, len(numlist)):
                    res = calc_operator(op[index-1], res, num[index])
                    if res == None:
                        break
            # print("RESULT:", res)
            if targetnum == res:
                print("RESULT:    ", end="")
                print(f"{num[0]} {view_op(op[0])} {num[1]}", end="")
                for index in range(2, len(numlist)):
                    print(f" {view_op(op[index-1])} {num[index]}", end="")
                print()
                exit(0)


def solve2nd(targetnum: Fraction, numlist: typing.List[Fraction]):
    """solver ver02

    Parameters
    ----------
    targetnum : Fraction
        目標の値
    numlist : typing.List[Fraction]
        数値の配列
    
    Note
    ----
    カッコ問題を（それっぽく）解決したソルバ
    たぶん解けないケースもある気がする
    逆ポーランド記法を使うことによって，パターンをそこまで考えなくて良くなった．
    本当はもっと自動拡張できるはずだけど，とりあえずありそうなパターンを3つ用意した．
    （数学できない人なので）
    """
    opl = [Operator.PLUS, Operator.MINUS, Operator.TIMES, Operator.DIVIDE]
    # op_all = product(opl, repeat=len(numlist)-1)
    # print(op_all)
    num_all = permutations(numlist)
    size_number = len(numlist)
    for num in num_all:
        # print(num)
        for op in product(opl, repeat=size_number - 1):
            rpn = RPNCalc()
            # print(op)
            rpn.push(num[0])
            rpn.push(num[1])
            rpn.push(op[0])
            for index in range(2, len(numlist)):
                rpn.push(num[index])
                rpn.push(op[index-1])
            # print("RESULT:", res)
            res = rpn.result()
            if res == None:
                continue
            if targetnum == res:
                print(f"RESULT TYPE1:    {rpn.postfix_formula()}")
                print(f"RESULT TYPE1:    {rpn.infix_formula()}")
                exit(0)

        if len(numlist) % 2 == 0:
            for op in product(opl, repeat=size_number - 1):
                rpn = RPNCalc()
                # print(op)
                rpn.push(num[0])
                rpn.push(num[1])
                rpn.push(op[0])
                for index in range(2, size_number, 2):
                    rpn.push(num[index])
                    rpn.push(num[index+1])
                    rpn.push(op[index-1])
                    rpn.push(op[index])
                # print("RESULT:", res)
                res = rpn.result()
                if res == None:
                    continue
                if targetnum == res:
                    print(f"RESULT TYPE2-1:    {rpn.postfix_formula()}")
                    print(f"RESULT TYPE2-1:    {rpn.infix_formula()}")
                    exit(0)
        else:
            for op in product(opl, repeat=size_number - 1):
                rpn = RPNCalc()
                # print(op)
                rpn.push(num[0])
                rpn.push(num[1])
                rpn.push(op[0])
                for index in range(2, size_number-1, 2):
                    rpn.push(num[index])
                    rpn.push(num[index+1])
                    rpn.push(op[index-1])
                    rpn.push(op[index])
                rpn.push(num[-1])
                rpn.push(op[-1])
                # print("RESULT:", res)
                res = rpn.result()
                if res == None:
                    continue
                if targetnum == res:
                    print(f"RESULT TYPE2-2:    {rpn.postfix_formula()}")
                    print(f"RESULT TYPE2-2:    {rpn.infix_formula()}")
                    exit(0)

        for op in product(opl, repeat=size_number - 1):
            rpn = RPNCalc()
            # print(op)
            rpn.push(num[0])
            rpn.push(num[1])
            rpn.push(num[2])
            rpn.push(op[0])
            rpn.push(op[1])
            for index in range(3, len(numlist)):
                rpn.push(num[index])
                rpn.push(op[index-1])
            # print("RESULT:", res)
            res = rpn.result()
            if res == None:
                continue
            if targetnum == res:
                print(f"RESULT TYPE3:    {rpn.postfix_formula()}")
                print(f"RESULT TYPE3:    {rpn.infix_formula()}")
                exit(0)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        tl = sys.argv[1:]
    else:
        tl = input("> ")
        tl = tl.split(" ")
        tl = [s for s in tl if s != ""]

    in_list = list(map(Fraction, tl))
    target = in_list.pop(-1)
    print(f"Q. {tl[:-1]} = {target}")
    solve2nd(target, in_list)
    print("Case Failed")