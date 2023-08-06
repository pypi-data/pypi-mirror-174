# BLC Data Analytics tools package

Data Analytics helper functions to work with inside BLC's Cloud system.

# Changelog
## Version 0.0.20
* **DatosCROM()**
    - interpretar_incidencias_bajo_iec61400() made more efficient, while keeping compatibility with pandas >= 1.5.0
    - _identificar_indisponibilidades() pgen and ppos parameters were added, to further improve filtering capacity
* **TablasVC()**
    - Added "potencia=False" parameter to consultar_agrupamientos(), consultar_equipos_no_agrupamientos() 

## Version 0.0.19
* **DatosCROM()**
    - Fixed bug: interpretar_incidencias_bajo_iec61400() was experiencing problems with pandas >= 1.5.0, and had a problem with the index selection statement at the beginning.
    - Added experimentally: _identificar_indisponibilidades(duracion=30)

## Version 0.0.18
* **DatosCROM()**
    - .exportar() now flattens MultiIndex columns, freezes panes and formats floats, for easier view on Excel.
    - Added "invalidar_datos_seg_congelados" initialization parameter (default = False)
    - Fixed bug: .exportar() throwing error when curvas_de_potencia or consolidado held more than 1 Dataframe
    - Fixed bug: .interpretar_incidencias_bajo_iec61400() now trims final result between fecha_i and fecha_f
    - Fixed bug: .elaborar_curvas_de_potencia() wasn't working properly with filtro_n >1

## Version 0.0.17
* **fechas submodule**
    - Added .sem_dia_1(date,offset=0) function. Returns first day of week of the given date + given offset in days (offset can be negative)
    - Added .sem_act_dia_1(offset=0) function. Returns first day of current week + given offset in days
    - Added .año_op(fecha_actual,fecha_cod) function. Returns the current contractual year based on the two dates (First year is 1, not 0)
* **DatosCROM()**
    - adjusted how xlsx files processing time is calculated
    - adjusted how .pickle files are created/read. Compression was added through bz2
    - consolidado attribute is now called consolidado_redux, which is a subset of columns of consolidado
    - consolidado attribute now holds all the original data, but resampled to the users' input sample rate, excluding categorical variables
    - consultar_equipos_parque() and consultar_equipos_parque_no_agrupamientos() are now called consultar_equipos() and consultar_equipos_no_agrupamientos()
    - __iec61400_preparar_df_vacio_minutal() and it's aux methods are now more efficient
    - Added variables "Gen", "Con", "Pos" as boolean series for each equipment, into the datos_seg dataframe
    - Added columns "ENS_Lim","ENS_LimExt","ENS_LimInt","ENS_Ind","ENS_IndExt,"ENS_IndInt" to "consolidado" report
    - Added variable "Datos_%" which indicates the ammount of not null data per row, per element, into the datos_seg dataframe
    - Added variable "Registros" which indicates the ammout of rows (measured in time) on the excel file for that given element. Should alwasy equal 24
    - Fixed bug: .__procesar_d10s_5i() wasn't ensuring boolean dtypes for 'Gen','Con' and 'Pos', which impacted negatively on .elaborar_reporte_consolidado()
    - Fixed bug: .consolidar_todo() wasn't working with PEGARCIG 
    - Fixed bug: .consolidar_todo() wasn't working adding up HOUR columns properly (the rest was fine)
    - Fixed bug: .consolidar_todo() wasn't finishing if there weren't any incidents for a given park on a given time window
    - Fixed bug: .explotar_incidencias() now works properly if there aren't any incidents on a given time window
    - Fixed bug: .exportar() was exporting empty dataframes, since they were not "None"
    - Fixed bug: Roll-up of availability parameters wasn't being done correctly. Now groupings are the mean or logic operator of their groupped elements.    
    - Fixed bug: 10s pre-processing: Wind_dir_r was not being saved correctly for 'PLANT' element on self.datos_seg
    - Fixed bug: 10 second data is now being completed (in case of missing 10second records) with null values. This could have lead to serious problems when 
    - Fixed bug: On many methods. From pandas >= 1.5.0 numpy series where linked and not copied when creating a new df. This created many bugs throughout the whole program. 
    - unloading incidents to the 10 second data, since the main mechanism behind it is selection trhough .loc[t_stamp,:] 
* **TablasVC()**
    - Added attributes .habilitaciones and .tipohabilitaciones which are new tables of "datos básicos". They contain COD related information of each plant
    - Added .consultar_cod(nemo_parque='',uc='') function, to quickly find out about a plant's COD (Birthday) date (grabs from the table above)
    - Added .consultar_año_op(fecha_actual,feca_cod) function. Returns the contractual year (Contractual age) of a power plant
    - Added .__crear_dict_tipo_empresa(). Which fills in thre internal attributes: _empresas_bop, _empresas_gen, _empresas_grid
    - Fixed bug: .consultar() would fetchdatos_basicos from offline file even when 'online' parameter was set. This was due to:
      -  a logic error of variable db_off inside .consultar()
      -  the order in which instructions were executed
    - Fixed bug: __procesar_incidencias_it2() wasn't executing properly when cargar_datos_basicos = 'offline' was set. Solved by calling the new function .__crear_dict_tipo_empresa() before business mapping
    - Fixed bug: Desconecting twice from DB when fetching incidencias
    - Fixed bug: __combinar_incidencias_locales_y_online() wasn't working properly. Duplicate dropping should only be done by 'ID'
    - Refactored __asignar_datos() .method, to make it modular per table

## Version 0.0.16
* **DatosCROM()**
    - Added data invalidation when processing 10 second data. Now consecutive values of P, Q, Wind, Wind_dir and PPos != 0 and != max (for Ppos) are replaced with np.nan
    - Fixed bug when selecting no .parques ( [] ) and initializing a DatosCROM object
    - Fixed bug when truying to export specific reports through the generating functions (ie elaborar_curvas_de_potencia, interpretar_bajo_iec61400, etc.) and seeting the "exportar" parameter to True
    - Fixed bug. PI wasn't being correctly calculated. (* instead of / was being used)
    - Added "filtro_n" parameter to .elaborar_curvas_de_potencia(), to only show results with an n_count >= n per bin. Default 0 (deactivated)
    - Added feature. Ppos is being calculated if column doesn't exist, based on Curvas_de_potencia.xlsx on BLC's cloud under blc.get_dc_cfg() directory
    - "clientes" initializing parameter was removed (little use for it)
    - "solo_CROM" initializing parameter was removed (little use for it)
* **TablasVC()**
    - Improved the processing of incidents, now "Origin" is "NA" and np.nan resistent. Default = "INT"
    - Fixed bug through which a filter for discarded incidents wasn't working.
    - Refactored processing of incidents, it's more readable now

## Version 0.0.15
* **DatosCROM()**
    - .exportar() was added. Helper function to export all loaded reports to xlsx format.
    - .explotar_incidencias() now takes in optional export parameters.
    - .incidencias_interpretar_bajo_iec61400() now takes in optional export parameters.
    - .incidencias_identificar_solapamientos() was added.
    - "curvas_de_potencia" parameter added while initializing, to force power curves to be computed automatically
    - .elaborar_curvas_de_potencia() is now more resistent to failures. Powercurves can be elaborated without having to process incidents before, although not recommended if user doesn't know what he is doing.
    - changed how __renombrar_lvl0() works, now it must be feed the equipment names.
* **TablasVC()**
    - fixed a bug, where .consultar_equipos_parque_no_agrupamientos would return "PLANT" twice for GRIOEO
    - "cargar_incidencias" and "cargar_datos_basicos" parameters added while initializing, with possible values being [Flase, True, 'offline', 'online']
    - now queries per default active incidents from the 1st day of two months prior to today (if True or 'online' values where passed to "cargar_incidencias" parameter). Then concatenates obtained results with offline results (if there are any).

## Version 0.0.14
* **TablasVC()**
    - Fixed bug: Corrected functions that took equipments from blctools.TablasVC().conjuntogeneradores, now reading from .tipoequipo
    - Fixed bug: Now Parks without any grouping of it's generators can return the generators without grouping. Special Case: PEGARCIG
* **SQLConnector()**
    - now decrypts login data from BLC's secure fileserver.
* **DatosCROM()**
    - .consultar_equipos_parque() now retrieves the right elements if the plant doesn't havy any other grouping stages
    - .consultar_equipos_por_agrupamiento() now returns an empty list if the plant doesn't havy any other grouping stages
    - .rpt_consolidado(granularidad='1D') was added.
    -  "forzar_reprocesamiento" parameter added while initializing, to force re-process 10 second data.
    - .rpt_curvas_de_potencia() was added
    - changed the behaviour of .fecha_i and .fecha_i setters. They now attempt to update "incidencias" and "archivos" depending on the values of fecha_i and fecha_f, but the setters dont try to order the dates automatically, which lead to an unwanted behaviour.
    - Changed completely how DatosCROM() now proceses raw data (10 seconds and Incidencias). It's more efficient, and the heavy lifting occurs while processing the 10-second data. Now index has 1 column (Time) and columns have a 3 level structure (p,e,v) = Park, Element, Variable

## Version 0.0.13
* Created SQLConnector class to migrate to SQLAlchemy
* blctools.TablasVC now inherits from SQLConnector

## Version 0.0.12
* Function blctools.fechas.obtener_periodo() was added (moved from blctools.ReporteBase())
* Added more parameter flexibility within all functions inside blctools.fechas.
* Objects PPO(), DTE() and DatosCROM() now accept the "periodo" initialization parameter (overrides fecha_i and fecha_f).
* bjects blctools.DatosCROM() and blctools.TablasVC() have now the "solo_CROM=False" initialization parameter.
* function blctools.TablasVC.consultar_nemoCammesa() has now the "solo_CROM=False" argument  

## Version 0.0.11
* Corrected blctools.PPO.periodo('mes_anterior')
* Function ReporteBase.a_excel() accepts now the parameter "exportar_consulta=bool"
* Objects PPO() and DTE() now accept the following initialization parameters
    - "filtro"
    - "periodo" (overrides fecha_i and fecha_f)
* No more unnecessary warnings on changing the "filtro" parameter
* Function blctools.fechas.mes_dia_1() and blctools.fechas.mes_ult_dia() now validate dates using blctools.fechas.validar_fechas()
* Functions blctools.fechas.validar_fecha() and .validar_fechas() now have a parameter "prevenir_futuro=True" as default, to prevent future dates or not.
* Fixed a bug, when changing "filtro" on functions of child classes of DTE() or PPO(), download and extraction directories wouldn't update properly.

## Version 0.0.10
* Attribute blctools.DatosCROM.dir_salida sets to which directory the reports go out to (didn't have much impact before)
* Improved automatic Servicios directory search

## Version 0.0.9
* Removed dependencies list
* Ability to download unfiltered PPOs/DTEs without specifying parks/plants list
* Incidents are no longer loaded by default on blctools.DatosCrom() objects

## Version 0.0.8
* Corrected dependencies list

## Version 0.0.6 ~ 0.0.7
* Bug fixes regarding file management
* Ability to customize filters when hitting CAMMESA's API
* PBA calculation according to IEC61400 is still functioning incorrectly

## Version 0.0.5
* Most of the code is Object Oriented now.
* CAMMESA's forecasts have been added.

## Version 0.0.2 ~ 0.0.4
Fixed the install issues

## Version 0.0.1
* Basic functionality is up and running

## TO DOs
* Prevenir que se intenten procesar archivos excel 10 segundales que no tengan datos
* Corroborar que la cantidad de grupos de columnas en los archivos 10 segundales, coincida con la cantidad de equipos del parque cuyo nombre de archivo enuncia.
* Convertir DatosCROM().parques a "nemos" automáticamente.
* Poder tomar mediciones SMEC de la BD del VC
* Mejorar los mensajes de procesamiento nivel 0, 1 y 2 en todas las funciones