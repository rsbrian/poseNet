class SocketHandler(object):
    def __init__(self):
        self.my_server = Server()

    def choose_course(self):
        return self.my_server.get_route(self.brain, self.view)
