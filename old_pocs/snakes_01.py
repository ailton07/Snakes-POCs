import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *
revenda_listar = "/revenda/listar"
revenda = "/revenda"

# Instruções no livro Web Scraping com Pyhton
# source venv/bin/activate


def add_transition(net, name_precious_place, name_new_place, name_transition, cons, prod):
    net.add_place(Place(name_new_place, []))

    transition = Transition(name_transition)
    net.add_transition(transition)

    net.add_input(name_precious_place, name_transition, cons)
    net.add_output(name_new_place, name_transition, prod)
    return transition

def factory (cons, prod, init=["request"]) :
    n = PetriNet("N")
    n.add_place(Place("src", init))
    n.add_place(Place("tgt", []))
    # /revenda/listar
    t = Transition(revenda_listar)
    n.add_transition(t)
    n.add_input("src", revenda_listar, cons)
    n.add_output("tgt", revenda_listar, prod)

    return n, t, t.modes()

def main():
    # net, trans, modes = factory(Value(1), Value(0))
    # print (modes)
    # net.draw("value-0.png")
    #
    # trans.fire(modes[0])
    # print (modes)
    # net.draw("value-1.png")
    ########################################################

    #net, trans, modes = factory(Variable("x"), Variable("x"))
    net, trans, modes = factory(Value("request"), Value("ID123"))

    print (modes)
    net.draw("value-0.png")

    trans.fire(modes[0])
    print (modes)
    net.draw("value-1.png")

    # trans.fire(modes[1])
    # print (modes)
    # net.draw("value-1.png")

    import ipdb; ipdb.set_trace()
    trans2 = add_transition(net, "tgt", "tgt2", revenda, Value("ID123"), Value(""))

    trans2.fire(modes[0])
    print (modes)
    net.draw("value-2.png")

if __name__ == "__main__":
    main()
