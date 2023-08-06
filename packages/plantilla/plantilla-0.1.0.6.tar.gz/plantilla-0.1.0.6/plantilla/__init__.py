def importar_style():

  import os
  import matplotlib

  from pkg_resources import resource_string

  files = [
    'styles\\mecon.mplstyle',
  ]

  for fname in files:
    path = os.path.join(matplotlib.get_configdir(),fname)
    text = resource_string(__name__,fname).decode()
    open(path,'w').write(text)



def plantilla(proyecto=None, subproyecto=None, path_proyectos=None, new=False, globales=True):
    """Creador de Plantilla para la Oficina 825.
    Genera las carpetas correspondientes para cada proyecto (y subproyecto) y define las globales para Stata/Python
    (en Stata, son globales tradicionales. En Python, la funcion devuelve un diccionario con la key equivalente al nombre de la variable y value con el valor de esa variable)

    Args:
        @proyecto (str, optional): Nombre de la carpeta del proyecto. Tiene que existir. Para Stata, detecta la global $proyecto, o se puede escribir a mano. En Python si o si hay que escribirla
        @subproyecto (str, optional): Nombre de la carpeta del subproyecto. Tiene que existir dentro de {path_proyectos}/{proyecto}/scripts. En Python hay que escribirla, en Stata se puede acceder desde global
        @path_proyectos (str, optional): Ruta de la carpeta de proyectos. Evalúa ciertas carpetas por default, pero sino hay que explicitarla
        @new (bool, optional): Con True se crea la version nueva (>0.1.0, con data_raw y data_proc generales). Con False, la vieja (<0.1.0, con data_in y data_out particulares). 
        @globales (bool, optional): Con True se crean las globales, con False no (por si hay errores en Py y solo se quiere armar la estructura)


    Returns:
        dict: {"nombre_de_la_variable": "valor_de_la_variable"}
    """
    ### ARMAR plantilla_old (dejar andando los dos juntos, pero con default al viejo)
    
    
    import os
    import matplotlib
    import matplotlib.pyplot as plt
    from pathlib import Path

    try:
        plt.style.use('mecon.mplstyle')
    except:
        from site import getsitepackages
        site_packages = getsitepackages()
        for folder in site_packages:
            try:
                path_style = os.path.join(folder, 'plantilla', 'styles', 'mecon.mplstyle')
                path_stylelib = os.path.join(matplotlib.get_configdir(), 'stylelib')
                path_end_style = os.path.join(path_stylelib, 'mecon.mplstyle')
                Path(path_style).rename(path_end_style)
                plt.style.use(path_end_style)
            except:
                pass

    else:
        path_stylelib = os.path.join(matplotlib.get_configdir(), 'stylelib')
        path_end_style = os.path.join(path_stylelib, 'mecon.mplstyle')
        print(f'No se pudo importar el estilo. Mover a mano a el archivo "mecon.mplstyle" desde la carpeta de plantilla (ruta de python/Lib/site-packages/plantilla/styles) a {path_end_style} y activarlo con "plt.style.use("mecon.mplstyle")"')
            
    
    # from sfi import Macro

    # proyecto = Macro.getGlobal("proyecto")
    if new:

        try:
            from sfi import Macro
            proyecto = Macro.getGlobal("proyecto")
            subproyecto = Macro.getGlobal("subproyecto")
        except:
            if proyecto==None:
                raise NameError("Error. Globales no definidas (proyecto no definido)")
            else:   
                proyecto = proyecto
                subproyecto = subproyecto

        ### ARMAR test_paths para cada compu
        test_path = fr"C:\Users\Administrador\Documents\MECON\Proyectos\{proyecto}"
        
        

        if path_proyectos:
            path_proyecto = path_proyectos + '\\' + str(proyecto)
            path_data = os.path.dirname(os.path.dirname(path_proyecto)) + '\\' + 'data'

        elif os.path.isdir(test_path):
            path_proyecto = test_path
            path_data = os.path.dirname(os.path.dirname(path_proyecto)) + '\\' + 'data'

        else:
            path = os.path.normpath(os.getcwd() + os.sep + os.pardir) # Get padre de la ruta del archivo
            path_proyecto = path + '\\' + str(proyecto)
            path_data = os.path.dirname(os.path.dirname(path_proyecto)) + '\\' + 'data'
            if os.path.isdir(path_proyecto)==False:
                raise NameError(f"El directorio {path_proyecto} no fue encontrado, revisar nombre del proyecto")
        
        folders = []

        print(path_proyecto + fr'\scripts\{subproyecto}')
        print(path_data)

        if os.path.isdir(path_proyecto + fr'\scripts\{subproyecto}'):
            print("El directorio en scripts existe. Creando carpetas.")
            try:
                folders = [ r'\data_out',
                            fr'\data_out\{subproyecto}',
                            r'\docs',
                            r'\scripts',
                            fr'\scripts\{subproyecto}',
                            r'\outputs',
                            r'\outputs\figures',
                            fr'\outputs\figures\{subproyecto}',
                            r'\outputs\maps',
                            fr'\outputs\maps\{subproyecto}',
                            r'\outputs\tables',
                            fr'\outputs\tables\{subproyecto}',
                            ]

            except:
                folders = [ r'\data_out',
                            r'\docs',
                            r'\scripts',
                            r'\outputs',
                            r'\outputs\figures',
                            r'\outputs\maps',
                            r'\outputs\tables']

            # FOLDERS EN /Proyectos/proyecto
            for folder in folders:
                mkdir = path_proyecto + folder
                if not os.path.isdir(mkdir):
                    os.mkdir(mkdir)
                    print(mkdir, 'creado')
                else:
                    print(mkdir, 'ya existe')
                    
                    
            # Folders en /data/
            data_folders = [
                r'\data_raw',
                r'\data_proc'
            ]
            
            for folder in data_folders:
                mkdir = path_data + folder
                if not os.path.isdir(mkdir):
                    os.mkdir(mkdir) 
                    print(mkdir, 'creado')
                else:
                    print(mkdir, 'ya existe')
                
                    

        else:
            raise NameError(f"El directorio {path_proyecto + f'//scripts//{subproyecto}'} no existe. Crear una carpeta en scripts con el nombre del subproyecto.")
                
        # global path_datain	  
        # global path_dataout  
        # global path_scripts  
        # global path_figures  
        # global path_maps	  
        # global path_tables	  
        # global path_programas

        if globales:
            path_dataraw	= path_data + r'\data\data_raw'
            path_dataproc   = path_data + r'\data\data_proc'
            path_dataout    = path_proyecto + fr'\data_out\{subproyecto}'
            path_scripts    = path_proyecto + fr'\scripts\{subproyecto}'
            path_figures    = path_proyecto + fr'\outputs\figures\{subproyecto}'
            path_maps	    = path_proyecto + fr'\outputs\maps\{subproyecto}'
            path_tables	    = path_proyecto + fr'\outputs\tables\{subproyecto}'
            path_programas  = os.path.dirname(os.path.dirname(os.path.dirname(path_proyecto))) + '\\' + r'\0. Varios\scripts\Programas'


            try:
                from sfi import Macro
                Macro.setGlobal('path_user', path_proyecto)
                Macro.setGlobal('path_dataraw', path_dataraw)
                Macro.setGlobal('path_dataproc', path_dataproc)
                Macro.setGlobal('path_dataout', path_dataout)
                Macro.setGlobal('path_scripts', path_scripts)
                Macro.setGlobal('path_figures', path_figures)
                Macro.setGlobal('path_maps', path_maps)
                Macro.setGlobal('path_tables', path_tables)
                Macro.setGlobal('path_programas', path_programas)

            except:
                return { 
                    'path_proyecto':path_proyecto,
                    'path_dataraw':path_dataraw,	  
                    'path_dataout':path_dataout,  
                    'path_dataproc':path_scripts, 
                    'path_figures':path_figures,  
                    'path_maps': path_maps,	  
                    'path_tables':path_tables,	  
                    'path_programas':path_programas
                }
    else:
        try:
            from sfi import Macro
            proyecto = Macro.getGlobal("proyecto")
            subproyecto = Macro.getGlobal("subproyecto")
        except:
            if proyecto==None:
                raise NameError("Error. Globales no definidas.")
            else:   
                proyecto = proyecto
                subproyecto = subproyecto

        path_user = ''
        
        test_path = fr"C:\Users\Administrador\Documents\MECON\{proyecto}"


        if os.path.isdir(test_path):
            path_user = test_path

        elif path_proyectos:
            path_user = path_proyectos + '\\' + str(proyecto)

        else:
            path = os.path.normpath(os.getcwd() + os.sep + os.pardir) # Get padre de la ruta del archivo

            path_user = path + '\\' + str(proyecto)

            if os.path.isdir(path_user)==False:
                raise NameError("Error 404. Directorio no encontrado, revisar nombre del proyecto")
        
        folders = []

        print(path_user + fr'\scripts\{subproyecto}')

        if os.path.isdir(path_user + fr'\scripts\{subproyecto}'):
            
            print("El directorio en scripts existe. Creando carpetas.")
            
            try:
                folders = [r'\data',
                            r'\data\data_in',
                            r'\data\data_out',
                            fr'\data\data_out\{subproyecto}',
                            r'\docs',
                            r'\scripts',
                            fr'\scripts\{subproyecto}',
                            r'\outputs',
                            r'\outputs\figures',
                            fr'\outputs\figures\{subproyecto}',
                            r'\outputs\maps',
                            fr'\outputs\maps\{subproyecto}',
                            r'\outputs\tables',
                            fr'\outputs\tables\{subproyecto}']

            except:
                folders = [ r'\data',
                            r'\data\data_in',
                            r'\data\data_out',
                            r'\docs',
                            r'\scripts',
                            r'\outputs',
                            r'\outputs\figures',
                            r'\outputs\maps',
                            r'\outputs\tables']


            for folder in folders:

                mkdir = path_user + folder
                if os.path.isdir(mkdir)==False:
                    os.mkdir(mkdir)
                    print(mkdir, 'Creado')
                else:
                    print(mkdir, 'ya existe')

        else:
            raise NameError("El directorio en scripts no existe. Por favor, crear una carpeta en scripts con el nombre del subproyecto.")
                
        # global path_datain	  
        # global path_dataout  
        # global path_scripts  
        # global path_figures  
        # global path_maps	  
        # global path_tables	  
        # global path_programas

        
        path_datain	   = path_user + r'\data\data_in'
        path_dataout   = path_user + fr'\data\data_out\{subproyecto}'
        path_scripts   = path_user + fr'\scripts\{subproyecto}'
        path_figures   = path_user + fr'\outputs\figures\{subproyecto}'
        path_maps	   = path_user + fr'\outputs\maps\{subproyecto}'
        path_tables	   = path_user + fr'\outputs\tables\{subproyecto}'
        path_programas = path_user + r'"C:\Users\Administrador\Documents\MECON\0. Varios\scripts\Programas"'


        try:
            from sfi import Macro
            Macro.setGlobal('path_user', path_user)
            Macro.setGlobal('path_datain', path_datain)
            Macro.setGlobal('path_dataout', path_dataout)
            Macro.setGlobal('path_scripts', path_scripts)
            Macro.setGlobal('path_figures', path_figures)
            Macro.setGlobal('path_maps', path_maps)
            Macro.setGlobal('path_tables', path_tables)
            Macro.setGlobal('path_programas', path_programas)

        except:
            return [
                path_user,
                path_datain,	  
                path_dataout,  
                path_scripts, 
                path_figures,  
                path_maps,	  
                path_tables,	  
                path_programas
            ]

def globales(proyecto, subproyecto=None, path_proyectos=None):
    import os

    
    test_path = fr"C:\Users\Administrador\Documents\MECON\Proyectos\{proyecto}"
        
        

    if path_proyectos:
        path_proyecto = path_proyectos + '\\' + str(proyecto)
        path_data = os.path.dirname(path_proyecto) + '\\' + 'data'

    elif os.path.isdir(test_path):
        path_proyecto = test_path
        path_data = os.path.dirname(path_proyecto) + '\\' + 'data'

    else:
        path = os.path.normpath(os.getcwd() + os.sep + os.pardir) # Get padre de la ruta del archivo
        path_proyecto = path + '\\' + str(proyecto)
        path_data = os.path.dirname(path_proyecto) + '\\' + 'data'
        if os.path.isdir(path_proyecto)==False:
            raise NameError(f"El directorio {path_proyecto} no fue encontrado, revisar nombre del proyecto")

    path_dataraw	= path_data + r'\data\data_raw'
    path_dataproc   = path_data + r'\data\data_proc'
    path_dataout    = path_proyecto + fr'\data_out\{subproyecto}'
    path_scripts    = path_proyecto + fr'\scripts\{subproyecto}'
    path_figures    = path_proyecto + fr'\outputs\figures\{subproyecto}'
    path_maps	    = path_proyecto + fr'\outputs\maps\{subproyecto}'
    path_tables	    = path_proyecto + fr'\outputs\tables\{subproyecto}'
    path_programas  = os.path.dirname(os.path.dirname(path_proyecto)) + '\\' + r'\0. Varios\scripts\Programas'


    try:
        from sfi import Macro
        Macro.setGlobal('path_user', path_proyecto)
        Macro.setGlobal('path_dataraw', path_dataraw)
        Macro.setGlobal('path_dataproc', path_dataproc)
        Macro.setGlobal('path_dataout', path_dataout)
        Macro.setGlobal('path_scripts', path_scripts)
        Macro.setGlobal('path_figures', path_figures)
        Macro.setGlobal('path_maps', path_maps)
        Macro.setGlobal('path_tables', path_tables)
        Macro.setGlobal('path_programas', path_programas)

    except:
        return { 
            'path_proyecto':path_proyecto,
            'path_dataraw':path_dataraw,	  
            'path_dataout':path_dataout,  
            'path_dataproc':path_scripts, 
            'path_figures':path_figures,  
            'path_maps': path_maps,	  
            'path_tables':path_tables,	  
            'path_programas':path_programas
        }
    




    
if __name__ == "__main__":
    plantilla(sys.argv[1], sys.argv[2])
