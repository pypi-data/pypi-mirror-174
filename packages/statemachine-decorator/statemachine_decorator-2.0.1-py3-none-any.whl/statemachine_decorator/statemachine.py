import copy
import types

from .exceptions import *

NS = None

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

    def __getitem__(self, item: str | int | None):
        if item is None:
            item = NS
        if isinstance(item, str):
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

class NoneState(StateNode):
    """
    The special state called none_state
    """
    _____ = False
    def __new__(cls, *args):
        if NoneState._____:
            return NS
        else:
            NoneState._____ = True
            return str.__new__(cls)

    def __hash__(self):
        return hash(str(self))

    def switchable(self, stateName: str) -> bool:
        return True

    def __init__(self):
        if not NoneState._____:
            self.__nextStates = set()

    def __str__(self):
        return '<____NoneState____>'
    def __repr__(self):
        return repr(str(self))
    def __init_subclass__(cls, **kwargs):
        raise TypeError("type 'NoneState' is not an acceptable base type")

    def __bool__(self):
        return False

    def __or__(self, other):
        if isinstance(other, types.UnionType):
            return other
        else:
            raise TypeError

    def __ror__(self, other):
        return self | other

    def __eq__(self, other):
        return other is NS


NS = NoneState()

"""
状态网解决方案
优点：能精准控制状态的切换能力
"""
class StateNet:
    # 无权有向图，代表所有允许的状态
    __slots__ = ['__states']
    def __init__(self, net={}):
        # an empty net
        self.__states = set()
        assert isinstance(net, dict), 'net must be a dict with str keys and set values'
        assert all(self.__states.add(StateNode(sn) if sn is not NS else NS) or all(s in net and isinstance(s, str) for s in (net[sn] if net[sn] else set())) for sn in net ), \
            'All states should be exist and must be instanceof str in your net! Check out your argument carefully.'
        for sn in self.__states:
            if not net[sn] is None:  # support None passed
                for s in net[sn]:
                    sn.addNext(self[s])

    def add(self, exits: set | None, name: str):
        """
        :param exits: a set that contains all exits states' name
        :param name:  the new state's name
        """
        assert all((any(self[sn]) and sn is not NS) for sn in (exits if (exits is not None) else set())), "Some exit are not exists or add a NS with any exit!"
        if not name in self.__states:
            state = StateNode(name)
        else:
            state = self[name]
        self.__states.add(state)
        for ns in (exits if exits is not None else set()):
            state.addNext(self[ns])

    def __getitem__(self, item: str):
        assert isinstance(item, str), "State key is not string or NS, None is not NS!"
        for s in self.__states:
            if s == item:
                return s
        return None # no such state

    def __delitem__(self, key: str):
        assert isinstance(key, str), "must delete a string key."
        self.__states.remove(key)

    def __iter__(self):
        return iter(self.__states)

    def __str__(self):
        return str(self.__states)

    def update(self, other: dict[str: set]):
        for s in other:
            self.__states.add(StateNode(s) if s is not NS else NS)
        for s, exits in other.items():
            self.add(exits, s)

    def copy(self):
        newnet = StateNet()
        for s in self:
            newnet.__states.add(s)
        for s in self.__states:
            if s is not NS:
                for ns in s.nextStates:
                    newnet[s].addNext(ns)
        return newnet

def _illegal_(states):
    assert len(set(states)) == len(states), "Repeat state detected."
    for state in states:
        if state == 'switch':
            raise ValueError('"switch" is protected for function switch(self).')
        elif state == 'state':
            raise ValueError('"state" is protected for attribute state.')
        elif state == 'states':
            raise ValueError('"states" is protected for readonly attribute states.')
        elif state is NS:
            raise ValueError('NS cannot appear in your state net directly!')
        if not isinstance(state, str):
            raise TypeError("Non string state detected!")
        if not state.isidentifier():
            raise ValueError("An identifier state value is expected.")
        if not state.isupper():
            Warning('Uppercase is suggested as state value.')


"""
类修饰器，
状态池从传入之时，便只能从switch函数切换
特点：提供可靠状态继承，没有元类不兼容问题，目前最推荐
注意：若继承自没有被本装饰器装饰的类，应确保它没有同时有states、switch、以及states中所有的属性
"""
def stateDefine(states: dict[str: set]={}, default_state:str|None=None, nonable:bool=False):
    """
    :param states: a dict that defines a net{
        state: {
            entries(所有能转换为该状态的状态，类型为字符串）
        }
    }
    :param default_state: default state
    :param nonable: If state can switch or have an empty state
    子类可以更新父类某状态节点的入边
    """
    _illegal_(states)
    if nonable:
        if default_state is None:
            default_state = NS
            states[NS] = None
    elif default_state is NS:
        raise ValueError("Cannot set default state to NS when given nonable False")
    def dec(cls: type):
        nonlocal states
        for state, exitStates in states.items():
            assert isinstance(state, str) and (isinstance(exitStates, set) or exitStates is None), \
                'State must be string or None and nextStates must be <class set>'
            setattr(cls, state, state)
        # 是否为继承来的
        if hasattr(cls, '_states_inherit') and isinstance(cls._states_inherit, StateNet):
            # modify sub class's state net
            if not nonable and NS in cls._states_inherit:    # remove NS
                state_net = cls._states_inherit.copy()
                del state_net[NS]
            else:           # just copy!
                if len(states):
                    state_net = cls._states_inherit.copy()
                    state_net.update(states)
                else:
                    state_net = cls._states_inherit
        else: state_net = StateNet(states)
        @property
        def _getstates(self):
            nonlocal state_net
            return state_net
        cls.state = __getstate
        cls.states = _getstates
        cls.switch = __switch
        if '__init__' in cls.__dict__:
            origin_init = cls.__init__
            if nonable:
                def __default_init__(self, *args, **kwargs):
                    nonlocal dec, default_state, nonable
                    if dec.__sub:
                        origin_init(self, *args, **kwargs)
                    else:
                        if default_state is not NS:
                            self.switch(default_state)
                        else:
                            self.__state = default_state
                        origin_init(self, *args, **kwargs)

                cls.__init__ = __default_init__
            elif default_state is not None:
                def __default_init__(self, *args, **kwargs):
                    nonlocal dec, default_state, nonable
                    if dec.__sub:
                        origin_init(self, *args, **kwargs)
                    else:
                        self.switch(default_state)
                        origin_init(self, *args, **kwargs)

                cls.__init__ = __default_init__
        elif nonable or default_state is not None:
            def __default_init__(self, *args, **kwargs):
                nonlocal default_state
                self.switch(default_state)
            cls.__init__ = __default_init__
        if '__setattr__' in cls.__dict__:
            _origin_setattr = cls.__setattr__

            def __readonlify__setattr__(self, key, value):
                if key in self.states:
                    raise ReadonlyStatesException(type(self), key)
                else:
                    _origin_setattr(self, key, value)

            cls.__setattr__ = __readonlify__setattr__
        else:
            cls.__setattr__ = __object_setattr__
        if '__delattr__' in cls.__dict__:
            _origin_delattr = cls.__delattr__

            def __readonly_delattr__(self, key):
                if key in self.states:
                    raise ReadonlyStatesException(type(self), key)
                _origin_delattr(self, key)

            cls.__delattr__ = __readonly_delattr__
        else:
            cls.__delattr__ = __object_delattr__
        if '__init_subclass__' in cls.__dict__ and hasattr(cls.__init_subclass__, '__func__'):
            origin_init_subclass = cls.__init_subclass__
            @classmethod
            def __sub_init_subclass__(subcls, *args, **kwargs):
                origin_init_subclass.__func__(subcls, *args, **kwargs)
                nonlocal dec
                dec.__sub = True
                subcls._states_inherit = state_net
            cls.__init_subclass__ = __sub_init_subclass__
        else:
            @classmethod
            def __sub_init_subclass__(subcls, *args, **kwargs):
                nonlocal dec
                dec.__sub = True
                subcls._states_inherit = state_net
            cls.__init_subclass__ = __sub_init_subclass__
        return cls
    dec.__sub = False
    return dec
state_define = stateDefine  # other naming styles
StateDefine = stateDefine

def __object_setattr__(self, key, value):
    if key in self.states:
        raise ReadonlyStatesException(type(self), key)
    else:
        return object.__setattr__(self, key, value)

def __object_delattr__(self, key):
    if key in self.states:
        raise ReadonlyStatesException(type(self), key)
    object.__delattr__(self, key)

def __switch(self, name: str):
    """
    switch to a state!
    :param name:
    """
    try:
        if name is not NS:
            assert isinstance(name, str), \
                "Try to switch to a non string!"
            if self.state.switchable(name):
                self.__state = self.states[name]
            else:
                raise UnswitchableStateException(type(self), name, self.state, self.state.nextStates)
        else:
            raise UnswitchableStateException(type(self), name, self.state, set(state for state in self.states if state is not NS))
    except NoStateException:
        if name in self.states:
            self.__state = self.states[name]
        else:
            raise UnswitchableStateException(type(self), name, None, set(state for state in self.states if state is not NS))
# TODO: in the next version 2.1.0, change the state property to a nonlocal variable in the decorator, avoid user write the __state attribute, and pull down namespace pollution
@property
def __getstate(self):
    try:
        return self.__state
    except AttributeError:
        raise NoStateException(self)

__all__ = ['stateDefine', 'StateMachine',
           'StateNode', 'StateNet', "NS", 'state_define', 'StateDefine']
