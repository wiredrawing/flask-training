from abc import ABC, abstractmethod


# インターフェースを定義する
class MessageFormatterInterface(ABC):
    """モデルを規程のdictフォーマットに修正する"""

    @abstractmethod
    def to_dict(self):
        pass
