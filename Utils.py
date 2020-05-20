import Plugins, importlib, pkgutil, sys
class PluginLoader():
    def __init__(self, strictLoad=None, excludeLoad=None):
        for handlerModule in self.getPackageModules(Plugins):
            if not (strictLoad and handlerModule not in strictLoad or excludeLoad and handlerModule in excludeLoad):
                if handlerModule not in sys.modules.keys():
                    importlib.import_module(handlerModule)
        print("Handler modules loaded")
    
    def getPackageModules(self, package):
        packageModules = []
        for importer, moduleName, isPackage in pkgutil.iter_modules(package.__path__):
            fullModuleName = "{0}.{1}".format(package.__name__, moduleName)
            if isPackage:
                subpackageObject = importlib.import_module(fullModuleName, package=package.__path__)
                subpackageObjectDirectory = dir(subpackageObject)
                if "Plugin" in subpackageObjectDirectory:
                    packageModules.append((subpackageObject, moduleName))
                    continue
                subPackageModules = self.getPackageModules(subpackageObject)
                packageModules = packageModules + subPackageModules
            else:
                packageModules.append(fullModuleName)
        return packageModules

class EventHandler():
    def __init__(self):
        self.handlers = {}
    
    def printt(self):
        print(self.handlers)

    def call(self, client, type, arg):
        print(f"Called {type} with {arg}")
        if type in self.handlers:
            for h in self.handlers[type]:
                h(client, arg)

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