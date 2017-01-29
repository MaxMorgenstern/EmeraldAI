from cachetools import LRUCache
from cachetools import cached

@cached(cache={})
def fib(n, test):
    print "... fib()", n, test
    return n if n < 2 else fib(n - 1, test) + fib(n - 2, test)

for i in range(20):
    print('fib(%d) = %d' % (i, fib(i, (i*2))))

for i in range(20):
    print('fib(%d) = %d' % (i, fib(i, (i*2))))


exit(1)


def test(key):
    print "test", key
    return "Max"

cache = LRUCache(maxsize=2, missing=test)
cache.update([('first', 1), ('second', 2)])
print cache

cache['third'] = 3
print cache

cache['fourth'] = 4
print cache


print cache['fifth']
print cache

