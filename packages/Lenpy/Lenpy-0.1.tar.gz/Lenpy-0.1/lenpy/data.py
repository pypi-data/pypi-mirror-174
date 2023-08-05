
# Un modulo para crear la Data de nuestro juego

import pickle, os

from lenpy import tools, system, config

# El Data Manager por ahora solo funciona en Windows, actualmente no cuento con Linux

class Manager:
    
    def __init__(self, folder_name, file_extension):
        
        self.file_extension = file_extension
        self.folder_name = folder_name
        self.folder = ""
        
        if system.windows:
            
            self.folder = os.environ["APPDATA"] + "/" + self.folder_name + "/"

            # Crea el directorio en donde se guardara la data
            tools.make_dir(os.environ["APPDATA"], self.folder_name)
        
    def Save(self, data, name):
        
        # Escribe de forma binario en el archivo de la data
        file = open(self.folder + "/" + name + self.file_extension, "wb")
        
        # Guarda la data en el archivo, según la variable indicada  
        pickle.dump(data, file)

    def Load(self, name):

        # Lee los datos binarios en el archivo
        file = open(self.folder + "/" + name + self.file_extension, "rb")

        data = pickle.load(file)

        # Retorna la data
        return data

    def Exists_data(self, name):

        # Existe la carpeta en donde se guardan los datos?
        return os.path.exists(self.folder + "/" + name + self.file_extension)

    def Load_game_data(self, files_to_load, default_data):

        variables = []

        # Hay más de un archivo de datos?
        for index, file in enumerate(files_to_load):
            
            if self.Exists_data(file):
                
                variables.append(self.Load(file))

            else:

                variables.append(default_data[index])

        if len(variables) > 1:

            return tuple(variables)

        else:

            return variables[0]

    def Save_game_data(self, files_to_save, file_names):

        # Hay más de un archivo que quieras guardar?
        for index, file in enumerate(files_to_save):

            self.Save(file, file_names[index])

    def delete(self, data, name):

        # Quieres borrar los datos de tu juego?

        if self.Exists_data(name):

            os.remove(self.folder + "/" + name + self.file_extension)

        else:

            print("The file " + str(name) + " does exist.")

        if data:

            data.clear()

    def delete_game_data(self, datas, file_names):

        # Hay más de un archivo que quieras borrar?
        for index, data in enumerate(datas):

            if self.Exists_data(file_names[index]):

                self.delete(data, file_names[index])

            else:

                if datas:

                    data.clear()

                print("The file " + str(file_names[index]) + f"{self.file_extension} does exist.")