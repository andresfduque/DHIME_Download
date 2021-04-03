# -*- coding: utf-8 -*-
"""
Created on Thu Apr 1 12:31:49 2021

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
            Se puede llamar del siguiente diccionario <Variables>.        
                        
            6_Department: Departamento alque pertenece la estación a descargar. Los nombres validos de departamentos son los siguientes:
            
            ("Amazonas", "Antioquia", "Arauca", "Archipiélago de San Andres, Providencia y Santa Catalina", "Atlantico", "Bogotá", "Bolivar",\
            "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila",\
            "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío", "Risaralda", "Santander", "Sucre",\
            "Tolima", "Valle del Cauca", "Vaupes", "Vichada")
            
            7_Code: Código de la estación a descargar.
            
            8_TimeWait (opcional): Parametro para indicar cuanto debe esperar el sistema para que carguen los elementos requeridos de la página web del
            DHIME. Para conexiones de internet lentas se puede aumentar el valor por defecto (10).

"""

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from zipfile import ZipFile

Variables = {'Brillo solar horario':'BSHG_CON', 'Brillo solar medio mensual':'BSHG_MEDIA_M', 'Brillo solar medio anual':'BSHG_MEDIA_A',\
             'Brillo solar total anual':'BSHG_TT_A', 'Caudal máximo diario':'Q_MX_D', 'Caudal medio diario':'Q_MEDIA_D', 'Caudal mínimo diario':'Q_MN_D',\
             'Caudal máximo mensual':'Q_MX_M', 'Caudal medio mensual':'Q_MEDIA_M', 'Caudal mínimo mensual':'Q_MN_M', 'Caudal medio anual':'Q_MEDIA_A',\
             'Caudal máximo anual':'Q_MX_A', 'Caudal mínimo anual':'Q_MN_A', 'Concentración media diaria en Kg/m3':'CM_KG/M3_D',\
             'Concentración media mensual en Kg/m3':'CM_M', 'Concentración media mínima mensual en Kg/m3':'CM_MN_M',\
             'Concentración media máxima mensual en Kg/m3':'CM_MX_M', 'Concentración media anual en Kg/m3':'CM_A', 'Concentración media mínima anual en Kg/m3':'CM_MN_A',\
             'Concentración media máxima anual en Kg/m3':'CM_MX_A', 'Concentración superficial promedio diaria de sedimentos':'CS_PROMEDIO_D',\
             'Dirección del viento cada 2 minutos':'DV_AUT_2', 'Dirección del viento cada 10 minutos':'DV_AUT_10',\
             'Dirección del viento vectorial 10 minutal media horaria':'DV_10_VECT_MEDIA_H', 'Dirección del viento de las 24 horas en grados (convencional)':'DVAG_CON',\
             'Dirección del viento vectorial 2 minutal media horaria':'DV_2_VECT_MEDIA_H', 'Dirección del viento vectorial 10 minutal media diaria':'DV_10_VECT_MEDIA_D',\
             'Dirección del viento máxima diaria':'DVMXAG_CON', 'Dirección del viento vectorial 2 minutal media diaria':'DV_2_VECT_MEDIA_D',\
             'Dirección del viento vectorial media diaria (convencional)':'DVAG_VECT_MEDIA_D', 'Dirección del viento vectorial media mensual (convencional)':'DVAG_VECT_MEDIA_M',\
             'Dirección del viento vectorial 10 minutal media mensual':'DV_10_VECT_MEDIA_M', 'Dirección del viento máxima mensual':'DVMXAG_MX_M',\
             'Dirección del viento vectorial 2 minutal media mensual':'DV_2_VECT_MEDIA_M', 'Dirección del viento vectorial media anual (convencional)':'DVAG_VECT_MEDIA_A',\
             'Dirección del viento vectorial 2 minutal media anual':'DV_2_VECT_MEDIA_A', 'Dirección del viento máxima anual':'DVMXAG_MX_A',\
             'Dirección del viento vectorial 10 minutal media anual':'DV_10_VECT_MEDIA_A', 'Evaporación total diaria':'EV_TT_D', 'Fenómeno Atmosférico de las 700, 1300 y 1800':'FA_CON',\
             'Fenómeno Atmosférico predominante diario':'FA_PREDO_D', 'Humedad relativa del aire a 2 metros cada 2 minutos':'HRA2_AUT_2',\
             'Humedad relativa del aire a 10 cm horaria':'HRA10_AUT_60', 'Humedad relativa del aire a 2 metros horaria':'HRA2_AUT_60',\
             'Humedad relativa de las 24 horas (gráfica)':'HRHG_CON', 'Húmeda relativa calculada horaria':'HR_CAL', 'Humedad relativa del aire a 2 metros mínima diaria':'HRA2_MN_D',\
             'Humedad relativa del aire 2 minutal a 2 metros (medición cada 2 minutos) mínima diaria':'HRA2_2_MN_D', 'Humedad relativa del aire a 10 cm máxima diaria':'HRA10_MX_D',\
             'Humedad relativa del aire a 10 cm media diaria':'HRA10_MEDIA_D', 'Húmeda relativa calculada mínima diaria':'HR_CAL_MN_D',\
             'Humedad relativa del aire a 2 metros media diaria':'HRA2_MEDIA_D', 'Humedad relativa del aire a 10 cm mínima diaria':'HRA10_MN_D',\
             'Humedad relativa del aire 2 minutal a 2 metros máxima diaria':'HRA2_2_MX_D', 'Humedad relativa del aire 2 minutal a 2 metros (medición cada 2 minutos) media diaria':'HRA2_2_MEDIA_D',\
             'Húmeda relativa calculada máxima diaria':'HR_CAL_MX_D', 'Humedad relativa del aire a 2 metros máxima diaria':'HRA2_MX_D', 'Húmeda relativa calculada mínima mensual':'HR_CAL_MN_M',\
             'Húmeda relativa calculada máxima mensual':'HR_CAL_MX_M', 'Humedad relativa del aire 2 minutal a 2 metros máxima mensual':'HRA2_2_MX_M',\
             'Humedad relativa del aire 2 minutal a 2 metros mínima mensual':'HRA2_2_MN_M', 'Humedad relativa del aire a 2 metros máxima mensual':'HRA2_MX_M',\
             'Humedad relativa del aire a 10 cm mínima mensual':'HRA10_MN_M', 'Humedad relativa del aire a 10 cm máxima mensual':'HRA10_MX_M',\
             'Humedad relativa del aire a 2 metros mínima mensual':'HRA2_MN_M', 'Humedad relativa del aire a 10 cm media mensual':'HRA10_MEDIA_M',\
             'Humedad relativa del aire 2 minutal a 2 metros media mensual':'HRA2_2_MEDIA_M', 'Humedad relativa del aire a 2 metros media mensual':'HRA2_MEDIA_M',\
             'Húmeda relativa calculada máxima anual':'HR_CAL_MX_A', 'Humedad relativa del aire a 10 cm media anual':'HRA10_MEDIA_A',\
             'Húmeda relativa calculada media anual':'HR_CAL_MEDIA_A', 'Humedad relativa del aire a 2 metros mínima anual':'HRA2_MN_A',\
             'Humedad relativa del aire a 10 cm mínima anual':'HRA10_MN_A', 'Humedad relativa del aire 2 minutal a 2 metros mínima anual':'HRA2_2_MN_A',\
             'Humedad relativa del aire a 2 metros media anual':'HRA2_MEDIA_A', 'Humedad relativa del aire a 10 cm máxima anual':'HRA10_MX_A',\
             'Humedad relativa del aire a 2 metros máxima anual':'HRA2_MX_A', 'Humedad relativa del aire 2 minutal a 2 metros media anual':'HRA2_2_MEDIA_A',\
             'Húmeda relativa calculada mínima anual':'HR_CAL_MN_A', 'Humedad relativa del aire 2 minutal a 2 metros máxima anual':'HRA2_2_MX_A',\
             'Nivel horario validado':'NIVEL_H', 'Nivel máximo diario':'NV_MX_D', 'Nivel mínimo diario':'NV_MN_D', 'Nivel medio diario':'NV_MEDIA_D',\
             'Nivel máximo mensual':'NV_MX_M', 'Nivel medio mensual':'NV_MEDIA_M', 'Nivel mínimo mensual':'NV_MN_M', 'Nivel medio anual':'NV_MEDIA_A',\
             'Nivel mínimo anual':'NV_MN_A', 'Nivel máximo anual':'NV_MX_A', 'Nubosidad de las 700, 1300 y 1800':'NB_CON', 'Nubosidad 19:00 HLC':'NB_19H00',\
             'Nubosidad 07:00 HLC':'NB_7h00', 'Nubosidad 13:00 HLC':'NB_13H00', 'Nubosidad 07:00 HLC media mensual':'NB_MEDIO7_M', 'Precipitación acumulada 10 minutos':'PT_AUT_10',\
             'Precipitación total horaria (sensor medición cada 10 minutos)':'PT_10_TT_H', 'Dias con lluvia >= 0,1 mm':'PTPM_DIAS_LLUVIA', 'Día pluviométrico':'PTPM_CON',\
             'Precipitación 10 minutal total diaria':'PT_10_TT_D', 'Radiación solar global cada dos minutos VALIDADA':'RSGVAL_AUT_2',\
             'Radiación solar global horaria VALIDADA':'RSGVAL_AUT_60', 'Radiación solar global diaria VALIDADA':'RSAG_CON', 'Radiación solar global acumulada diaria':'RSG _TT_D',\
             'Radiación solar global acumulada diaria mínima mensual':'RSG_TTD_MIN_M', 'Radiación solar global acumulada diaria máxima mensual':'RSG_TTD_MX_M',\
             'Radiación solar global media mensual':'RSG_MEDIA_M', 'Radiación UVA (longitud de onda 340 nm) media horaria':'RUVA340_MEDIA_H',\
             'Radiación UVA (longitud de onda 340 nm) máxima horaria':'RUVA340_MX_H', 'Radiación UVA (longitud de onda 380 nm) media horaria':'RUVA380_MEDIA_H',\
             'Radiación UVA (longitud de onda 380 nm) máxima horaria':'RUVA380_MX_H', 'Radiación UVB (longitud de onda 305 nm) media horaria':'RUVB305_MEDIA_H',\
             'Radiación visible (PAR) máxima horaria.':'RSVPAR_MX_H', 'Radiación UVB (longitud de onda 320 nm) media horaria':'RUVB320_MEDIA_H',\
             'Radiación UVB (longitud de onda 320 nm) máxima horaria':'RUVB320_MX_H', 'Radiación visible (PAR) Media horaria.':'RSVPAR_MEDIA_H',\
             'Radiación UVB (longitud de onda 305 nm) máxima horaria':'RUVB305_MX_H', 'Indice de radiación ultravioleta máxima horaria':'RUVINDICE_MX_H',\
             'Indice de radiación ultravioleta media horaria':'RUVINDICE_MEDIA_H', 'Temperatura seca de las 24 hora (gráfica)':'TSTG_CON',\
             'Temperatura húmeda de las 700, 1300 y 1800':'THSM_CON', 'Temperatura seca de las 700, 1300 y 1800':'TSSM_CON', 'Temperatura seca  máxima diaria':'TSTG_MX_D',\
             'Temperatura del Aire a 2 metros mínima diaria':'TA2_MN_D', 'Temperatura mínima del Aire a 10 cm absoluta diaria':'TAMN10_MN_D',\
             'Temperatura del Aire 2 minutal a 2 metros máxima diaria':'TA2_2_MX_D', 'Temperatura del Aire 2 minutal a 2 metros mínima diaria':'TA2_2_MN_D',\
             'Temperatura máxima diaria':'TMX_CON', 'Temperatura mínima diaria':'TMN_CON', 'Temperatura seca mínima diaria':'TSSM_MN_D',\
             'Temperatura seca máxima diaria':'TSSM_MX_D', 'Temperatura del Aire a 10 cm media anual':'TA10_MEDIA_A',\
             'Temperatura del Aire 2 minutal a 2 metros mínima anual':'TA2_2_MN_A', 'Temperatura húmeda media anual':'THSM_MEDIA_A',\
             'Temperatura máxima del Aire a 10 cm media anual':'TAMX10_MEDIA_A', 'Temperatura del punto de rocío mínima anual':'TPR_CAL_MN_A',\
             'Temperatura máxima media anual':'TMX_MEDIA_A', 'Temperatura del Aire 2 minutal a 2 metros máxima anual':'TA2_2_MX_A',\
             'Temperatura del punto de rocío media anual':'TPR_CAL_MEDIA_A', 'Temperatura mínima máxima anual':'TMN_MX_A',\
             'Temperatura húmeda máxima anual' :'THSM_MX_A', 'Temperatura húmeda mínima anual':'THSM_MN_A', 'Temperatura del Aire a 2 metros máxima anual':'TA2_MX_A',\
             'Temperatura del Aire a 2 metros mínima anual':'TA2_MN_A', 'Temperatura seca mínima anual':'TSSM_MN_A', 'Temperatura mínima media anual':'TMN_MEDIA_A',\
             'Temperatura máxima del Aire a 2 metros máxima absoluta anual':'TAMX2_MX_A', 'Temperatura mínima del Aire a 10 cm absoluta anual':'TAMN10_MN_A',\
             'Temperatura máxima del Aire a 10 cm mínima anual':'TAMX10_MN_A', 'Temperatura del Aire a 10 cm máxima anual':'TA10_MX_A',\
             'Temperatura del Aire a 10 cm mínima anual':'TA10_MN_A', 'Temperatura seca máxima anual':'TSSM_MX_A', 'Temperatura máxima mínima anual':'TMX_MN_A',\
             'Temperatura máxima del Aire a 2 metros media anual':'TAMX2_MEDIA_A', 'Temperatura del Aire 2 minutal a 2 metros media anual':'TA2_2_MEDIA_A',\
             'Temperatura mínima absoluta anual':'TMN_MN_A', 'Temperatura máxima absoluta anual':'TMX_MX_A', 'Temperatura del Aire a 2 metros media anual':'TA2_MEDIA_A',\
             'Temperatura máxima del Aire a 10 cm máxima absoluta anual':'TAMX10_MX_A', 'Temperatura del punto de rocío mínima diaria':'TPR_CAL_MN_D',\
             'Temperatura del punto de rocío media diaria':'TPR_CAL_MEDIA_D', 'Temperatura del punto de rocío máxima diaria':'TPR_CAL_MX_D',\
             'Temperatura del punto de rocío calculada horaria':'TPR_CAL', 'Transporte medio diario a partir de la CM':'TR_CM_D',\
             'Transporte medio diario a partir de la Ecuación de Qs':'TR_KT/D_QS_D', 'Transporte medio total mensual a partir de la CM':'TR_CM_TT_M',\
             'Transporte medio mensual a partir de la CM':'TR_CM_M', 'Transporte medio total mensual a partir de la Ecuación de Qs':'TR_QS_TT_M',\
             'Transporte medio máximo mensual a partir de la Ecuación de Qs':'TR_QS_MX_M', 'Transporte medio mensual a partir de la Ecuación de Qs':'TR_QS_M',\
             'Transporte medio máximo mensual a partir de la CM':'TR_CM_MX_M', 'Transporte medio máximo anual a partir de la CM':'TR_CM_MX_A',\
             'Transporte medio anual mensual a partir de la Ecuación de Qs':'TR_QS_MX_A', 'Transporte medio anual a partir de la Ecuación de Qs':'TR_QS_A',\
             'Transporte medio total anual a partir de la CM':'TR_CM_TT_A', 'Transporte medio anual a partir de la CM':'TR_CM_A',\
             'Transporte medio total anual a partir de la Ecuación de Qs':'TR_QS_TT_A', 'Velocidad vectorial del viento media diaria':'VVAG_VECT_MEDIA_D',\
             'Velocidad vectorial 10 minutal del viento media diaria':'VV_10_VECT_MEDIA_D', 'Velocidad del viento cada 2 min':'VV_AUT_2',\
             'Velocidad del viento cada 10 min':'VV_AUT_10', 'Velocidad del viento de las 24 horas':'VVAG_CON', 'Velocidad del viento 2 minutal media horaria':'VV_2_MEDIA_H',\
             'Velocidad 10 minutal del viento media horaria':'VV_10_MEDIA_H', 'Velocidad del viento máxima diaria':'VVMXAG_CON',\
             'Velocidad 10 minutal del viento media diaria':'VV_10_MEDIA_D', 'Velocidad del viento 2 minutal media diaria':'VV_2_MEDIA_D',\
             'Velocidad vectorial 2 minutal del viento media diaria':'VV_2_VECT_MEDIA_D', 'Velocidad vectorial del viento media mensual convencional':'VVAG_VECT_MEDIA_M',\
             'Velocidad del viento 2 minutal media mensual':'VV_2_MEDIA_M', 'Velocidad 10 minutal del viento media mensual':'VV_10_MEDIA_M',\
             'Velocidad vectorial 2 minutal del viento media mensual':'VV_2_VECT_MEDIA_M', 'Velocidad vectorial 10 minutal del viento media mensual':'VV_10_VECT_MEDIA_M',\
             'Velocidad del viento media anual convencional':'VVAG_MEDIA_A', 'Velocidad vectorial 2 minutal del viento media anual':'VV_2_VECT_MEDIA_A',\
             'Velocidad 10 minutal del viento media anual':'VV_10_MEDIA_A', 'Velocidad del viento 2 minutal media anual':'VV_2_MEDIA_A',\
             'Velocidad vectorial del viento media anual convencional':'VVAG_VECT_MEDIA_A', 'Velocidad vectorial 10 minutal del viento media anual':'VV_10_VECT_MEDIA_A'    
}

def DHIME_Download(Path,DateIni,DateFin,Parameter,Variable,Department,Code,TimeWait=10):
       
    # Abrir Google Chrome operado con Selenium cambiando la carpeta de descargas
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : Path.replace('/',"\\")}
    chrome_options.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(Path+'/Chromedriver.exe', options=chrome_options)
    
    # Abrir la página inicial del DHIME
    browser.get('http://dhime.ideam.gov.co/atencionciudadano/')
    
    #Aceptar los terminos y condiciones de la página
    try:
        button = WebDriverWait(browser, TimeWait*1.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".checkbox")))
    except:
        print("Tiempo de carga de la página superado, aumentar el valor de TimeWait")
        return
    button.click()
    button = browser.find_element_by_css_selector(".enable-btn")
    button.click()
    
    #Introducir las fechas de inicio y final de la descarga
    Date_ini = WebDriverWait(browser, TimeWait*1.5).until(EC.presence_of_element_located((By.ID, "datepicker")))
    Date_ini.click()
    Date_ini.clear()
    Date_ini.send_keys(DateIni)
    
    Date_fin = browser.find_element_by_id("datepicker1")
    Date_fin.click()
    Date_fin.clear()
    Date_fin.send_keys(DateFin)
    
    #Seleccionar parametro a descargar
    Par = browser.find_element_by_xpath("//div[@id='pnlEstandar']/table/tbody/tr/td[2]/span/span/span")
    Par.click()
    Par2 = browser.find_element_by_xpath("//li[contains(.,'"+Parameter+"')]")
    Par2.click()
    
    #Seleccionar variable a descargar
    Var = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@onclick,'"+Variable+"')]")))
    Var.click()
    
    #Seleccionar departamento
    Dep = browser.find_element_by_xpath("//div[@id='first']/table/tbody/tr/td[2]/span/span/span")
    Dep.click()
    time.sleep(TimeWait/4)
    Dep_Index = int(WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//li[contains(.,'"+Department+"')]"))).get_attribute('outerHTML').split('"')[9]) + 1
    Dep2 = browser.find_element_by_xpath("//ul[@id='deptos2_listbox']/li["+str(Dep_Index)+"]")
    Dep2.click()
    
    #Seleccionar municipio
    Mun = browser.find_element_by_xpath("//div[@id='first']/table/tbody/tr[2]/td[2]/span/span/span")
    Mun.click()
    Mun2 = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//ul[@id='municipio2_listbox']/li[2]")))
    Mun2.click()
    
    #seleccionar estación
    Est_cod = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//input[@value='"+Code+"']"))).get_attribute('outerHTML')
    Est_cod_sep = Est_cod.split()[1].replace('"',"").replace("id=idEstacionmetaData","")
    Est_cod_id = "//input[@id='checkMetaData"+Est_cod_sep+"']"
    
    Est = browser.find_element_by_xpath(Est_cod_id)
    Est.click()
    
    #Agregar a la consulta
    Search = browser.find_element_by_xpath("//div[@id='first']/div[5]/div")
    Search.click()
    
    #Iniciar descarga
    Download = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.XPATH, "//div[@id='second']/div/div[3]/div")))
    Download.click()
    
    #Aceptar terminos de uso
    Accept = WebDriverWait(browser, TimeWait).until(EC.presence_of_element_located((By.ID, "dijit_form_Button_2_label")))
    Accept.click()
    time.sleep(TimeWait*1.2)
    
    browser.close()
    
    # Extraer el archivo .csv del archivo comprimido descargado
    zf = ZipFile(Path+'/datos.zip', 'r')
    zf.extractall(Path)
    zf.close()
    
    # Cambiar el nombre del archivo extraido
    os.rename(Path+'/excel.csv.csv', Path+'/'+Code+'-'+Variable+'-'+DateIni.replace('/','')+'-'+DateFin.replace('/','')+'.csv')
    
    # Eliminar el comprimido
    os.remove(Path+"/datos.zip")

    print(Code+'-'+Variable+'-'+DateIni.replace('/','')+'-'+DateFin.replace('/','')+'.csv Descargado')

# Ejemplos
# DHIME_Download(Path="C:/Users/sanba/Downloads/AutomateDownloads",DateIni="31/07/2010", DateFin="15/08/2010", Parameter="PRECIPITACION", Variable=Variables["Precipitación acumulada 10 minutos"], Department="Bogotá", Code="21205012")
# DHIME_Download(Path="C:/Users/sanba/Downloads/AutomateDownloads",DateIni="31/07/2010", DateFin="15/08/2010", Parameter="EVAPORACION", Variable="EV_TT_D", Department="Bolivar", Code="29015040")

