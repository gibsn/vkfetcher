class User():
    uid: int

    def __init__(self, uid: int):
        self.uid = uid

    def __str__(self) -> str:
        return "{}".format(self.uid)
