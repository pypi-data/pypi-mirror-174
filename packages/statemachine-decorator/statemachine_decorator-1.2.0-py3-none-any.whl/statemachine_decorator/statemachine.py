import copy

class StateNode(str):
    # 无权有向状态图中的一个节点，用户可切换的下一个状态为当前状态节点的 nextStates 集合中的值
    # 一个状态节点由一个字符串 name 标识
    __slots__ = ['__nextStates']

    @property
    def nextStates(self):
        # 只读的可切换状态表
        return self.__nextStates

    def __new__(cls, value):
        return str.__new__(cls, value)

    def __init__(self, value):
        self.__nextStates = set()

    def addNext(self, nextState):
        # 添加下一个节点
        assert isinstance(nextState, StateNode), TypeError("Isn't add a state node!")
        self.__nextStates.add(nextState)

    def switchable(self, stateName: str) -> bool:
        # 下一个节点是否可切换
        return any(s == stateName for s in self.__nextStates)

    def __getitem__(self, item: str | int):
        if isinstance(item, str):
            assert isinstance(item, str), "Next state getter must receive a string!"
            for s in self.__nextStates:
                if s == item:
                    return s
            return None
        else:
            return super(StateNode, self).__getitem__(item)


    def __delitem__(self, key: str | int):
        """
        To delete an state form nextStates.
        :param key: the state's value
        :return:
        """
        if isinstance(key, str):
            if key in self.__nextStates:
                self.__nextStates.remove(key)
        else:
            return super(StateNode, self).__delitem__(key)

    def __bool__(self):
        return True
"""
状态网解决方案
优点：能精准控制状态的切换能力
"""
class StateNet:
    # 无权有向图，代表所有允许的状态
    __slots__ = ['__states']
    def __init__(self, net={}):
        # an empty net
        assert isinstance(net, dict), 'net must be a dict with str keys and set values'
        assert all(all(s in net for s in net[sn]) for sn in net), 'All states should be exist in your net! Check out your argument carefully.'
        self.__states = set()
        for sn in net:
            node = StateNode(sn)
            self.__states.add(node)
        for sn in self.__states:
            for s in net[sn]:
                for ns in self.__states:
                    if ns == s:
                        ns.addNext(sn)
                        break

    def add(self, entry: set[str], name: str):
        """
        :param entry: a set that contains all entry states' name
        :param name:  the new state's name
        """
        assert all(any(sn == s for s in self.__states) for sn in entry), "Some entry are not exists"
        if not name in self.__states:
            state = StateNode(name)
        else:
            state = self[name]
        if entry:
            for s in self.__states:
                del s[state]
                if s in entry:
                    s.addNext(state)    # add new entries
        self.__states.add(state)

    def __getitem__(self, item: str):
        assert isinstance(item, str), "State key is not string"
        for s in self.__states:
            if s == item:
                return s
        return None # no such state

    def __delitem__(self, key: str):
        assert isinstance(key, str), "must delete a string key."
        for s in self.__states:
            del s[key]
        self.__states.remove(key)

    def __iter__(self):
        return iter(self.__states)

    def __str__(self):
        return str(self.__states)

    def update(self, other: dict[str: set]):
        for s in other:
            if not s in self.__states:
                self.__states.add(StateNode(s))
        for s, entries in other.items():
            self.add(entries, s)


def _illegal_(states):
    assert len(set(states)) == len(states), "Repeat state detected."
    for state in states:
        if state == 'switch':
            raise ValueError('"switch" is protected for function switch(self).')
        elif state == 'state':
            raise ValueError('"state" is protected for attribute state.')
        elif state == 'states':
            raise ValueError('"states" is protected for readonly attribute states.')
        if not isinstance(state, str):
            raise TypeError("Non string state detected!")
        if not state.isidentifier():
            raise ValueError("An identifier state value is expected.")
        if not state.isupper():
            Warning('Uppercase is suggested as state value.')
    return True
"""
类修饰器，
状态池从传入之时，便只能从switch函数切换
特点：提供可靠状态继承，没有元类不兼容问题，目前最推荐
注意：若继承自没有被本装饰器装饰的类，应确保它没有同时有states、switch、以及states中所有的属性
"""
def stateDefine(states: dict[str: set], default=None):
    """

    :param states: a dict that defines a net{
        state: {
            entries(所有能转换为该状态的状态，类型为字符串）
        }
    }
    :param default: default state
    子类可以更新父类某状态节点的入边
    """
    _illegal_(states)
    keywords = tuple(states) + ('switch', 'state', 'states')
    def dec(cls: type):
        for state, nextStates in states.items():
            assert isinstance(state, str) and (isinstance(nextStates, set) or nextStates is None), 'State must be string and nextStates must be set'
            setattr(cls, state, state)
        # 是否为继承来的
        if hasattr(cls, 'states') and isinstance(cls.states, StateNet):
            cls.states = copy.deepcopy(cls.states)
            # modify sub class's state net!
            cls.states.update(states)
            print(cls.states)

        else:
            cls.states = StateNet(states)
        new_setattr = None
        new_delattr = None
        new_init_ = None
        if '__setattr__' in cls.__dict__:
            origin_setattr = cls.__setattr__
            def _readonlify__setattr__(self, key, value):
                if key in keywords:
                    raise AttributeError('State\swtich\states is readonly!')
                else:
                    return origin_setattr(self, key, value)
            new_setattr = _readonlify__setattr__
        else:
            def _object__setattr(self, key, value):
                if key in keywords:
                    raise AttributeError('State\swtich\states is readonly!')
                else:
                    return object.__setattr__(self, key, value)
            new_setattr = _object__setattr
        if '__delattr__'  in cls.__dict__:
            origin_delattr = cls.__delattr__
            def __new_delattr__(self, key):
                if key in keywords:
                    raise AttributeError('State cannot be deleted!')
                origin_delattr(self, key)
            new_delattr = __new_delattr__
        else:
            def __object_delattr__(self, key):
                if key in keywords:
                    raise AttributeError('State cannot be deleted!')
                object.__delattr__(self, key)
            new_delattr = __object_delattr__

        if default:
            if '__init__' in cls.__dict__:
                origin_init = cls.__init__
                def __default_state_init__(self, *args, **kwargs):
                    origin_init(self, *args, **kwargs)
                    self.switch(default)
                new_init_ = __default_state_init__
            else:
                def __default_state_init__(self, *args, **kwargs):
                    self.switch(default)
                new_init_ = __default_state_init__

        def switch(self, name: str):
            """
            switch to a state!
            :param name:
            :return: nothing
            """
            assert isinstance(name, str)
            try:
                if self.__state.switchable(name):
                    self.__state = cls.states[name]
                else:
                    raise ValueError(f"No such state to switch! All allowed is {self.__state.nextStates}")
            except AttributeError:
                node = cls.states[name]
                if node:
                    self.__state = node
                else:
                    raise ValueError(f"No such state to entry! All allowed is {cls.states}")

        @property
        def state(self):
            try:
                return self.__state
            except AttributeError:
                raise AttributeError("No state on the object. Please switch a state first!")

        cls.state = state
        cls.__setattr__ = new_setattr
        cls.switch = switch
        if new_init_:
            cls.__init__ = new_init_
        cls.__delattr__ = new_delattr
        return cls
    return dec

__all__ = ['stateDefine', 'StateMachine',
           'StateNode', 'StateNet']
