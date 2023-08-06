from statemachine_decorator import stateDefine

@stateDefine({
    's1': {"s2"},
    "s2": set()
}, 's1')
class span:
    pass

@stateDefine({
    's3': {'s1'}
})
class subspan(span):
    pass

@stateDefine({
    's1': {'s3', 's4'},
    's4': {"s2"}
}, 's4')
class subsubspan(subspan):
    pass

if __name__ == '__main__':
    s = span()
    print(s.state)
    s = subspan()
    print(s.state)
    s.switch('s3')
    print(s.state)
    s = subsubspan()
    print(s.state)
    s.switch('s1')
    print(s.state)
