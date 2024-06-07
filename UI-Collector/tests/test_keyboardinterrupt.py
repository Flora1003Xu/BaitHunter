import sys
import time


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print('\nKeyboardInterrupt ...')
            print('do something after Interrupt ...')
            print(f"global cnt {cnt}")
    sys.excepthook = new_hook


def main():
    ll = []
    for i in range(0, 10000000):
        ll.append(i)
    print('before ...')
    global cnt
    for i in range(len(ll) + 1):
        cnt = i
        print(i)
    print('after ...')


if __name__ == '__main__':
    cnt = 0
    suppress_keyboard_interrupt_message()
    try:
        main()
        print('the end')
    except Exception as e:
        print(e)