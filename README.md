# DHIME_Download

@author: John Alexander Sandoval Barrera. Ingeniero Civil UNAL. Estudiante Msc Recursos Hidráulicos UNAL.
email: jasandovalb@unal.edu.co
Linkedin : https://www.linkedin.com/in/jasandovalb/

Este script permite automatizar la descarga de datos del portal DHIME del IDEAM

Version 0:  Se define la función DHIME_Download que permite automatizar la descarga de datos
            del portal DHIME del IDEAM. Los parámetros a pasar a la función son:

            1_Path: Dirección de la carpeta en donde se van a guardar el archivo csv             
            
            Nota: En la direccción elegida se debe colocar el archivo Chromedrive.exe. El Webdriver
            de Chrome se puede descargar desde https://chromedriver.chromium.org/downloads.
            
            2_DateIni: Fecha inicial del periodo a descargar. Fotmato dd/mm/yyyy.
            3_DateFin: Fecha final del periodo a descargar. Fotmato dd/mm/yyyy. 

            Nota: Se debe haber confirmado previamente el periodo de disponibilidad de datos para la estación
            a descargar. Adicionalmente, el periodo a descargar no debe ser muy extenso o no se hará la descarga.
            Si se requiere un periodo largo se recomienda dividirlo en sub-periodos, descargar los archivos haciendo
            uso de la función dentro de un ciclo y luego unir los .csv.
            
            4_Parameter: Parametro a descargar. Se puede escoger entre los siguientes:

            ("BRILLO SOLAR", CAUDAL", "CM", "CS", "DIR VIENTO", "EVAPORACION", "FEN ATMOS", "HUM RELATIVA", "NIVEL", "NUBOSIDAD",\
             "PRECIPITACION", "RAD SOLAR", "RAD UV", "Sin dimensiones", "TEMPERATURA", "TM", "VEL VIENTO")

            5_Variable: Código de la Variable a descargar. La variable debe corresponder con el parametro definido. 
            Se puede llamar del diccionario <Variables>.        
                        
            6_Department: Departamento alque pertenece la estación a descargar. Los nombres validos de departamentos son los siguientes:
            
            ("Amazonas", "Antioquia", "Arauca", "Archipiélago de San Andres, Providencia y Santa Catalina", "Atlantico", "Bogotá", "Bolivar",\
            "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila",\
            "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío", "Risaralda", "Santander", "Sucre",\
            "Tolima", "Valle del Cauca", "Vaupes", "Vichada")
            
            7_Code: Código de la estación a descargar.
            
            8_TimeWait (opcional): Parametro para indicar cuanto debe esperar el sistema para que carguen los elementos requeridos de la página web del
            DHIME. Para conexiones de internet lentas se puede aumentar el valor por defecto (10).
