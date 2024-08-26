import json


class ManageJson:
    def __init__(self, path: str):
        """
        Inicializa la clase ManageJson.

        Parámetros:
        - path (str): Ruta del archivo JSON.
        """
        self.path = path

    def read_json(self) -> dict:
        """
        Lee un archivo JSON.

        Returns:
            dict: Diccionario con los datos del archivo JSON.
        """
        with open(self.path, "r") as file:
            data = json.load(file)
        return data

    def write_json(self, data: dict) -> None:
        """
        Escribe un archivo JSON.

        Parámetros:
        - data (dict): Diccionario con los datos a escribir en el archivo JSON.
        """
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

    def update_json(self, data: dict) -> None:
        """
        Actualiza un archivo JSON.

        Parámetros:
        - data (dict): Diccionario con los datos a actualizar en el archivo JSON.
        """
        with open(self.path, "r") as file:
            json_data = json.load(file)
        json_data.update(data)
        with open(self.path, "w") as file:
            json.dump(json_data, file, indent=4)
