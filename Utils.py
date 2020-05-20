import importlib, pkgutil, sys

class EventHandler():
    def __init__(self):
        print("EventHandler")
        self.handlers = {}
    
    def printt(self):
        print(self.handlers)

    def call(self, type, arg):
        print(f"Called {type} with {arg}")
        if type in self.handlers:
            for h in self.handlers[type]:
                h(arg)

    def delete(self, type):
        print(f"Try to delete {type}")
        if type in self.handlers:
            try:
                del self.handlers[type]
            except Exception:
                print(f"Cant delete {type} because {Exception}")

    def register(self, type):
        def registerhandler(handler):
            if type in self.handlers:
                self.handlers[type].append(handler)
                print("Append for EH: " + str(type))
            else:
                self.handlers[type] = [handler]
                print("Registered for EH: " + str(type))
            return handler
        return registerhandler