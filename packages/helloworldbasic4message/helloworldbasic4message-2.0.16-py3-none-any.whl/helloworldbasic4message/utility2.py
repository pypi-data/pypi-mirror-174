

class SomeClass(list):
    def __init__(self, val):
        self.value=val

    pass

def somefunction(someclassvar):
    if type(someclassvar)==SomeClass:
        print("yes class match value=", someclassvar.value)
        pass
    else:
        print(" no match")
        pass
    return 1




def utilB_saygoodbye(name):
    return "util B says version Nov 2, 2022 13:44 : goodbye "+name;





