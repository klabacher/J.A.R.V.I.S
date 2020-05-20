from Plugins import EH
def filter(data):
    EH.call("d", data)
    ds = data.split()
    print(data)