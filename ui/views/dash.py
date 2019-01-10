import flask

dash = flask.Blueprint('dash', __name__)

@dash.route('/')
def route_index():
    return 'Dashboard Index Placeholder'
