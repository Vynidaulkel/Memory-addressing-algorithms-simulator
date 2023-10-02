import math
from paginas import Pagina
from algoritmos import Algoritmos
# - [ RAM ] -
RAM:int = 400

# - [PID Eliminados] -
# Agrega los pids que son eliminados
# Cuando se intenta crear una nueva peticion
# revisa esta lista 
# Si esta en la lista, no se permite hacer nada
# Si NO esta en la lista, se realiza el proceso
# pid_vistos:list = []

# - [ TABLA ] -
# Aun no tengo claro que se guarda en la tabla de simbolos
# Puede ser Key:puntero, value: lista de paginas de ese puntero
# TABLA:dict = {}

# - [DISCO DURO ] -
# Supong que las paginas guardades en disco se ven
# en forma de lista o diccionario
# HDD:list = []

# - [ MMU ] -
# La memoria real del MMU es de 100 paginas (400kb)
#MMU:int = 100
# MMU = []
# Tambien podria ser una lista con 100 elementos
# de tipo <Pagina>

# - [ PUNTERO ] -
# ptr va a ser de tipo String (str)
# Se me ocurre de nombre: "ptr-N"
# Donde N incrementa cada puntero nuevo
# O tambien se puede dejar el puntero como un numero
# que va incrementando por cada nuevo

# Capacidad MAXIMA de paginas en RAM
MAX_MMU = 100


class Puntero:
  def __init__(self, pid:int, name):
    self.pid = pid
    self.name = f'ptr-{name}'
    return self

class Proceso:
  def __init__(self, id:int) -> None:
    self.id = id
    self.ptrs = []
  
  def getPtrs(self):
    return self.ptrs
  
  def addPtr(self, ptr:Puntero):
    self.ptrs.append(ptr)


"""
- - - [ MMU ] - - -
La MMU debe realizar las siquientes funciones:
  ~new(pid, size):ptr - Solicita una memoria de tamano <size> en B y recibe
 		de vuelta la direccion del puntero logico (ptr) debera guardar 'ptr'
 		en la tabla de simbolos
  
  ~use(ptr):void - Utiliza un puntero ya definido en su tabla de simbolos
 	
  ~delete(ptr):void - Elimina un puntero de la tabla de simbolos y libera la
 	  memoria asignada
 	
  ~kill(pid):void - Libera toda la memoria asignada a este proceso.
 		Una vez que corre la instruccion KILL, no puede correr ninguna
 		instruccion mas para este proceso (pid)

La MMU debe tener un mapa de memoria que relacione cada <ptr> con
una lista de paginas. Si un ptr requiere mas de 4kb de memoria, debe
asignarle mas de una pagina

"""

class Mmu:
  def __init__(self, tipo:int):
    self.pid_vistos:list = []
    self.ptr_vistos:list = []
    self.PROCESOS:dict = {} # {PID: [puntero1, puntero2, ...]}
    self.PUNTEROS:dict = {} # {Puntero: [Pagina, Pagina2, ...]}
    self.HDD:list = [] # Lista de Paginas en Memoria Virtual
    self.MMU = [] # Lista de Paginas en Memoria Real
    self.ptrID = 0 # Contador de ID para Punteros
    self.pagID = 0 # Contador de ID para Paginas
    self.addr = 'addr-' # Address/Direccion = Puntero
    self.tipo = tipo # Determina el algoritmo que se va a usar
    self.algortimo = Algoritmos() # Clase que contiene los algoritmos
    self.tiempo_accion = 0 # Tiempo que tardo en hacer una accion
    self.tiempo_total = 0 # Tiempo acumulativo de todas las acciones
    self.tiempo_trash = 0 # Tiempo gastado en paginacion (Fallos)
    self.address_pid = {} # Tabla que relaciona un Puntero con su PID
    self.frag = 0 # Tamano de la fragmentacion interna acumulativa
    if tipo == 3:
      self.ultimo = 1
  


  def new(self, pid, size:int, uses:list=None):
    """
    Debe crear las paginas en Memoria REAL
    Y retornar un ptr resultante
    """
    # Si al PID se le ha hecho KILL
    if(type(pid) != int or pid in self.pid_vistos):
      print('Error! Ya no puedes usar este PID de nuevo!')
      return "None"
    
    # Verifica que el tamano sea un entero positivo mayor a cero
    if (type(size) != int or size <= 0):
      print(f'Error! El size debe ser un entero mayor a 0!')
      return "None"
    
    # Determina la cantidad de paginas a generar
    num_pages = math.ceil(size/4) # Por cada 4Kb de tamano, es una pagina
    if(size == 1):
      self.frag += 3
    elif(size == 2):
      self.frag += 2
    else:
      self.frag += (num_pages*4) % size

    # Verifica que la cantidad de paginas no exceda la capacidad de la MMU
    if num_pages > MAX_MMU:
      print('Error!\n La cantidad de paginas excede la memoria!')
      return "None"
    
    # Genera el Address a retornar
    address = self.addr+str(self.ptrID)

    # Lista que contiene las paginas creadas para el puntero del PID
    process_page_list = []

    # Si la MMU aun NO esta llena, agrega las paginas
    while (len(self.MMU) < MAX_MMU and num_pages > 0):
      page = Pagina(self.pagID, pid, address, True, real=address)
      if(self.tipo == 2): page.data = 1
      elif (self.tipo == 3):
        page.data = self.ultimo
        self.ultimo += 1
      process_page_list.append(page)
      self.MMU.append(page)
      self.pagID+=1
      num_pages -= 1
      self.tiempo_total += 1
      # Suma 1s al tiempo en memoria a todas las paginas en memoria RAM
      for page in self.MMU:
        page.time += 1

    # Si la MMU esta llena, hace espacio de acuerdo al algoritmo elegido
    if (len(self.MMU) >= MAX_MMU and num_pages > 0):
      # self.tiempo_accion += num_pages * 5
      # self.tiempo_trash += num_pages * 5
      # Tipos = 1: FIFO / 2: SC / 3: MRU / 4: RND
      match self.tipo:
        case 1: # Aplica FIFO
          # Hace espacio hasta que quepan todas las paginas requeridas
          while (len(self.MMU) + num_pages > MAX_MMU):
            page = Pagina(self.pagID, pid, address, True,real=address)
            self.MMU, self.HDD = self.algortimo.FIFO(self.MMU, self.HDD, page)
            process_page_list.append(page)
            self.pagID+=1
            num_pages -= 1
            self.tiempo_total += 5
            self.tiempo_trash += 5

            # Suma 5s al tiempo en memoria a todas las paginas en memoria RAM
            for page in self.MMU:
              page.time += 5

      
        case 2: # Aplica Second Chance (SC)
          while (len(self.MMU) + num_pages > MAX_MMU):
            page = Pagina(self.pagID, pid, address, True,real=address)
            self.MMU, self.HDD = self.algortimo.SC(self.MMU, self.HDD, page)
            process_page_list.append(page)
            self.pagID += 1
            num_pages -= 1
            self.tiempo_total += 5
            self.tiempo_trash += 5

            for page in self.MMU:
              page.time += 5
            
          

          
        case 3: # Aplica Most Recently Used (MRU)
          for i in range(num_pages):
            page = Pagina(self.pagID, pid, address, True,real=address)
            page.data = self.ultimo
            self.MMU, self.HDD = self.algortimo.MRU(self.MMU, self.HDD, page)
            process_page_list.append(page)
            self.pagID += 1
            self.ultimo += 1
            self.tiempo_total += 5
            self.tiempo_trash += 5
            
            # Suma 5s al tiempo en memoria a todas las paginas en memoria RAM
            for page in self.MMU:
              page.time += 5
                    


        case 4: # Aplica Random (RND)
          # Si la MMU esta llena, hace espacio de acuerdo al algoritmo elegido (SC)
          while (len(self.MMU) + num_pages > MAX_MMU):
            page = Pagina(self.pagID, pid, address, True,real=address)
            self.MMU, self.HDD = self.algortimo.RND(self.MMU, self.HDD, page)
            process_page_list.append(page)
            self.pagID += 1
            num_pages -= 1
            self.tiempo_total += 5
            self.tiempo_trash += 5
            
            # Suma 5s al tiempo en memoria a todas las paginas en memoria RAM
            for page in self.MMU:
              page.time += 5
        


        case 5:
          # Si la MMU esta llena, hace espacio de acuerdo al OPTIMO
          # Verifica si hay puntero en lista de usos
          sale = self.last_ptr(uses, address)
          if not sale:
            # Si no hay, elimina un puntero de la RAM que no se usa
            elim:str = self.no_usa(uses, address)
            self.delete(elim)
            del elim
            while (len(self.MMU) < MAX_MMU and num_pages > 0):
              page = Pagina(self.pagID, pid, address, True, real=address)
              process_page_list.append(page)
              self.MMU.append(page)
              self.pagID+=1
              num_pages -= 1
              self.tiempo_total += 1
              # Suma 1s al tiempo en memoria a todas las paginas en memoria RAM
              for page in self.MMU:
                page.time += 1

          # Hace lo normal
          while (len(self.MMU) + num_pages > MAX_MMU):
            page = Pagina(self.pagID, pid, address, True,real=address)
            sale = self.last_ptr(uses, address)
            if sale:
              self.MMU, self.HDD = self.algortimo.Optimo(self.MMU, self.HDD, page, sale)
            else:
              self.MMU, self.HDD = self.algortimo.RND(self.MMU, self.HDD, page)
            process_page_list.append(page)
            self.pagID+=1
            num_pages -= 1
            self.tiempo_total += 5
            self.tiempo_trash += 5

            # Suma 5s al tiempo en memoria a todas las paginas en memoria RAM
            for page in self.MMU:
              page.time += 5


    # Agrega el PID con la direccion a la TABLA PROCESOS
    procesos:list = self.PROCESOS.get(pid)
    # Si el PID ya esta registrado
    if(procesos):
      procesos.append(address)
      self.PROCESOS.update({pid: procesos})
    else:
      self.PROCESOS.update({pid: [address]})

    # Algrega la Direccion a la TABLA PUNTEROS
    self.PUNTEROS.update({address: process_page_list})
    self.ptrID += 1

    # Una vez guardado el procesos, se eliminan de la variable temporal
    del procesos

    self.address_pid.update({address: pid})
    # self.tiempo_total += self.tiempo_accion
    # self.tiempo_accion = 0
    # Devuele el puntero a la direccion
    return address
  



  """
  Simula utilizar el puntero, debe garantizar que las paginas correspondientes
  al ptr esten en memoria real
  
  Tal vez se haga un for recorriendo la lista de paginas verificando que todas
  esten en memoria real(memR), si no lo estan, las pasa, pero debe sacar de memR
  algunas paginas para que este puntero tenga todas sus paginas en memR
  """
  def use(self, ptr:str, uses:list=None):
    paginas:list = self.PUNTEROS.get(ptr)
    if(paginas):
      fuera:list = []
      for pagina in paginas:
        # Para el MRU se necesita saber que se ha utilizado recientemente
        if self.tipo == 3:
          pagina.data = self.ultimo
          self.ultimo += 1

        # Si esta fuera de la RAM
        if(pagina in self.HDD): 
          fuera.append(pagina)
          # self.tiempo_total += 5
          # self.tiempo_trash += 5
        
        else:
          self.tiempo_total += 1
          pagina.time += 1

      if(fuera):
        # Por cada pagina fuera, quita la direccion virtual
        # Y se la pasa a la direccion real
        for page in fuera:
          page.real = page.virtual
          page.virtual = None
          
        largo = len(fuera)
        for _ in range(largo):
          # Si hay campo en RAM, se trae las paginas
          # de disco sin problemas
          if len(self.MMU) < MAX_MMU:
            temp_page:Pagina = fuera.pop(0)
            temp_page.in_real = True
            self.MMU.append(self.HDD.pop(self.HDD.index(temp_page)))
            del temp_page
        
        # Si todas las paginas han sido traidas y aun hay campo en ram
        # O si esta justamente llena, sale con exito
        if len(self.MMU) <= MAX_MMU and len(fuera) == 0:
          return 'exito'
        
        if self.tipo == 5:
          sale = self.last_ptr(uses, ptr)
          if not sale:
            elim:str = self.no_usa(uses, ptr)
            self.delete(elim)
            del elim
            largo = len(fuera)
            for _ in range(largo):
              # Si hay campo en RAM, se trae las paginas
              # de disco sin problemas
              if len(self.MMU) < MAX_MMU:
                temp_page:Pagina = fuera.pop(0)
                temp_page.in_real = True
                self.MMU.append(self.HDD.pop(self.HDD.index(temp_page)))
                del temp_page

        # Si aun quedan paginas por traer, aplica el algoritmo
        match self.tipo:
          case 1: # FIFO
            for page in fuera:
              self.MMU, self.HDD = self.algortimo.FIFO(self.MMU, self.HDD, page)
              self.HDD.pop(self.HDD.index(page))
              self.tiempo_total += 5
              for pagina in self.MMU:
                pagina.time += 5

          
          
          case 2: # Second Chance (SC)
            for page in fuera:
              page.data = 1
              self.MMU, self.HDD = self.algortimo.SC(self.MMU, self.HDD, page)
              self.HDD.pop(self.HDD.index(page))
              self.tiempo_total += 5
              for pagina in self.MMU:
                pagina.time += 5
            
          
          
          case 3: # Most Recenttly Used (MRU)
            for page in fuera:
              self.MMU, self.HDD = self.algortimo.MRU(self.MMU, self.HDD, page)
              self.HDD.pop(self.HDD.index(page))
              self.tiempo_total += 5
              for pagina in self.MMU:
                pagina.time += 5

          
          
          case 4: # Aplica Random (RND)
            for page in fuera:
              self.MMU, self.HDD = self.algortimo.RND(self.MMU, self.HDD, page)
              self.HDD.pop(self.HDD.index(page))
              self.tiempo_total += 5
              for pagina in self.MMU:
                pagina.time += 5
          
          
          
          case 5:
            for page in fuera:
              sale = self.last_ptr(uses, ptr)
              if sale:
                self.MMU, self.HDD = self.algortimo.Optimo(self.MMU, self.HDD, page, sale)
              else:
                self.MMU, self.HDD = self.algortimo.RND(self.MMU, self.HDD, page)
              self.HDD.pop(self.HDD.index(page))
              self.tiempo_total += 5
              for pagina in self.MMU:
                pagina.time += 5
            
        
      
        # Actualiza las paginas del puntero
        paginas = self.actualizar_ptr(self.PUNTEROS[ptr], fuera)
        self.PUNTEROS[ptr] = paginas
        
    
    else:
      print('Puntero no existe')
    




  def delete(self, ptr):
    """
    Elimina todas las paginas asociadas al puntero
    Tecnicamente el puntero queda libre, pero no nos debemos preocupar por eso
    Debe aumentar el numero de paginas disponibles
    """
    # Obtiene todas las paginas asiociadas al puntero
    paginas = self.PUNTEROS.get(ptr)
    if paginas: # Si el puntero existe
      # Elimina todas las paginas asociadas al puntero
      for pagina in paginas:
        # Si esta en RAM la elimina de la RAM
        if(pagina in self.HDD): 
          temp_page = self.HDD.pop(self.HDD.index(pagina))
          del temp_page
          self.tiempo_accion += 1

        # Si esta en Disco, la elimina de DIsco
        elif(pagina in self.MMU): 
          temp_page = self.MMU.pop(self.MMU.index(pagina))
          del temp_page
          self.tiempo_accion += 1
        
        else:
          print(f'La pagina {pagina} se encuentra en el limbo!')
      
      del paginas
      # Obtiene el PID asociado al puntero
      pid = self.address_pid.get(ptr)
      # Obtiene la lista de punteros del PID
      punteros = self.PROCESOS.get(pid)
      # Saca al puntero de la lista y lo elimina
      puntero = punteros.pop(punteros.index(ptr))
      del puntero
      # Actualiza la lista de punteros del PID
      self.PROCESOS.update({pid: punteros})
      del punteros
      del pid
      del self.address_pid[ptr]
      # Elimina definitivamente el puntero de la tabla
      del self.PUNTEROS[ptr]
      self.ptr_vistos.append(ptr)

      # Actualiza el tiempo
      self.tiempo_total += self.tiempo_accion
      self.tiempo_accion = 0
      
    else:
      print(f'El puntero <{ptr}> no existe o ya ha sido eliminado!')




  def kill(self, pid):
    """
    Borra todas las paginas y punteros que pertenezcan a ese PID
    Va por la tabla de simbolos hace <del> por cada pagina del puntero
    
    Si el PID ya ha sido eliminado pero se llama otra vez a la funcion,
      deberia lanzar una Exception que diga 'PID ya ha sido eliminado'
    """
    if(pid in self.pid_vistos):
      print(f'El PID: <{pid}> no existe o ya ha sido eliminado')
    
    punteros = self.PROCESOS.get(pid)
    if punteros:
      for _ in range(len(punteros)):
        self.delete(punteros[0])
      self.pid_vistos.append(pid)
      del punteros
      del self.PROCESOS[pid]
    else:
      try:
        del self.PROCESOS[pid]
      
      except Exception:
        print(f'El PID: <{pid}> no existe o ya ha sido eliminado')


    

  def actualizar_ptr(self, paginas:list, fuera:list):
    for pagina in fuera:
      pagina.in_real = True
      paginas[paginas.index(pagina)] = pagina

    return paginas


  # - - - - - - - - - - [ RESET ] - - - - - - - - - -
  def reset_acion_time(self):
    self.tiempo_accion = 0
  
  def reset_trash_time(self):
    self.tiempo_trash = 0
  
  def reset_total_time(self):
    self.tiempo_accion = 0
  
  def reset_pointer_id(self):
    self.ptrID = 0
  
  def reset_page_id(self):
    self.pagID = 0
  
  def reset_process_used(self):
    self.pid_vistos = []
  
  def reset_pointer_used(self):
    self.ptr_vistos = []
  
  

  # - - - - - - - - - - [ GETTERS ] - - - - - - - - - -
  def get_action_time(self):
    return self.tiempo_accion
  
  def get_total_time(self):
    return self.tiempo_total
  
  def get_trash_time(self):
    return self.tiempo_trash

  def get_mmu(self):
    return self.MMU
  
  def get_hdd(self):
    return self.HDD
  
  def get_process_pointers(self):
    return self.PROCESOS
  
  def get_pointers_pages(self):
    return self.PUNTEROS
  
  def get_pointer_pid(self):
    return self.address_pid
  
  def get_fragmentation(self):
    return self.frag
  
  # - - - [ Lista de las llaves ] - - -
  def get_list_process(self):
    return list(self.PROCESOS.keys())
  
  def get_list_pointers(self):
    return list(self.PUNTEROS.keys())
  
  def get_list_pages(self):
    paginas = self.PUNTEROS.values()
    total = []
    for pagina in paginas:
      total.extend(pagina)
    return total
  
  def last_ptr(self, uses:list, current:str):
    # Falta current
    for x in uses:
      sale = 'addr-'+str(x-1)
      for paginaMMU in self.MMU:
        if paginaMMU.address == sale and sale != current:
          return sale
  
  def no_usa(self, uses:list, current:str):
    # No encontro, asi que busca el primero
    # Que no este en la lista
    for paginaMMU in self.MMU:
      ptr:str = paginaMMU.address
      pid = int(ptr.split('-')[1])+1
      if pid not in uses and ptr != current:
        print(f'Delete no usado: {pid}')
        return ptr