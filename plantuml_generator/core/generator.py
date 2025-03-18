from plantuml import PlantUML


class PlantUMLGenerator:
    def __init__(self):
        self.__plantuml = PlantUML("http://www.plantuml.com/plantuml/img/")

    def generate_from_code(self, code: str):
        return self.__plantuml.processes(code)
