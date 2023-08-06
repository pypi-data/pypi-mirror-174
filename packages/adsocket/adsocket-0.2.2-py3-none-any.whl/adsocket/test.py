import weakref


class A:

    _name = None

    def __init__(self, name):
        self._name = name
        self._running = False

    def run(self):
        self._running = True

    def close(self):
        del self

    def __del__(self):
        print(f"{self._name} deleted")

    def __str__(self):
        return self._name


if __name__ == '__main__':
    l = weakref.WeakSet()
    tmp_list = []
    for x in range(30):
        i = A(f'test-{x}')
        i.run()
        l.add(i)
        tmp_list.append(i)

    print()
    print([x for x in l])
    print(len(l))
    #
    # for y in l:
    #     y.close()
    #
    # print([x for x in l])
    # print(len(l))
