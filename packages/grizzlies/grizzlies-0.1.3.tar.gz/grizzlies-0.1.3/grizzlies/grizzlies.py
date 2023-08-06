import json, csv
from flatten_json import flatten

class grizzlies:
    def __init__(self):
        """
            Atributos:
                fichero -- Atributo donde se guarda el fichero sobre el que trabaja. (default:None).
            
        """

        self.fichero = None

    def leer_csv(self, doc, delimitador = ","):
        """

        Función para leer archivos csv.

        Argumentos:
            doc {csv} -- archivo sobre el que se quiere trabajar trabajar.
            delimitador {string} -- delimitador del archivo csv. (default:";").
        
        Resultado:
            Se guarda directamente el resultado en el argumento fichero.

        """

        lista_dicc = []


        with open(doc, encoding='utf-8') as csv_leer:

            csv_leido = csv.DictReader(csv_leer, delimiter = delimitador)


            for instancia in csv_leido:

                lista_dicc.append(instancia)

            csv_leer.close()


        self.fichero = lista_dicc

        return
    

    def leer_json(self, doc):
        """

        Función para leer archivos json.

        Argumentos:
            doc {json} -- archivo sobre el que se quiere trabajar trabajar.
        
        Resultado:
            Se guarda directamente el resultado en el argumento fichero. 

        """

        with open(doc, "r") as json_leer:


            self.fichero = json.load(json_leer)

            json_leer.close()

        return

    def leer(self, doc):
        """

        Función para detectar automáticamente el tipo de archivo introducido, y que se ejecute la función correspondiente
        para su lectura.

        Argumentos:
            doc {csv} -- archivo sobre el que se quiere trabajar trabajar.

        Resultado:
            Se guarda directamente el resultado en el argumento fichero.
        
        """

        self.tipofich = doc[-1]

        if self.tipofich != "v" and self.tipofich != "n":

            raise ValueError("Tipo de fichero invalido")

        if self.tipofich == "v":

            return self.leer_csv(doc)

        return self.leer_json(doc)




    def convertir_a_json(self):
        """
        Función para convertir un archivo csv a un archivo json.

        Resultado:
            Se guarda directamente la conversión en el argumento fichero.

        """


        self.fichero = json.dumps(self.fichero, indent=4)




    def convertir_a_csv(self, nido = True, separador = "_"):

        """

        Función para convertir un archivo json a un archivo csv.

        Arguments:
            nido {boolean} -- (default:True)
            separador {string} -- Separador para tu archivo csv (default:"_")

        Resultado:
            Se guarda directamente la conversión en el argumento fichero.
        
        """
        if nido == True:


            self.fichero =  [flatten(d, separator = separador) for d in self.fichero]

            return


        return




    def convertir(self):
        """
        
        Función para detectar automáticamente el tipo de archivo que se encuentra en el argumento fichero, y que se ejecute la función correspondiente
        para su conversión.

        Resultado:
            Se guarda directamente la conversión en el argumento fichero.

        """


        if self.tipofich == "v":

            return self.convertir_a_json()

        return self.convertir_a_csv()



    def guardar_json(self, nombre_json):

        """
        
        Función para guardar el archivo que se encuentra en el argumento fichero como json en el directorio introducido.

        Argumentos:
            nombre_json {string} -- Ruta donde se quiere guardar el archivo y el nombre con el que se quiere guardar con la extensión json.

        Resultado:
            Se guarda el archivo en la ruta establecida y con el nombre deseado.

        """



        with open(nombre_json, 'w', encoding='utf-8') as json_obj:

            json_obj.write(self.fichero)

            json_obj.close()


            return


    def guardar_csv(self, nombre_csv):
        """
        Función para guardar el archivo que se encuentra en el argumento fichero como csv en el directorio introducido.

        Argumentos:
            nombre_csv {string} -- Ruta donde se quiere guardar el archivo y el nombre con el que se quiere guardar con la extensión csv.

        Resultado:
            Se guarda el archivo en la ruta establecida y con el nombre deseado.

        """

        with open(nombre_csv, 'w') as csv_obj:

            headers = self.fichero[0].keys()


            writer = csv.DictWriter(csv_obj, fieldnames = headers)

            writer.writeheader()

            for instancia in self.fichero:

                writer.writerow(instancia)


            csv_obj.close()

        return 



    def guardar(self, nombre_archivo):
        """

        Función para detectar automáticamente el tipo de archivo que se encuentra en el argumento fichero, y que se ejecute la función correspondiente
        para guardarlo.

        Argumentos:
            nombre_archivo {string} -- Ruta donde se quiere guardar el archivo y el nombre con el que se quiere guardar con la extensión correspondiente.

        Resultado:
             Se guarda el archivo en la ruta establecida y con el nombre deseado.

        """

        if self.tipofich == "v":

            return self.guardar_json(nombre_archivo)

        return self.guardar_csv(nombre_archivo)






