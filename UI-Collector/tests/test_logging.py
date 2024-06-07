import logging


def foo(a, b):
    c = a + b
    raise ValueError('test')
    return c


def bar(a):
    print('a + 100:', foo(a, 100))


def main():
    try:
        bar(100)
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()