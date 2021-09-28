import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *
# producer
revenda_listar = "/revenda/listar"
revenda_listar_response = "response to /revenda/listar"
# consumer
revenda = "/revenda"
revenda_response = "response to /revenda"


def add_transition(net, name_precious_place, name_new_place, name_transition, cons, prod):
    net.add_place(Place(name_new_place, []))

    transition = Transition(name_transition)
    net.add_transition(transition)

    net.add_input(name_precious_place, name_transition, cons)
    net.add_output(name_new_place, name_transition, prod)
    return transition

def factory (prod, init=[]) :
    n = PetriNet("N")

    # /revenda/listar
    t = Transition(revenda_listar)
    n.add_transition(t)
    n.add_place(Place(revenda_listar_response, []))
    n.add_output(revenda_listar_response, revenda_listar, prod)

    return n, t

def main():
    # given a revenda_listar_request and revenda_listar_response
    # revenda_listar_response = Value("0")
    # net, revenda_listar_trans = factory(revenda_listar_response, [])

    # MultiArc
    # revenda_listar_response = [Value("1"), Value("2"), Value("3")]
    # net, revenda_listar_trans = factory(MultiArc(revenda_listar_response), [])

    # Variable("x")
    revenda_listar_response = Variable("x")
    net, revenda_listar_trans = factory(revenda_listar_response, [])

    net.draw("value-0.png")
    #import ipdb; ipdb.set_trace()
    revenda_listar_trans.fire(Substitution(x="1"))
    net.draw("value-1.png")

    # trans.fire(modes[1])
    # print (modes)
    # net.draw("value-1.png")

    #import ipdb; ipdb.set_trace()
    # trans2 = add_transition(net, "tgt", "tgt2", revenda, Value("ID123"), Value(""))
    #
    # trans2.fire(modes[0])
    # print (modes)
    # net.draw("value-2.png")

if __name__ == "__main__":
    main()
