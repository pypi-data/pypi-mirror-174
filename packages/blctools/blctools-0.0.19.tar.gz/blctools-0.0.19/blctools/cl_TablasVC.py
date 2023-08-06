from . import dirs
from . import fechas

import gc
import pickle
import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path

from .cl_SQLConnector import *

__all__ = ['TablasVC',]

class TablasVC(SQLConnector):
    
    def __init__(
        self,
        cargar_incidencias = False,
        cargar_datos_basicos = 'offline',
        parques = [],
        clientes = [],
        solo_CROM = False,
        mensajes=True,
        ):

        super().__init__()

        self.dfs = {}
        self._idsApiCammesa = {}
        self._ucs = []
        self._nemos = []
        self.__parques = parques
        self.__clientes = clientes
        self.solo_CROM = solo_CROM
        
        self.incidencias_todas_auditoria = None
        self.incidencias_todas = None
        self.central = None
        self.origen = None
        self.empresas = None
        self.centralesempresas = None
        self.razones = None
        self.estado = None
        self.tipoequipo = None
        self.tipogenerador = None
        self.conjuntogeneradores = None
        self.habilitaciones = None
        self.tipohabilitaciones = None
        
        self._idApiC_a_nemo = {}
        self._nemo_a_uc = {}
        self._nemo_a_idApiC = {}
        self._nemo_a_owner = {}
        self._uc_a_nemo = {}
        self._uc_a_owner = {}
        self._uc_a_idApiC = {}
        
        self._empresas_bop = None
        self._empresas_gen = None
        self._empresas_grid = None
        
        self._iec61400 = None
        self._iec61400_metodos = ['IEC',] # Antiguamente: ['IEC','WTG','BOP','GRID']
        self.__procesar_norma_iec_61400()

        ruta = dirs.get_dc_cfg()
        nombre_tablas = 'Tablas_VC_Offline.xlsx'
        nombre_incidencias = 'Incidencias_VC_Offline.pickle'
        self.__archivo_tablas = Path(ruta + '\\' + nombre_tablas)
        self.__archivo_incidencias = Path(ruta + '\\' + nombre_incidencias)

        self.consultar(
            datos_basicos=cargar_datos_basicos,
            incidencias=cargar_incidencias,
            mensajes=mensajes
            )

        # Evaluar cómo incluir las curvas de potencia a este objeto, para tenerlas a mano para DatosCROM()

    #
    # Propiedades. Getters y Setters
    #
    @property
    def parques(self):
        return self.__parques
    
    @parques.setter
    def parques(self,val):
        self.__check_cliente_parque(val,tipo='parques')
        if val != []:
            self.clientes = []
    
        self.__parques = val
    
    @property
    def clientes(self):
        return self.__clientes
    
    @clientes.setter
    def clientes(self,val):
        self.__check_cliente_parque(val,tipo='clientes')
        if val != []:
            self.parques = []
        
        self.__clientes = val
    
    @property
    def idsApiCammesa(self):
        if self._idsApiCammesa == {}:
            if self.checkear_conexion():
                self.__consultar_datos_basicos(mensajes=True,desconectar=True)

        return self._idsApiCammesa
    
    @property
    def ucs(self):
        if self._ucs == []:
            if self.checkear_conexion():
                self.__consultar_datos_basicos(mensajes=True,desconectar=True)

        return self._ucs
    
    @property
    def nemos(self):
        if self._nemos == []:
            if self.checkear_conexion():
                self.__consultar_datos_basicos(mensajes=True,desconectar=True)
            
        return self._nemos
    
    @idsApiCammesa.setter
    def idsApiCammesa(self,val):
        if not isinstance(val,dict):
            raise TypeError('Las IDs de la Api de CAMMESA deben ingresarse como un diccionario {Unidadcomercial : ID}')
        
        self._idsApiCammesa = val
        
    @ucs.setter
    def ucs(self,val):
        if not isinstance(val,(list,set,tuple)):
            raise TypeError('Las unidades comerciales deben listarse en una lista, tupla o set')
        
        self._ucs = list(val)
                
    @nemos.setter
    def nemos(self,val):
        if not isinstance(val,(list,set,tuple)):
            raise TypeError('Los Mnemotécnicos de CAMMESA deben listarse en una lista, tupla o set')
        
        self._nemos = list(val)

    @property
    def dir_salida(self):
        return self._dir_salida

    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_salida = dirs.check_dir(val)    

    @property
    def solo_CROM(self):
        return self._solo_CROM
    
    @solo_CROM.setter
    def solo_CROM(self,val):
        if isinstance(val,bool):
            self._solo_CROM = val
        else:
            raise TypeError('solo_CROM puede tomar sólo valores booleanos: True/False')

    #
    # Chequeo de parámetros de entrada de otras funciones
    #
    def __check_params_carga(self,param,val):
        # Chequea si los parámetros de carga "cargar_incidencias" o "cargar_datos_básicos" 
        # tienen parámetros válidos
        
        valores_posibles_bool = [False, True]
        valores_posibles_str = ['online','offline'] 
        valores_posibles = valores_posibles_str + valores_posibles_bool
        
        if not isinstance(val,(bool,str)):
            raise TypeError(f'El parámetro {param} = {val} debe ser del tipo bool/str y se recibió {type(val)}')
        elif isinstance(val,bool):
            # No hay que trasformar el valor de ninguna manera, ya que es booleano
            pass
        else:
            #Sólo queda la opción posible de que el valor del parámetro sea del tipo string
            val = val.lower()
            if not val in valores_posibles_str:
                raise ValueError(f'El parámetro {param} = {val} debe estar entre {valores_posibles_str}')

        return val
            
    def __check_cliente_parque(self,val,tipo='parques'):
        if isinstance(val,(list,set,tuple)):
            str_filter = lambda x: isinstance(x,str)
            results = map(str_filter,val)
            if all(results):
                #Acá se podría agregar un chequeo de que los clientes/parques estén en la lista del CROM, en caso de estar conectado.
                return True
            else:
                raise TypeError(f'Todos los valores dentro de la lista "{tipo}" deben ser del tipo string.')
        else:
            raise TypeError(f'Se esperaba una lista, set o tuple para la variable "{val}".')

    def __check_nemo(self,nemo_parque):
        
        if not isinstance(nemo_parque,str):
            raise TypeError('El Nemotécnico debe ser del tipo String')
        elif not nemo_parque:
            raise ValueError('El nemo del parque no puede estar vacío')
        elif not nemo_parque.upper() in self.nemos:
            raise ValueError(f'El nemotécnico {nemo_parque} no se encuentre entre:\n{self.nemos}')
        else:
            return nemo_parque.upper()

    def __check_uc(self,uc):
        
        if not isinstance(uc,str):
            raise TypeError('El Nemotécnico debe ser del tipo String')
        elif not uc:
            raise ValueError('El nemo del parque no puede estar vacío')
        elif not uc.upper() in self.ucs:
            raise ValueError(f'El nemotécnico {uc} no se encuentre entre:\n{self.ucs}')
        else:
            return uc.upper()

    def __check_params_nemo_uc(self,nemo_parque='',uc=''):
        if nemo_parque != '' and uc != '':
            raise ValueError('No se puede seleccionar un Nemotécnico y una Unidad Comercial a la vez')
        
        elif nemo_parque == '' and uc == '':
            raise ValueError('Debe ingresar un valor para nemo_parque parque o para uc')
        elif nemo_parque !='' and uc== '':
            nemo_parque = self.__check_nemo(nemo_parque)
            return ('Nemo',nemo_parque)
        else:
            uc = self.__check_uc(uc)
            return ('UC',nemo_parque)

    def __check_filtro(self,filtro):
        if not isinstance(filtro,str):
            raise TypeError('El parámetro filtro debe ser del tipo string')
        elif not filtro.lower() in ['nemo','uc']:
            raise ValueError('El parámetro filtro debe ser "nemo" o "uc"')
        else:
            if filtro.lower() == 'nemo':
                filtro = 'Nemo'
            else:
                filtro = 'UC'
        
        return filtro

    #
    # Funciones para consultar tablas internas específicas rápidamente
    #
    def _crear_dict(self,df,llave,valor):
        
        llaves = df[llave].to_list()
        valores = df[valor].to_list()
        
        return dict(zip(llaves,valores))
 
    def __crear_dict_tipo_empresa(self):
        flt_bop = ~self.empresas['mantenimientoBOP'].isna()
        flt_gen = ~self.empresas['generador'].isna() 
        flt_opL = ~self.empresas['operacionLocal'].isna()
        flt_mantL = ~self.empresas['mantenimientoparque'].isna() 
        flt_traspo = ~self.empresas['transportista'].isna()
        flt_distro = ~self.empresas['distribuidora'].isna()
        flt_adm = ~self.empresas['administracion'].isna()
        
        self._empresas_bop = self.empresas.loc[flt_bop,'Empresa'].to_list()
        self._empresas_gen = self.empresas.loc[flt_gen | flt_opL | flt_mantL,'Empresa'].to_list()
        self._empresas_grid = self.empresas.loc[flt_traspo | flt_distro | flt_adm,'Empresa'].to_list()
        
        self._empresas_gen = {x:'GENERATOR' for x in self._empresas_gen}
        self._empresas_bop = {x:'BOP_CONTRACTOR' for x in self._empresas_bop}
        self._empresas_grid = {x:'GRID_OPERATOR' for x in self._empresas_grid}
    
    def __obtener_equipos_parque(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        filtro = self.__check_filtro(filtro)
                
        agrupamientos = self.conjuntogeneradores\
                            .query(f'{filtro} == "{valor}"')\
                            .loc[:,'Agrupamiento']\
                            .sort_values()\
                            .unique()
        
        generadores = self.__obtener_equipos_parque_no_agr(filtro,valor)
        
        return ['PLANT',] + list(agrupamientos) + list(generadores)

    def __obtener_equipos_parque_no_agr(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        filtro = self.__check_filtro(filtro)
            
        generadores = self.conjuntogeneradores\
                            .query(f'{filtro} == "{valor}"')\
                            .loc[:,'equipo']\
                            .sort_values()\
                            .unique()
        
        if len(generadores) == 0:
            generadores = self.tipoequipo\
                            .query(f'{filtro} == "{valor}" & equipo != "PLANT"')\
                            .loc[:,'equipo']\
                            .sort_values()\
                            .unique()
        
        return list(generadores)
            
    def __obtener_equipos_agrupamiento(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        filtro = self.__check_filtro(filtro)
                
        df = self.conjuntogeneradores.query(f'{filtro} == "{valor}"') 
        agrupamientos =  df['Agrupamiento'].unique()
        lista_equipos = lambda x : df.query(f'Agrupamiento == "{x}"')['equipo'].to_list()
        
        return {agrupamiento:lista_equipos(agrupamiento) for agrupamiento in agrupamientos}

    def __obtener_agrupamientos_parque(self,filtro,valor):
        filtro = self.__check_filtro(filtro)
        df = self.conjuntogeneradores.query(f'{filtro} == "{valor}"') 
        agrupamientos =  list(df['Agrupamiento'].unique())
        
        return agrupamientos

    def __obtener_cod(self,filtro,valor):
        filtro = self.__check_filtro(filtro)
        cod = self.habilitaciones\
            .query(f'{filtro} == "{valor}" & tipo == "PPA"')\
            .sort_values(by='fecha',ascending=False)\
            .loc[:,'fecha']\
            .array[0]       #Obtiene el primer valor explícitamente
        return cod

    def __obtener_año_op(self,filtro,valor,fecha):
        
        fecha_cod = self.__obtener_cod(filtro,valor)
        return fechas.año_op(fecha_cod=fecha_cod,fecha_actual=fecha)

    #
    # Procesamiento de incidencias
    #
    def __procesar_norma_iec_61400(self):
    
        try:
            self._iec61400 = pd.read_excel(dirs.get_dc_cfg() + '\\IEC61400.xlsx')
        except:
            self._iec61400 =  pd.read_excel(dirs.raiz + '\\IEC61400.xlsx')
            
        cols = [f'Priority_{x}' for x in self._iec61400_metodos]
        maximo = self._iec61400.loc[:,cols].values.max()
        numeros = [x for x in range(maximo,0,-1)]
        cat = pd.CategoricalDtype(numeros,ordered=True)
        self._iec61400.loc[:,cols] = self._iec61400.loc[:,cols].astype(cat)
    
    def __procesar_incidencias_it1(self,mensajes=False):
        
        #Crear el dataframe de incidencias y la estructura que tendrá hasta el final
        df_tipoequipo = self.tipoequipo\
                            .loc[:,['idtipoEquipo','id_central','equipo','idTipoGenerador','Pnom']]
                            
        df = pd\
                            .merge(
                                left=self.incidencias_todas,
                                right=df_tipoequipo,
                                left_on=['id_tipoEquipo','id_central'],
                                right_on=['idtipoEquipo','id_central'],
                                how='left')\
                            .drop(columns=['id_tipoEquipo','idtipoEquipo'])
                            
        mapeo_owner = self._crear_dict(self.centralesempresas,'idCentral','generador')
        mapeo_origen = self._crear_dict(self.origen,'idorigen','origen')
        mapeo_origen2 = {'Interno':'INT','Externo':'EXT','--':'NA'}
        mapeo_empresas = self._crear_dict(self.empresas,'id','Empresa')
        mapeo_razones = self._crear_dict(self.razones,'idrazones','razones')
        mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
        mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
        mapeo_estado = self._crear_dict(self.estado,'idestado','estado')
        mapeo_tipogenerador = self._crear_dict(self.tipogenerador,'id','nombre')
        
        
        mapeo_razones2= {
            'MAPRO':'MAPRO',
            'MAPRO (no computa)':'MAPRO S_A',
            'Mantenimiento no programado':'MANOPRO',
            'Falla':'FAILURE',
            'Limitación':'LIMITATION',
            'Reactivo Nocturno':'QNIGHT',
            'Suspensdido':'SUSPENDED',
            'Fuerza mayor':'FORCE MAJEURE'
            }
        
        df['UC'] = df['id_central'].map(mapeo_ucs)
        df['Nemo'] = df['id_central'].map(mapeo_nemos)
        df['idTipoGenerador'] = df['idTipoGenerador'].map(mapeo_tipogenerador)
        df['id_trabajo'] = df['id_trabajo'].map(mapeo_empresas)
        df['id_central'] = df['id_central'].map(mapeo_owner)
        df['id_razones'] = df['id_razones'].map(mapeo_razones).map(mapeo_razones2)
        df['id_origen'] = df['id_origen'].map(mapeo_origen).map(mapeo_origen2)
        df['id_estado'] = df['id_estado'].map(mapeo_estado)
        df['SolverAgent'] = np.nan
        df['numero_pt11'] = df['numero_pt11'].replace(to_replace=-1,value=0)
    
        #Renombrar columnas
        cols_renombrar = {
            'idincidencia':'ID',
            'idPrimario':'ID_prim',
            'idLimitacion':'ID_lim',
            
            'id_estado':'Status',
            'UC':'UC',
            'Nemo':'Nemo',
            'id_central':'Owner',
            'cantEquipos':'QtyTot',
            
            'evStFecha':'Start',
            'evStUser':'StartUsr',
            'evStPotCor':'PowerCut',

            'cuNoFecha':'NoticeDate',
            
            'evEndFecha':'End',
            'evEndUser':'EndUsr',
            'evEndPot':'PowerRet',
            
            'id_pt11':'PT11',
            'numero_pt11':'ID_PT11',
            
            'equipo':'Equipo',
            'Pnom':'Pnom',
            'idTipoGenerador':'GenType',
            'afCantEquipos':'Qty',
            'afQuantity':'QtyProp',
            
            'afTime':'Hours',
            'energyLoss':'ENS',
            'id_trabajo':'SolvedBy',
            'SolverAgent':'SolverAgent',
            'id_razones':'Reason',
            'id_origen':'Origin',
            'codFalla':'Code',

            'pot_posible':'Pteo',
            'setpoint_pot':'SP_P',

            'descripcion':'BLC_Description',
            'comentario':'BLC_Comments',
            
            'descripcionFalla':'Owner_Description',
            'equipoAfectado':'Owner_AffectedEquipment',
            'accionesTomadas':'Owner_ActionsTaken',
            'resultados':'Owner_Results',
            'proximosPasos':'Owner_NextSteps',
            'comentariosCliente':'Owner_Comments',
        }


        self.incidencias_todas = df\
                                    .rename(columns=cols_renombrar)\
                                    .copy(deep=True)
 
    def __procesar_incidencias_it2(self,mensajes=False):
        #Integridad de Datos

        df = self.incidencias_todas
        
        #Rellenar huecos, que se dan naturalmente
        descartadas = ~df['descartadoFecha'].isna()
        falta_SolvedBy = df['SolvedBy'].isna()
        falta_EndUsr = df['EndUsr'].isna()
        
        falta_Origin = (df['Origin'] == 'NA') | (df['Origin'].isna()) | ((df['Origin'] != 'INT') & (df['Origin'] != 'EXT'))
        falta_Reason = (df['Reason'] == 'NA') | (df['Reason'].isna())
        flt_no_descartada = df['Status'] != 'DESCARTADA'
        
        #Para aquellas incidencias descartadas, se coloca como usuario que cerró, el usuario que descartó.
        df.loc[descartadas & falta_EndUsr,'EndUsr'] = df.loc[descartadas & falta_EndUsr,'lastModifUser']
        
        #Las no descartadas deberían ser incidencias abiertas, por cómo funciona el sistema
        df.loc[~descartadas & falta_EndUsr,'EndUsr'] = 'corte_automático'
        df.loc[~descartadas & falta_EndUsr,'End'] = dt.datetime.now().replace(second=0,microsecond=0)
        
        #Hay un único caso en el que falta el campo SolvedBy, de una incidencia muy vieja.
        #Se deja esto aquí para no hardcodear soluciones.
        df.loc[falta_SolvedBy,'SolvedBy'] = df.loc[falta_SolvedBy,'Owner']
        
        #Rellenar huecos de 'Origin' y 'Reason'
        df.loc[flt_no_descartada & falta_Origin,'Origin'] = 'INT'   # Los huecos y valores extraños se asumen internos
        df.loc[flt_no_descartada & falta_Reason,'Reason'] = np.nan  # EL hueco se llena más adelante

        #Recalcular el SolverAgent, ya que se llenaron los huecos
        self.__crear_dict_tipo_empresa()
        mapeo_solveragent = self._empresas_bop | self._empresas_gen | self._empresas_grid
        
        df['SolverAgent'] = df['SolvedBy'].map(mapeo_solveragent)
        falta_SolverAgent = df['SolverAgent'].isna()
        
        df.loc[falta_SolverAgent,'SolverAgent'] = 'INVALIDO'
        
        for col in ['Equipo','GenType','Reason']:
            df[col] = df[col].fillna('DESCONOCIDO')
            
        self.incidencias_todas = df.copy(deep=True)

    def __procesar_incidencias_it3(self,mensajes=False):
        
        df = self.incidencias_todas
        
        #Cambiar tipos de datos para ahorrar memoria
        cols_ui16 = ['PT11','ID_PT11','QtyTot','Qty']
        cols_ui32 = ['ID','ID_prim','ID_lim',]
        cols_cat = [
            'Status',
            'UC',
            'Nemo',
            'Owner',
            'StartUsr',
            'EndUsr',
            'Equipo',
            'GenType',
            'SolvedBy',
            'SolverAgent',
            'Reason',
            'Origin',
            'Code'
            ]

        for col in cols_ui16:
            if mensajes: print(f'Convirtiendo {col} a UI16')
            df[col] = df[col].astype('UInt16')
            
        for col in cols_ui32:
            if mensajes: print(f'Convirtiendo {col} a UI32')
            df[col] = df[col].astype('UInt32')

        for col in cols_cat:
            try:
                df.loc[:,col] = df.loc[:,col].str.upper()
                valores = df[col].unique()
                categoria = pd.CategoricalDtype(valores,ordered=False)
                df.loc[:,col] = df[col].astype(categoria)
            except:
                if mensajes: print(f'Procesando Incidencias CROM: Imposible convertir {col} a categoría...')
        
        cols_produccion = [
            'ID',
            'ID_prim',
            'ID_lim',
            
            'Status',
            'UC',
            'Nemo',
            'Owner',
            'QtyTot',
            
            'Start',
            'StartUsr',
            'PowerCut',

            'NoticeDate',
            
            'End',
            'EndUsr',
            'PowerRet',
            
            'PT11',
            'ID_PT11',
            
            'Equipo',
            'Pnom',
            'GenType',
            'Qty',
            'QtyProp',
            
            'Hours',
            'ENS',
            'SolvedBy',
            'SolverAgent',
            'Reason',
            'Origin',
            'Code',

            'Pteo',
            'SP_P',

            'BLC_Description',
            'BLC_Comments',
            
            'Owner_Description',
            'Owner_AffectedEquipment',
            'Owner_ActionsTaken',
            'Owner_Results',
            'Owner_NextSteps',
            'Owner_Comments',
        ]

        cols_auditoria = [ 
            'sinCuNo',
            'abiertoFecha',
            'cerrIncFecha',
            'cerrComFecha',
            'visadoFecha',
            'descartadoFecha',
            'justificacionDescarte',

            'lastModifUser',
            'lastModifFecha',
            'lastModifUserWeb',
            'lastModifFechaWeb',
            'comentarioEdicion',

            'resaltar',
        ]
        
        self.incidencias_todas_auditoria = df.loc[:,cols_produccion+cols_auditoria].copy(deep=True)
        flt_no_descartada = df['Status'] != 'DESCARTADA'
        self.incidencias_todas = df.loc[flt_no_descartada,cols_produccion].copy(deep=True)

    def __procesar_incidencias_it4(self,mensajes=False):
        #Incorporar columnas de la norma IEC61400
        cols_todas = self.incidencias_todas.columns.to_list()
        
        #Con este bloque de código, permitimos reprocesar infinitamente el mismo dataframe, para incorporarle las prioridades IEC
        if 'IEC_lvl1' in cols_todas:
            cols_iec = self.incidencias_todas.loc[:,'IEC_lvl1':].columns.to_list()
            cols_resto = [c for c in cols_todas if not c in cols_iec]
            self.incidencias_todas = self.incidencias_todas.loc[:,cols_resto].copy(deep=True)

        self.incidencias_todas = self.incidencias_todas.merge(
                            right=self._iec61400,
                            on=['Origin','Reason','SolverAgent'],
                            how='left'
                            )

    def __combinar_incidencias_locales_y_online(self,mensajes=False):
        # Intenta concatenar incidencias leídas de la BD con las incidencias que se encontraran offline.
        # en caso de duplicados se queda con las más nuevas
        if not self.__archivo_incidencias.exists():
            return
            
        
        with open(self.__archivo_incidencias, "rb") as r:
            dict_dfs = pickle.load(r)
        
        df_short_new = self.incidencias_todas
        df_long_new = self.incidencias_todas_auditoria
        
        df_short_old = dict_dfs['incidencias_todas']
        df_long_old = dict_dfs['incidencias_todas_auditoria']
        
        if mensajes: print(f"Concatenando incidencias offline con las recientemente leídas.")
        df_short_merged = pd.concat([df_short_new,df_short_old],ignore_index=True)
        df_long_merged = pd.concat([df_long_new,df_long_old],ignore_index=True)
        
        if mensajes: print(f"Eliminando duplicados...")
        subset= ['ID',]
        df_short_merged.drop_duplicates(subset=subset,ignore_index=True,inplace=True)
        df_long_merged.drop_duplicates(subset=subset,ignore_index=True,inplace=True)
        
        if mensajes: print(f"Reordenando...")
        df_short_merged.sort_values(by=subset,ascending=[True for _ in subset],inplace=True)
        df_long_merged.sort_values(by=subset,ascending=[True for _ in subset],inplace=True)
        
        if mensajes: print(f"Asignando resultados.")
        self.incidencias_todas = df_short_merged.copy(deep=True)
        self.incidencias_todas_auditoria = df_long_merged.copy(deep=True)
        
        if mensajes: print(f"Guardando copia local del resultado.")
        self.__crear_backup_de_las_tablas(datos_basicos=False,incidencias=True,mensajes=mensajes)

        del df_short_new,df_short_old,df_long_new,df_long_old,df_short_merged,df_long_merged,dict_dfs
        gc.collect()

    #
    # Funciones, más complejas, privadas y auxiliares, de 
    # consulta y manipulación de datos 
    #
    def __asignar_datos_incidencias(self,mensajes=False):
        self.incidencias_todas = self.dfs['incidencias']
        
        #Crear el DataFrame que contendrá todas las incidencias y renombrar columnas
        self.__procesar_incidencias_it1(mensajes=mensajes)  #Renombrar columnas
        self.__procesar_incidencias_it2(mensajes=mensajes)  #Validación de datos
        self.__procesar_incidencias_it3(mensajes=mensajes)  #Optimización de consumo de memoria
        self.__procesar_incidencias_it4(mensajes=mensajes)  #Procesar incidencias bajo IEC61400
        
    def __asignar_datos_central(self,mensajes=False):
        self.central = self.dfs['central']
        self.central['idApiCammesa'] = self.central['idApiCammesa'].astype('Int64')

    def __asignar_datos_origen(self,mensajes=False):
        self.origen = self.dfs['origen']
    
    def __asignar_datos_habilitaciones(self,mensajes=False):
            self.habilitaciones = self.dfs['habilitaciones']
            
            mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
            mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
            mapeo_tipohab = self._crear_dict(self.tipohabilitaciones,'id','nombre')
            
            self.habilitaciones['UC'] = self.habilitaciones['id_central'].map(mapeo_ucs)
            self.habilitaciones['Nemo'] = self.habilitaciones['id_central'].map(mapeo_nemos)
            self.habilitaciones['tipo'] = self.habilitaciones['tipo'].map(mapeo_tipohab)
    
    def __asignar_datos_tipohabilitaciones(self,mensajes=False):
        self.tipohabilitaciones = self.dfs['tipohabilitaciones']
    
    def __asignar_datos_empresas(self,mensajes=False):
        self.empresas = self.dfs['empresas']\
                            .rename(columns={'nombre':'Empresa'})\
                            .applymap(lambda x : np.nan if x == 0 else x)
    
    def __asignar_datos_centralesempresas(self,mensajes=False):
        self.centralesempresas = self.dfs['centralesempresas']
        mapeo = self._crear_dict(self.empresas,'id','Empresa')
    
        for col in self.centralesempresas.columns[1:]:
            self.centralesempresas[col] = self.centralesempresas[col].map(mapeo)
    
    def __asignar_datos_razones(self,mensajes=False):
        self.razones = self.dfs['razones']
    
    def __asignar_datos_estado(self,mensajes=False):
        self.estado = self.dfs['estado']
    
    def __asignar_datos_tipoequipo(self,mensajes=False):
        self.tipoequipo = self.dfs['tipoequipo']\
                            .rename(columns={'nombre':'equipo','potencia':'Pnom'})
                            
        flt_tiene_fabricante =  ~self.tipoequipo.fabricante.isna()
        pot_inst_ct = self.tipoequipo[flt_tiene_fabricante].groupby('id_central',as_index=False)['Pnom'].sum()
        pot_inst_ct['idtipoEquipo'] = 0
        pot_inst_ct['idTipoGenerador'] = 0
        pot_inst_ct['equipo'] = 'PLANT'
        self.tipoequipo = pd.concat([self.tipoequipo,pot_inst_ct],ignore_index=True)
        
        
        mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
        mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
        self.tipoequipo['UC'] = self.tipoequipo['id_central'].map(mapeo_ucs)
        self.tipoequipo['Nemo'] = self.tipoequipo['id_central'].map(mapeo_nemos)
        self.tipoequipo['equipo'] = self.tipoequipo['equipo'].str.upper()
    
    def __asignar_datos_tipogenerador(self,mensajes=False):
            self.tipogenerador = self.dfs['tipogenerador']
            
            data = {
                'id':[0],
                'nombre':['Planta Completa'],
                'agrupamiento':[np.nan]
                }
            df_tmp = pd.DataFrame(data)

            self.tipogenerador = pd.concat([self.tipogenerador,df_tmp],ignore_index=True)
    
    def __asignar_datos_conjuntogeneradores(self,mensajes=False):
        self.conjuntogeneradores = pd.merge(left=self.dfs['conjuntogeneradores'],right=self.tipoequipo,left_on='idGenerador',right_on='idtipoEquipo',suffixes=('_or',''))\
            .drop(columns=['idGenerador','idtipoEquipo','cantidad'])\
            .rename(columns={
                'idTipoGenerador_or':'Agrupamiento',
                'idTipoGenerador':'GenType'
            }
        )
                            
        mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
        mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
        mapeo_equipos = self._crear_dict(self.tipoequipo,'idtipoEquipo','equipo')
        mapeo_tipogenerador = self._crear_dict(self.tipogenerador,'id','nombre')
        
        self.conjuntogeneradores['UC'] = self.conjuntogeneradores['id_central'].map(mapeo_ucs)
        self.conjuntogeneradores['Nemo'] = self.conjuntogeneradores['id_central'].map(mapeo_nemos)
        self.conjuntogeneradores['GenType'] = self.conjuntogeneradores['GenType'].map(mapeo_tipogenerador)
        self.conjuntogeneradores['Agrupamiento'] = self.conjuntogeneradores['Agrupamiento'].map(mapeo_equipos)
        
        self.conjuntogeneradores.drop(columns=['id_central'],inplace=True)
        
        self.conjuntogeneradores['Agrupamiento'] = self.conjuntogeneradores['Agrupamiento'].str.upper()
        self.conjuntogeneradores['equipo'] = self.conjuntogeneradores['equipo'].str.upper()
   
    def __asignar_datos(self,tabla,mensajes=False):
        if tabla == 'central':
            self.__asignar_datos_central(mensajes=mensajes)
            
        elif tabla == 'origen':
            self.__asignar_datos_origen(mensajes=mensajes)
        
        elif tabla == 'habilitaciones':
            self.__asignar_datos_habilitaciones(mensajes=mensajes)

        elif tabla == 'tipohabilitaciones':
            self.__asignar_datos_tipohabilitaciones(mensajes=mensajes)
            
        elif tabla == 'empresas':
            self.__asignar_datos_empresas(mensajes=mensajes)

        elif tabla == 'centralesempresas':
            self.__asignar_datos_centralesempresas(mensajes=mensajes)
            
        elif tabla == 'razones':
            self.__asignar_datos_razones(mensajes=mensajes)
            
        elif tabla == 'estado':
            self.__asignar_datos_estado(mensajes=mensajes)
            
        elif tabla == 'tipoequipo':
            self.__asignar_datos_tipoequipo(mensajes=mensajes)
            
        elif tabla == 'tipogenerador':
            self.__asignar_datos_tipogenerador(mensajes=mensajes)
            
        elif tabla == 'conjuntogeneradores':
            self.__asignar_datos_conjuntogeneradores(mensajes=mensajes)
            
        elif tabla == 'incidencias':
            self.__asignar_datos_incidencias(mensajes=mensajes)
        else:
            pass

    def __consultar(self,tablas,mensajes=False,desconectar=True,query=None):
        if not isinstance(tablas,(list,tuple,set)):
            raise Exception('El listado de tablas debe ser del tipo lista, tupla o set')
        
        elif len(tablas) == 0:
            raise Exception('Debe ingresar al menos una tabla en la lista de tablas')
        
        if self.checkear_conexion(mensajes=mensajes):
            
            if query is None:
                SQL_A_DF = lambda t: pd.read_sql(f'SELECT * FROM {t}',self.conexion)
            else:
                SQL_A_DF = lambda t: pd.read_sql(query,self.conexion)

            for tabla in tablas:
                if mensajes: print(f'Consultando {tabla}')
                self.dfs[tabla] = SQL_A_DF(tabla)
                self.__asignar_datos(tabla,mensajes=mensajes)


        else:
            raise Exception('Imposible conectarse a la Base de Datos del CROM')

        if desconectar:
            self.desconectar(mensajes=mensajes)
     
    def __consultar_datos_basicos(self,mensajes=False,desconectar=True):  
        
        tablas = [
            'central',
            'origen',
            'empresas',
            'centralesempresas',
            'razones',
            'estado',
            'tipoequipo',
            'tipogenerador',
            'conjuntogeneradores',
            'tipohabilitaciones',
            'habilitaciones',
        ]
        
        self.__consultar(tablas,mensajes=mensajes,desconectar=False)

        if self.checkear_conexion(mensajes=mensajes):
            self.consultar_idsApiCammesa()
            self.consultar_ucs(solo_CROM=self.solo_CROM)
            self.consultar_nemoCammesa(solo_CROM=self.solo_CROM)
        
        if desconectar:
            self.desconectar(mensajes=mensajes)

    def __consultar_incidencias(self,
                                mensajes=False,
                                query=None,
                                fecha_i=fechas.restar_mes(fechas.mes_ant_dia_1()),
                                fecha_f=fechas.ayer().replace(hour=23,minute=59,second=59),
                                desconectar=True
                                ):
        
        # Valida la fecha de inicio
        if not fecha_i is None:
            fecha_i = fechas.validar_fecha(fecha_i)
        
        # Valida la fecha de inicio
        if not fecha_f is None:
            fecha_f = fechas.validar_fecha(fecha_f)
        
        # Valida que si se colocaron ambas fechas, la más antigua sea la fecha de inicio
        if fecha_i and fecha_f:
            fecha_i,fecha_f = fechas.validar_fechas(fecha_ini = fecha_i, fecha_fin = fecha_f)
            
        if query is None:
            query = f"SELECT * FROM incidencias WHERE evStFecha <= '{fecha_f}' AND evEndFecha >= '{fecha_i}'"
        
        if mensajes: (f"Consultando incidencias:")
        if mensajes: (f"Query: {query}")
        
        self.__consultar(
            tablas=['incidencias',],
            query=query,
            mensajes=mensajes,
            desconectar=desconectar
        )

        self.__combinar_incidencias_locales_y_online(mensajes=mensajes)

    def __crear_backup_de_las_tablas(self,datos_basicos=True,incidencias=True,mensajes=False):

        hay_incidencias = not self.incidencias_todas is None
        
        if datos_basicos:
            if mensajes: print(f"Guardando backup local de los datos básicos en {self.__archivo_tablas}")
            
            with pd.ExcelWriter(self.__archivo_tablas) as w:
                self.central.to_excel(w,sheet_name='central',index=False)
                self.origen.to_excel(w,sheet_name='origen',index=False)
                self.empresas.to_excel(w,sheet_name='empresas',index=False)
                self.centralesempresas.to_excel(w,sheet_name='centralesempresas',index=False)
                self.razones.to_excel(w,sheet_name='razones',index=False)
                self.estado.to_excel(w,sheet_name='estado',index=False)
                self.tipoequipo.to_excel(w,sheet_name='tipoequipo',index=False)
                self.tipogenerador.to_excel(w,sheet_name='tipogenerador',index=False)
                self.conjuntogeneradores.to_excel(w,sheet_name='conjuntogeneradores',index=False)
                self.habilitaciones.to_excel(w,sheet_name='habilitaciones',index=False)
                self.tipohabilitaciones.to_excel(w,sheet_name='tipohabilitaciones',index=False)
            
        if incidencias and hay_incidencias:
            if mensajes: print(f"Guardando backup local de las incidencias en {self.__archivo_incidencias}")
            dict_inc = {
                'incidencias_todas' : self.incidencias_todas.copy(deep=True),
                'incidencias_todas_auditoria' : self.incidencias_todas_auditoria.copy(deep=True)
            }
            
            if self.__archivo_incidencias.exists():
                # Eliminar archivo de tablas existente
                pass
            
            with open(self.__archivo_incidencias, 'wb') as w:
                pickle.dump(dict_inc,w)
    
    def __leer_ultimo_backup_de_las_tablas(self,cargar_datos_basicos=True,cargar_incidencias=False,mensajes=False):
        
        if cargar_datos_basicos:
            if self.__archivo_tablas.exists():
                if mensajes: print(f"Cargando datos básicos en modo offline desde {self.__archivo_tablas}")
                dict_dfs = pd.read_excel(self.__archivo_tablas,sheet_name=None)
                
                self.central = dict_dfs['central']
                self.origen = dict_dfs['origen']
                self.empresas = dict_dfs['empresas']
                self.centralesempresas = dict_dfs['centralesempresas']
                self.razones = dict_dfs['razones']
                self.estado = dict_dfs['estado']
                self.tipoequipo = dict_dfs['tipoequipo']
                self.tipogenerador = dict_dfs['tipogenerador']
                self.conjuntogeneradores = dict_dfs['conjuntogeneradores']
                self.habilitaciones = dict_dfs['habilitaciones']
                self.tipohabilitaciones = dict_dfs['tipohabilitaciones']
                
                self.consultar_idsApiCammesa()
                self.consultar_ucs(solo_CROM=self.solo_CROM)
                self.consultar_nemoCammesa(solo_CROM=self.solo_CROM)
                
            else:
                print(f"No se encontró un archivo con los datos básicos offline {self.__archivo_tablas}")
        
        if cargar_incidencias:
            if self.__archivo_incidencias.exists():
                if mensajes: print(f"Cargando incidencias en modo offline desde {self.__archivo_incidencias}")
                with open(self.__archivo_incidencias, "rb") as r:
                    dict_dfs = pickle.load(r)
                self.incidencias_todas = dict_dfs['incidencias_todas']
                self.incidencias_todas_auditoria = dict_dfs['incidencias_todas_auditoria']
            else:
                print(f"No se encontró un archivo con los datos de incidencias offline {self.__archivo_incidencias}")
   
    #
    # Funciones visibles al usuario, de consulta de datos
    #
    def consultar_idsApiCammesa(self):
        flt = self.central['idApiCammesa'] > 0
        self.idsApiCammesa =  self.central\
                                    .loc[flt,['unidadComercial','idApiCammesa']]\
                                    .set_index('unidadComercial')\
                                    .to_dict('dict')['idApiCammesa']  

    def consultar_ucs(self,solo_CROM=False):
        if solo_CROM:
            flt_sc = self.central['opcCROM'].isna()
            self.ucs = self.central.loc[~flt_sc,'unidadComercial'].to_list()
        else:
            self.ucs = self.central.loc[:,'unidadComercial'].to_list()

    def consultar_nemoCammesa(self,solo_CROM=False):
        flt = self.central['nemoCammesa'].str.len() > 0     
        
        if solo_CROM:
            flt_sc = self.central['opcCROM'].isna()
            self.nemos = self.central\
                    .loc[flt & ~flt_sc,'nemoCammesa']\
                    .to_list()
        else:
            self.nemos = self.central\
                                .loc[flt,'nemoCammesa']\
                                .to_list()

    def consultar_equipos(self,nemo_parque='',uc='',potencia=False):

        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)

        if potencia:
            df = self.tipoequipo.query(f'{filtro} == "{valor}"')
            return self._crear_dict(df,'equipo','Pnom')
        else:
            return self.__obtener_equipos_parque(filtro=filtro,valor=valor)
     
    def consultar_equipos_por_agrupamiento(self,nemo_parque='',uc=''):

        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_equipos_agrupamiento(filtro=filtro,valor=valor)
    
    def consultar_agrupamientos(self,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_agrupamientos_parque(filtro=filtro,valor=valor)

    def consultar_equipos_no_agrupamientos(self,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_equipos_parque_no_agr(filtro=filtro,valor=valor)

    def consultar_cod(self,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_cod(filtro=filtro,valor=valor)

    def consultar_año_op(self,fecha,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_año_op(filtro=filtro,valor=valor,fecha=fecha)

    def consultar(self,
                  datos_basicos=False,
                  incidencias=False,
                  fecha_i=fechas.restar_mes(fechas.mes_ant_dia_1()),
                  fecha_f=fechas.ayer().replace(hour=23,minute=59,second=59),
                  mensajes=False
                  ):

        # Chequear parámetros de entrada
        datos_basicos = self.__check_params_carga(param='datos_basicos',val=datos_basicos)
        incidencias = self.__check_params_carga(param='incidencias',val=incidencias)
        
        # "on" significa modo online (consultar directamente a la base de datos del CROM)
        # "off" significa modo offline (Cargar de archivos guardados en la nube del sharepoint)
        inc_on = (incidencias == 'online') or (incidencias== True)
        inc_off = (incidencias == 'offline')

        db_on = (datos_basicos == 'online')
        db_off = (datos_basicos == 'offline') or (datos_basicos == True) or (inc_on and not db_on)

        #Consultas directas a la BD del CROM
        if db_on: 
            #Desconectar significa, desconectar el objeto conector SQL luego de realizar la consulta de dátos básicos
            # Si, además, se pretenden consultar las incidencias, lo más educado (y eficiente) es no desconectar y luego reconectar enseguida
            self.__consultar_datos_basicos(mensajes = mensajes, desconectar = not inc_on)
            self.__crear_backup_de_las_tablas(datos_basicos=True,incidencias=False)
        
        # Lecturas offline directas
        self.__leer_ultimo_backup_de_las_tablas(
            cargar_datos_basicos=db_off,
            cargar_incidencias=inc_off,
            mensajes=mensajes
            )

        if inc_on: 
            self.__consultar_incidencias(mensajes=mensajes,fecha_i=fecha_i,fecha_f=fecha_f)
            self.__crear_backup_de_las_tablas(datos_basicos=False,incidencias=True)