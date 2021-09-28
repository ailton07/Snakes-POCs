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

def factory (cons, prod, init=[]) :
    n = PetriNet("N")

    # /revenda/listar
    n.add_place(Place(revenda_listar_response, init))

    # /revenda
    n.add_place(Place(revenda_response, []))
    t = Transition(revenda)
    n.add_transition(t)
    n.add_input(revenda_listar_response, revenda, cons)
    n.add_output(revenda_response, revenda, prod)

    return n, t

def main():
    linked_variable="codigoRevenda"
    #net, revenda_listar_trans = factory(Variable("codigoRevenda"), Variable("codigoRevenda"))
    net, revenda_listar_trans = factory(Variable("codigoRevenda"), Value(""))
    net.draw("value-0.png")
    import ipdb; ipdb.set_trace()


    # given the request and response of "/revenda/listar"
    net.place(revenda_listar_response).add(["01", "02", "03"])
    net.draw("value-1.png")


    # given the request "/revenda"
    revenda_listar_trans.fire(Substitution(codigoRevenda="01"))
    net.draw("value-2.png")

    #
    try:
        revenda_listar_trans.fire(Substitution(codigoRevenda="999"))
    except:
        print("IDOR Attack Detected")
    net.draw("value-2.png")

if __name__ == "__main__":
    main()
