import json
from ColouredToken import ColouredToken, RequestResponseToken
from OpenAPI2PetriNet import OpenAPI2PetriNet
from utils.log_utils import LogUtils
import snakes.plugins

snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

LOGS_PATH = 'logs/combined_bola_example.json'

OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example.yaml'
#OPENAPI_PATH = 'examples/Structural_Problem_Based_on_BOLA_Example_02.yaml'

# Código utilizado na dissertação como exemplo
# loading log
logs_file = open(LOGS_PATH)
logs_json = json.load(logs_file)
logs_file.close()


def main():
    open_api_to_petri_parser = OpenAPI2PetriNet(OPENAPI_PATH)
    petri_net = open_api_to_petri_parser.create_petri_net('Juice Shop')
    transitions = petri_net.transition()
    petri_net.draw("value-0.png")



if __name__ == "__main__":
    main()
