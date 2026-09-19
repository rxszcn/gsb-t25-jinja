# 复现：同一条取值表达式，普通环境按未定义处理，沙箱环境把异常抛出来
from jinja2 import Environment
from jinja2.sandbox import SandboxedEnvironment


class D(dict):
    def __missing__(self, key):
        raise AttributeError("no attr here")


src = "{{ d[k] }}"
data = dict(d=D(), k="x")
for name, env in (("普通环境", Environment()), ("沙箱环境", SandboxedEnvironment())):
    try:
        print(name, "=", repr(env.from_string(src).render(data)))
    except Exception as e:
        print(name, "-> 抛", type(e).__name__, str(e)[:50])

src2 = "{{ d.attr }}"
for name, env in (("普通环境点号", Environment()), ("沙箱环境点号", SandboxedEnvironment())):
    try:
        print(name, "=", repr(env.from_string(src2).render(d=D())))
    except Exception as e:
        print(name, "-> 抛", type(e).__name__, str(e)[:50])
