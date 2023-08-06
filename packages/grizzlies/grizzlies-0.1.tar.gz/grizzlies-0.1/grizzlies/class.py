import json, csv
from flatten_json import flatten

class grizzlies:


    def __init__(self):

        self.fichero = None

    def leer_csv(self, doc, delimitador = ","):

            lista_dicc = []


            with open(doc, encoding='utf-8') as csv_leer:

                csv_leido = csv.DictReader(csv_leer, delimiter = delimitador)


                for instancia in csv_leido:

                    lista_dicc.append(instancia)

                csv_leer.close()


            self.fichero = lista_dicc

            return

    def leer_json(self, doc):

        with open(doc, "r") as json_leer:


            self.fichero = json.load(json_leer)

            json_leer.close()

        return



    def leer(self, doc):

        self.tipofich = doc[-1]

        if self.tipofich != "v" and self.tipofich != "n":

            raise ValueError("Tipo de fichero invalido")

        if self.tipofich == "v":

            return self.leer_csv(doc)

        return self.leer_json(doc)



    def convertir_a_json(self):


        self.fichero = json.dumps(self.fichero, indent=4)




    def convertir_a_csv(self, nido = True, separador = "_"):



        if nido == True:


            self.fichero =  [flatten(d, separator = separador) for d in self.fichero]

            return


        return




    def convertir(self):

        if self.tipofich == "v":

            return self.convertir_a_json()

        return self.convertir_a_csv()



    def guardar_json(self, nombre_json):

        with open(nombre_json, 'w', encoding='utf-8') as json_obj:

            json_obj.write(self.fichero)

            json_obj.close()


            return


    def guardar_csv(self, nombre_csv):

        with open(nombre_csv, 'w') as csv_obj:

            headers = self.fichero[0].keys()


            writer = csv.DictWriter(csv_obj, fieldnames = headers)

            writer.writeheader()

            for instancia in self.fichero:

                writer.writerow(instancia)


            csv_obj.close()

        return



    def guardar(self, nombre_archivo):

        if self.tipofich == "v":

            return self.guardar_json(nombre_archivo)

        return self.guardar_csv(nombre_archivo)






