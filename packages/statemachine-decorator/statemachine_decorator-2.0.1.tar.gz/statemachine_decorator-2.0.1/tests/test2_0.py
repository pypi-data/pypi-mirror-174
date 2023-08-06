"""
test task:
    1. The nonable usage
    2. The unnonable usage
    3. The exceptions
    4. When inheriting without rewrite
    5. When inheriting with rewite
    6. The alias of the decorator
    7. setattr、delattr 是否能工作
    8. 以前版本基本功能
"""

from statemachine_decorator import *
from statemachine_decorator.exceptions import *
from statemachine_decorator.statemachine import NS
if __name__ == '__main__':
    @StateDefine()
    class base:
        pass
    print('不传参数的用法 -- 通过')
    try:
        @stateDefine({
            "walk": {None},
            None: None
        })
        class error_people:
            pass
        print('传入None但不设置相应参数的用法 -- 错误，可能因为参数判断分支错误')
    except TypeError:
        print('传入None但不设置相应参数的用法 -- 通过')
    @stateDefine({
        "stand": {"walk"},
        "walk": {"stand", "run"},
        "run": {"walk"}
    })
    class person_walking(base):
        pass
    print('传入作为入口集合的用法 -- 通过')
    p1 = person_walking()
    try:
        print(p1.state)
    except NoStateException:
        print('NoStateException -- 通过')
    p1.switch('stand')
    print('无默认状态切换状态 -- 通过', p1.state)
    @stateDefine({
        "stand": {"walk"},
        "walk": {"stand", "run"},
        "run": {"walk"}
    }, nonable=True)
    class person_non_walking(base):
        pass
    p1 = person_non_walking()
    print('Nonable 状态机初始化 -- 通过')
    print(p1.state)
    print("打印默认初始状态 -- 通过")
    try:
        p1.switch(NS)
        print('空状态转换不可转换性 -- 错误')
    except UnswitchableStateException as e:
        print('空状态转换不可转换性 -- 通过')
        print('抛出错误：', e)
    p1.switch('stand')
    print(f'空状态转换为其他状态 {p1.state} -- 通过')
    p1.switch('walk')
    print(f'其他状态正常转换为 {p1.state} -- 通过')
    try:
        p1.switch('jj')
    except UnswitchableStateException as e:
        print(f'转换为不存在的状态 -- 通过')
        print('抛出错误', e)
    try:
        p1.switch('stand')
    except UnswitchableStateException as e:
        print(f'转换为不可转换的状态 -- 通过')
        print('抛出错误', e)
    @stateDefine({
        "stand": {"walk"},
        "walk": {"stand", "run"},
        "run": {"walk"}
    }, default_state="walk", nonable=True)
    class person_non_def_walking(base):
        pass
    p1 = person_non_def_walking()
    print(f'取nonable 但是又同时指定了默认状态 {p1.state} -- 通过')
    try:
        p1.switch(NS)
    except UnswitchableStateException as e:
        print(f'有默认状态的 nonable 不可切换到 nonable -- 通过')
        print('抛出错误', e)
    @stateDefine({
        "stand": {"walk"},
        "walk": {"stand", "run"},
        "run": {"walk"}
    }, default_state="walk", nonable=True)
    class person_non_def_inh_walking(person_non_walking):
        pass
    p1 = person_non_def_inh_walking()
    if p1.state == 'walk':
        print(f'继承中 新添加default {p1.state} -- 通过')
    else:
        print(f'继承中 新添加default {p1.state} -- 错误')
    print(p1.states)
    @stateDefine({}, default_state="stand", nonable=True)
    class person_non_def_inh_rew_walking(person_non_def_inh_walking):
        pass
    p1 = person_non_def_inh_rew_walking()
    if p1.state == 'stand':
        print(f'继承中覆盖重写 default {p1.state} -- 通过')
    else:
        print(f'继承中覆盖重写 default {p1.state} -- 错误')
    try:
        del p1.stand
        del p1.switch
        print(f'删除关键属性 -- 错误')
    except ReadonlyStatesException as e:
        print(f'删除关键属性 -- 通过')
    try:
        p1.switch('run')
        print(f'转换到不存在的状态出错 -- 错误')
    except UnswitchableStateException as e:
        print(f'转换到不存在的状态出错 -- 成功')
    @stateDefine({
        'stand': {"run"}
    }, nonable=True)
    class peoplerunning(person_non_def_inh_rew_walking):
        pass
    p = peoplerunning()
    print(f'Nonable 重写父类默认状态 -- {"通过" if p.state == NS else "失败"}')
    p.switch('stand')
    p.switch('run')
    print(f'覆盖父类状态网 -- 成功')
    @stateDefine({
        "sit": {"stand"},
        "stand": {"sit"}
    }, default_state="sit", nonable=False)
    class person_can_sit:
        pass
    p = person_can_sit()
    p.switch('stand')
    print(f'创建父类中没有的新状态并与原状态网互操作-- 成功')
    @stateDefine({})
    class person_wring_run(peoplerunning):
        pass
    try:
        p = person_wring_run()
        print('覆盖父类默认 default，并切换 nonable 能力 -- 错误')
    except UnswitchableStateException as e:
        print('覆盖父类默认 default，并切换 nonable 能力 -- 通过')
    try:
        print(f'覆盖父类nonable能力 {p.state} -- 错误')
    except UnswitchableStateException as e:
        print('覆盖父类nonable能力 -- 通过')
        print('抛出错误', e)