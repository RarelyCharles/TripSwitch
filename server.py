__all__ = ["start_server"]

import bottle
from bottle import Bottle, post, get, response
app = bottle.app()
mock = False

if mock:
    def move_switch_row(count, direction):
        print("Moving switcher " + str(count) + " rows " + direction)
        return

    def flip_switch(side, state):
        print("Flipping " + side + " switch " + state)
        return
else:
    from stepper import move_switch_row
    from servos import flip_switch

currentYLoc = 0
# Switch y axis, move row down is a positive increase
switches = {"Kitchen":{"side":"left", "y":0},
            "Laundry":{"side":"right", "y":0},
            "Master Bedroom":{"side":"left", "y":2},
            "Second Bedroom":{"side":"right", "y":2},
            "Living room":{"side":"left", "y":4},
            "Bathroom 1":{"side":"right", "y":4},
            "Bathroom 2":{"side":"right", "y":5}}


def move_switcher(direction):
    global currentYLoc
    if direction == "up":
        move_switch_row(1, "up")
        currentYLoc = currentYLoc - 1
    elif direction == "down":
        move_switch_row(1, "down")
        currentYLoc = currentYLoc + 1


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        print("Handling cors")
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        #response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        #response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, ' \
        #                                                   'X-CSRF-Token, Authorization, ' \
        #                                                   'Access-Control-Allow-Headers, ' \
        #                                                   'Access-Control-Request-Method, ' \
        #                                                   'Access-Control-Request-Headers,' \
        #                                                   'Access-Control-Allow-Origin'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@post('/move/<direction>')
def creation_handler(direction):
    """Moves the switcher in the desired direction up|down"""
    move_switcher(direction)


@post('/switch/left/<state>')
def creation_handler(state):
    """Flips the left side switch to the desired state of on|off"""
    flip_switch("left", state)


@post('/switch/right/<state>')
def creation_handler(state):
    """Flips the right side switch to the desired state of on|off"""
    flip_switch("right", state)


@app.route('/switch/<switch_name>/<state>', method=['OPTIONS', 'POST'])
@enable_cors
def creation_handler(switch_name, state):
    """Flips the desired switch to the desired state of on|off"""
    print("Handling setting " + switch_name + " " + state)
    global currentYLoc
    global switches
    desiredSwitchState = switches[switch_name]["side"]
    desiredLocation = switches[switch_name]["y"]

    while currentYLoc != desiredLocation:
        if currentYLoc > desiredLocation:
            move_switcher("up")
        else:
            move_switcher("down")

    flip_switch(desiredSwitchState, state)


@app.route('/switch/list', method=['OPTIONS', 'GET'])
@enable_cors
def creation_handler():
    """Get the list of switches and their locations"""
    response.headers['Content-type'] = 'application/json'
    return switches


def start_server():
    app.run(host='0.0.0.0', port=8120)
