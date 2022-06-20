import argparse

def initialize_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("client_port",
                        help="The port of your device",
                        type=int)

    parser.add_argument("broker_ip",
                        help="The IP address of the broker",
                        type=str)

    parser.add_argument("broker_port",
                        help="The port of the broker",
                        type=int)

    return parser.parse_args()
