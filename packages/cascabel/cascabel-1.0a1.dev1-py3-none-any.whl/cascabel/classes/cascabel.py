
from genericpath import isfile
import os, sys, shutil, colorama
from urllib import request
cmd_dir  = os.getcwd()
file_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/").replace("/classes", "")

class Cascabel:
    
    VERSION = "1.0a1.dev1"
    #================================================================================================
    
    def print_simplify_logo (self):

        w_c = colorama.Style.RESET_ALL
        y_c = colorama.Fore.YELLOW

        logo =   y_c + "   _______  _\n"
        logo +=  y_c + "  /  __  c\\|_|\n"
        logo +=  y_c + " |  /  \__/|__|\n"
        logo +=  y_c + " |  |      | __|\n"
        logo +=  y_c + " |  \__/\\  | |\n"
        logo +=  y_c + "  \_____/ |_/  versión " + self.VERSION + "\n" + w_c

        print(logo)
        

    def print_logo (self):

        clear_command = 'cls' if os.name in ('nt', 'dos') else 'clear'
        os.system(clear_command)

        w_c = colorama.Style.RESET_ALL #Si la consola es oscura se muestra de color blanco y viceversa.
        y_c = colorama.Fore.YELLOW

        logo =   f"{y_c}   _______  {w_c}                       _            {y_c} _\n"
        logo +=  f"{y_c}  /  __  c\\{w_c}                       | |          {y_c} |_|\n"
        logo +=  f"{y_c} |  /  \__/{w_c}__ _  ___   ___   __ _ | |__    ___  {y_c}|__|\n"
        logo +=  f"{y_c} |  |     {w_c}/ _' |/ __| / __| / _' || '_ \  / _ \\{y_c} | __|\n"
        logo +=  f"{y_c} |  \__/\\{w_c}| (_| |\__ \| (__ | (_| || |_) ||  __/{y_c} | |\n"
        logo +=  f"{y_c}  \_____/ {w_c}\__,_||___/ \___| \__,_||_.__/  \___|{y_c}|_/  versión {self.VERSION} \n {w_c}"

        print(logo)

        #import platform
        
        #if os.path.isfile(f"{os.getcwd()}/routes.py") and os.path.isfile(f"{os.getcwd()}/config.py") and os.path.isfile(f"{os.getcwd()}/execute.py"):
        #    is_project_dir = "Si"
        #else:
        #    is_project_dir = "No"
            
    
        #print(' Sistema Operativo:', platform.system() )
        #print(' Platafotma       :', sys.platform)
        #print(' Distribucion     :', platform.platform())
        #print(' Version de python:', sys.version.replace('\n',''))
        #print(' Version dict     :', sys.version_info)
        #print(' Ejecutable actual:', sys.executable)
        #print(' Argumentos       :', sys.argv)
        #print(' Ruta actual      :', os.getcwd())
        #print(' Ruta de projecto?:', is_project_dir)
        #print(' Ruta de ejecución:', os.path.dirname(os.path.realpath(__file__)))
        #print('')


      

    def catch_error(self):

        w_c = colorama.Fore.WHITE
        y_c = colorama.Fore.YELLOW

        Cascabel().print_logo()

        from cascabel.dictionaries.commands import commands, full_commands
        
        print(" Comando no valido")

        import difflib
        import itertools

        keys = list(commands.keys())
        values = list(itertools.chain.from_iterable(commands.values()))

        all_words = keys + values

        coincidences = difflib.get_close_matches(sys.argv[1], all_words)

        if len(coincidences) != 0:

            coincidence = coincidences[0]

            if coincidence in keys:
                possible_command = full_commands[coincidence]
            else:
                for key, value in commands.items():
                    if coincidence in value:
                        possible_command = full_commands[key]
                        break
                    
            print(f"\n ¿Quisiste ejecutar el siguiente comando '{y_c}{possible_command}{w_c}' ?")


    def verify_libraries(self):
        self.print_logo()

        w_c = colorama.Style.RESET_ALL
        y_c = colorama.Fore.YELLOW
        r_c = colorama.Fore.RED

        print(y_c + " Librerias Necesarias" + w_c)

        try:
            import flask
            print(" |- Flask  : Instalado")
        except:
            print(" |- Flask  : " + r_c + "No instalado" + w_c)

        try:
            import dotenv 
            print(" |- Dotevn: Instalado")
        except:
            print(" |- Dotevn: " + r_c + "No instalado" + w_c)

        print(y_c + "\n Librerias Opcionales" + w_c)

        #try:
        #    import bcrypt
        #    print(" |- Bcrypt : Instalado")
        #except:
        #    print(" |- Bcrypt : " + r_c + "No instalado" + w_c)

        try:
            import MySQLdb 
            print(" |- MySqldb: Instalado")
        except:
            print(" |- MySqldb: " + r_c + "No instalado" + w_c)


        try:
            import flask_wtf
            print(" |- Flask-WTF: Instalado")
        except:
            print(" |- Flask-WTF: " + r_c + "No instalado" + w_c)


        print("\n Puedes instalar las librerias manualmente o utilizando " + y_c + "'--install_libraries'" + w_c)

    def install_libraries(self):

        import platform
        
        w_c = colorama.Style.RESET_ALL #Si la consola es oscura se muestra de color blanco y viceversa.
        y_c = colorama.Fore.YELLOW

        executable = sys.executable

        self.print_logo()

        if (sys.version).find('3.') > -1:
   
            try:
                import flask
                return_code_1 = '0'
            except:
                self.print_logo()
                return_code_1 = os.system(f"{executable} -m pip install Flask")
                
            try:
                import dotenv
                return_code_2 = '0' 
            except:
                self.print_logo()
                return_code_2 = os.system(f"{executable} -m pip install python-dotenv")

            try:
                import MySQLdb 
                return_code_3 = '0'
            except:
                self.print_logo()

                return_code_3 = os.system(f"{executable} -m pip install mysqlclient") #si tira errorse procedera a realizar comandos extras segun sistema op

                if str(return_code_3) != '0':
                    if platform.system() == "Windows":

                        return_code_3 = os.system("python -m pip install mysqlclient")

                    elif platform.system() == "Linux":
                        self.print_logo()
                        print(f" --mysqlclient --")
                        print(f' -> {y_c}default-libmysqlclient-dev{w_c} -> mysqlclient')
                        print()
                        return_code_tmp = os.system("sudo apt install default-libmysqlclient-dev")

                        self.print_logo()
                        print(f" --mysqlclient --")
                        print(f' -> default-libmysqlclient-dev -> {y_c}mysqlclient{w_c}')
                        print()
                        return_code_3   = os.system(f"{executable} -m pip install mysqlclient")

                    elif platform.system() == "Darwin":

                        self.print_logo()
                        print(f" --mysqlclient --")
                        print(f' -> {y_c}Homebrew{w_c} -> mysql -> mysqlclient')
                        print()

                        return_code_tmp = os.system('brew -v') #verifica si esta instalado brew
                        
                        print(return_code_tmp)
                        if str(return_code_tmp) != "0":
                            return_code_tmp = os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
                        
                        self.print_logo()
                        print(f" --mysqlclient --")
                        print(f' -> Homebrew -> {y_c}mysql{w_c} -> mysqlclient')
                        print()

                        return_code_tmp = os.system('brew list mysql') #verifica si esta instalado mysql

                        if str(return_code_tmp) != "0":
                            return_code_tmp = os.system('brew install mysql')

                        self.print_logo()
                        print(f" --mysqlclient --")
                        print(f' -> Homebrew -> mysql -> {y_c}mysqlclien{w_c}')
                        print()

                        return_code_3 = os.system(f"{executable} -m pip install mysqlclient")
            

            try:
                import flask_wtf
                return_code_4 = 0
            except:
                self.print_logo()
                return_code_4 = os.system(f"{executable} -m pip install Flask-WTF")

            self.print_logo()
            print(" flask:", return_code_1)    
            print(" dot_env:", return_code_2)  
            print(" mysqlclient:", return_code_3)  
        else:
            print(" Esta función solo esta disponible para python 3.8")

       
    def show_info(self):

        self.print_logo()

        print(" Versión de python : " + sys.version.split(" ")[0] + "\n")
        print(" Desarrollado por Ignacio Aguilera")

    def show_help(self):
        self.print_logo()

        from cascabel.dictionaries.commands import full_commands
    
        for key, command in full_commands.items():
            print(f' {key.ljust(20)} -> {command}')

    def create_new_project(self):

        project_name = sys.argv[2].lower()
        project_dir  = f'{cmd_dir}/{project_name}/'
        template_dir = f'{file_dir}/data/template/project/'

        if os.path.isdir((project_dir)):
            self.print_logo()
            print(f" Ya existe una carpeta con el nombre '{project_name}' en el directorio actual")
        else:
            self.print_logo()
            shutil.copytree(template_dir, project_dir, ignore=None)
            print(" La plantilla del proyecto ha sido creada correctamente")
    
    def make_database(self):
        
        self.print_logo()

        database_name = sys.argv[2].lower()
        database_class_name = database_name.replace("_", " ").capitalize().replace(" ", "")
        project_dir  = f'{cmd_dir}/'
        db_template_dir = f'{file_dir}/data/template/database/NAME_database.py'

        content = open(db_template_dir, "r").read().replace("NAME", database_class_name)
        
        if os.path.isdir(project_dir + "databases/databases/"):
            if not os.path.isfile(project_dir + "databases/databases/" + database_name + ".py"):
                file = open(project_dir + "databases/databases/" + database_name + "_database.py", "w")
                file.write(content)
                file.close()

                print("la base de datos ha sido creada correctamente")
            else:
                print("Error el archivo ya existe")
        else:
            print("Directorio invalido")

    def make_controller(self):

        self.print_logo()

        controller_name = sys.argv[2].lower()
        controller_class_name = controller_name.replace("_", " ").capitalize().replace(" ", "") + "Controller"

        project_dir  = f'{cmd_dir}/'
        controller_template_dir = f'{file_dir}/data/template/controller/simple_controller.py'

        content = open(controller_template_dir, "r").read().replace("NAME", controller_class_name)
        
        if os.path.isdir(project_dir + "app/controllers/") and os.path.isfile(project_dir + "routes.py"):
            if not os.path.isfile(project_dir + "app/controllers/" + controller_name +"_controller.py"):
                file = open(project_dir + "app/controllers/" + controller_name + "_controller.py", "w")
                file.write(content)
                file.close()

                routes_content = open(project_dir + "routes.py", "r+").read()
                import_stat = f"\nfrom app.controllers.{controller_name}_controller import {controller_class_name}\n"
                import_route_stat = "from resources.routes.route import Route\n"
                add_route_stat = f"Route().add_route(app, 'GET', '/{controller_name}',  {controller_class_name}().index , '{controller_name}_index') \n"
                

                if routes_content.count(import_route_stat) == 0:
                    routes_content = import_route_stat + routes_content +  import_stat + add_route_stat
                    
                else:
                    routes_content = routes_content +import_stat + add_route_stat
                
                file = open(project_dir + "routes.py", "w").write(routes_content)

                print(" El controlador sido creada correctamente")
            else:
                print(" Error el archivo ya existe")
        else:
            print(" Directorio invalido")

    def make_request(self):
        
        self.print_logo()

        request_name = sys.argv[2].lower()
        request_class_name = request_name.replace("_", " "). capitalize().replace(" ", "") + "Request"

        project_dir  = f'{cmd_dir}/'
        request_template_dir = f'{file_dir}/data/template/request/request.py'

        content = open(request_template_dir, "r").read().replace("NAME", request_class_name)

        if not os.path.isdir(project_dir + "app/requests/") or not os.path.isfile(project_dir + "routes.py"):
            print(" Directorio invalido")
            return None

        if os.path.isfile(project_dir + "app/requests/" + request_name +"_controller.py"):
            print(" Error el archivo ya existe")
            return None

        file = open( f"{project_dir}app/requests/{request_name}_request.py", "w")
        
        file.write(content)
        file.close()

    def make_manager_controller(self):

        self.print_logo()

        controller_name = sys.argv[2].lower()
        controller_class_name = controller_name.replace("_", " ").capitalize().replace(" ", "") + "Controller"

        project_dir  = f'{cmd_dir}/'
        controller_template_dir = f'{file_dir}/data/template/controller/manager_controller.py'

        content = open(controller_template_dir, "r").read().replace("NAME", controller_class_name)
        
        if not os.path.isdir(project_dir + "app/controllers/") or not os.path.isfile(project_dir + "routes.py"):
            print(" Directorio invalido")
            return None
        
        if os.path.isfile(project_dir + "app/controllers/" + controller_name +"_controller.py"):
            print(" Error el archivo ya existe")
            return None
        
        file = open(project_dir + "app/controllers/" + controller_name + "_controller.py", "w")
        file.write(content)
        file.close()

        routes_content = open(project_dir + "routes.py", "r+").read()
        import_stat = f"\nfrom app.controllers.{controller_name}_controller import {controller_class_name}\n"
        import_route_stat = "from resources.routes.route import Route\n"
        add_route_stat =  f"Route().add_route(app, 'GET', '/{controller_name}',  {controller_class_name}().index , '{controller_name}_index') \n"
        add_route_stat += f"Route().add_route(app, 'GET', '/{controller_name}/view/<id>',  {controller_class_name}().view , '{controller_name}_view') \n"
        add_route_stat += f"Route().add_route(app, 'POST', '/{controller_name}/store',  {controller_class_name}().store , '{controller_name}_store') \n"
        add_route_stat += f"Route().add_route(app, 'POST', '/{controller_name}/update/<id>',  {controller_class_name}().update , '{controller_name}_update') \n"
        add_route_stat += f"Route().add_route(app, 'POST', '/{controller_name}/delete/<id>',  {controller_class_name}().delete , '{controller_name}_delete') \n"

        if routes_content.count(import_route_stat) == 0:
            routes_content = import_route_stat + routes_content +  import_stat + add_route_stat
            
        else:
            routes_content = routes_content +import_stat + add_route_stat
        
        file = open(project_dir + "routes.py", "w").write(routes_content)

        print(" El controlador sido creada correctamente")
       
            

