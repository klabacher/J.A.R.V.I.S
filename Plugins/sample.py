from boot import EH
print("SAMPLE")

@EH.register("sample")
def sample(jarvis):
    print("SAMPLE DEF")

    