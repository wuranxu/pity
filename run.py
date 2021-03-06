from app import pity


@pity.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    pity.run("0.0.0.0", threaded=True, port="7777")
