from .post_machine import PostMachine


def main(argv=None) -> int:
    print("Введите начальное состояние ленты")
    initial = input().rstrip("\n")
    size = max(1, len(initial)) if initial is not None else 20
    pm = PostMachine(size)
    pm.set_tape(initial)
    print("Машина Поста готова")
    while True:
        print("Введите команду")
        cmd = input().rstrip("\n")
        if cmd.strip() == "":
            continue
        try:
            pm.execute(cmd)
        except SystemExit as e:
            raise
