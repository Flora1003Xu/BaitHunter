from constant.DefException import RestartException


def test():
    raise RestartException("重启")

if __name__ == "__main__":
    try:
        test()
    except RestartException as e:
        print(e)
    except Exception as e:
        print(e)
