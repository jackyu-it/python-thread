def match(pattern):
    print('Looking for ' + pattern)
    try:
        while True:
            s = (yield)
            print ("S is: {}".format(s))
            if pattern in s:
                print(s)
    except GeneratorExit:
        print("=== Done ===")


def read(text, next_coroutine):
    for line in text.split():
        next_coroutine.send(line)
    next_coroutine.close()


text = 'Commending spending is offending to people pending lending!'

matcher = match('ending')
matcher.__next__()

read(text, matcher)
