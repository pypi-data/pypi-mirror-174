from statemachine_decorator import stateDefine
if __name__ == '__main__':
    # States data structure is a net, main class is StateNet, it countains node class called StateNode.
    # Every state is a string, the state node is s subclass of str
    # A stateful class could be created like this:
    @stateDefine({
        "state1": set(),  # refers to no entry, means no state can switch "state1",
        "state2": {"state1", "state3"},
        # refers to two entry, that means the object can switch to "state2" when its state is "state1" or "state3"
        "state3": {"state2", "state3"},  # refers to two entry, one is the state itself
        # it will raises an error if any string in args[0].values() (refers to above three python sets) is not exsits in the args[0].keys()(refers to the three string)
        # it will alse raise an error if you pass a non-str state key to the dict
    })
    class StatefulItem:
        # any class be decorated will be added attributes and a method below:
        # method:
        #   switch(self, new_state: str):
        #       # switch to a new state
        #       # if the new state is not switchable (i.e. "state2" switch to "state1" or "state2" switch to "any other state that not exists"), it will raise an error
        # attributes:
        #   state:
        #       # readonly property
        #       # type: str
        #       # probably value are states you passed in stateDefine function above: "state1" | "state2" | "state3"
        #       # can noly be changed by switch method.
        def __init__(self, state: str):
            self.switch(state)
    class subItem(StatefulItem):
        # inherit father's states
        def __init__(self):
            self.switch("state3")
    @stateDefine({
        'state1': {'state2'},    # modify father's states. It cause to father's 'state1' has the new one entry, and if father's 'state1' has old entrys, they will be cut totally.
        "state2": {"state1"},    # this modify will cut old entries: "state1" -> "state2", "state3" -> "state2", and build new : "state4" -> "state2"
        "state4": {"state1", "state3"}  # add new state! And relate it to old states.
        # attention: sub class can only add new state and modify old state's entries, if you want to delete old state, please change a mind(reconstruct your class relationships)
    })
    class subItem2(StatefulItem):
        pass
    item = StatefulItem("state1")
    print(item.state)  # "state1"
    item.switch("state2")
    print(item.state)  # "state2"
    # item.switch('state1') # will raise an error because "state1" has no entry, don't even say "state2"
    try:
        item.switch("state1")
        print("never")
    except ValueError:
        print("cannot switch to state1!")
    print(item.state1, item.state2, item.state3)
    subitem = subItem()
    print(subitem.state)
    subitem.switch('state2')
    print(subitem.state)
    for s in subitem.states:
        print(s, s.nextStates)
    subitem = subItem2('state2')
    print(subitem.state)
    subitem.switch('state1')
    print(subitem.state)
    subitem.switch('state4')
    print(subitem.state)
    for s in subitem.states:
        print(s, s.nextStates)