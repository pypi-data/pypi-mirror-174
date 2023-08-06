import MySQLdb 
import decimal

class Database:

    """
    Plantilla de conexión para las bases de datos
    """

    _HOST     = ""
    _USER     = ""
    _PASSWORD = ""
    _DATABASE = ""
    _PORT     = 3306
    

    def _connect (self):
        if self._HOST == "":
            raise Exception ('No se ha especificado un Host para la conexion base de datos')
        elif self._USER == "":
            raise Exception ('No se ha especificado un Usuario para la conexion con la base de datos')
        elif self._DATABASE == "":
            raise Exception ("No se ha especificado una Base de datos para establecer la conexión")
        else:
            self._database = MySQLdb.connect(host = self._HOST, user = self._USER, passwd = self._PASSWORD, db = self._DATABASE, port = self._PORT)
            self._cursor = self._database.cursor()


    def _disconnect (self):
        self._database.close()


    def retrieve_data (self, query:str = ""):
        """
        Mediante este metodo se puede generar una consulta sql del que se espere un retorno de datos.
        """

        self._connect()
        self._cursor.execute(query)

        column_names = [name[0] for name in self._cursor.description]
        rows = self._cursor.fetchall()
        
        #Tranformar las listas a un diccionario
        dict_list = []
        for row in rows:
            row = list(row)
            
            #Todos los datos de una columna que sean nulos entregarlos como texto vacío

            row[:] = [content if content != None else "" for content in row]

             #Todos los datos que sean de tipo 'decimal' (float con alta precisión) se convierten a 'float' [evita problemas al ser entregados como JSON]

            row[:] = [float(content) if type(content) is decimal.Decimal else content  for content in row]
            dict_list.append(dict(zip(column_names, row)))
    
        self._disconnect()
        
        
        return dict_list


    def execute (self, query:str = ""):
        """
        Mediante este método se puede generar una consulta SQL de la que no se espere un retorno.
        """
        
        self._connect()
        self._cursor.execute(query)
        self._database.commit()
        self._disconnect()

