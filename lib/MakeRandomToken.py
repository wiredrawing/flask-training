import string
import random


class MakeRandomToken:
    def __init__(self):
        """ランダムなトークンを生成する
        """
        self.sign = True
        self.number = True

    def include_number(self, include_number: bool) -> bool:
        """数字を含めるかどうか

        :param include_number: 数字を含めるかどうか
        :return: self.number
        """
        if include_number is True:
            self.number = True
        else:
            self.number = False
        return self.number

    def include_sign(self, include_sign: bool) -> bool:
        """記号を含めるかどうか

        :param include_sign: 記号を含めるかどうか
        :return: self
        """
        if include_sign is True:
            self.sign = True
        else:
            self.sign = False

        return self.sign

    def token(self, size: int) -> str:
        # 半角英数字をシーケンスにする
        alpha_numbers = string.ascii_letters
        if self.number is True:
            alpha_numbers += string.digits
        letters = []
        for i in alpha_numbers:
            letters.append(i)

        if self.sign is True:
            letters += ["-", "_", ".", "@", "="]
        print(letters)
        # シャッフルする
        token = []
        for i in range(size):
            token.append(letters[random.randrange(len(letters))])

        # シャッフルしたものを結合して返す
        return "".join(token)
