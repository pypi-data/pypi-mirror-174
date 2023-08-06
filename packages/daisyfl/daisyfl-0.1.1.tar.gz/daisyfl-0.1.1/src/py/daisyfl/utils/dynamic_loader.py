class DynamicLoader:
    def __init__(self, module_name, class_name):
        module = __import__(module_name, fromlist=["import from sub-module"])
        self.plugin = getattr(module, class_name)
