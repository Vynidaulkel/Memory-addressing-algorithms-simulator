from paginas import Pagina
import random

class Algoritmos:
  
  # First In, First Out
  def FIFO(self, MMU:list, HDD:list, pagina:Pagina):
    index = 0
    temp_page:Pagina = MMU[index]
    while(temp_page.address == pagina.address):
      index += 1
      temp_page = MMU[index]

    temp_page = MMU.pop(index)
    temp_page.virtual = temp_page.real
    temp_page.real = None
    temp_page.in_real = False
    temp_page.tiempo = 0
    HDD.append(temp_page)
    MMU.append(pagina)
    del index
    del temp_page
    return MMU, HDD



  # Second Chance
  def SC(self, MMU:list, HDD:list, pagina:Pagina):
    # Cuando se crea la pagina, el espacio de <Data> ahora va a tener el valor de 1
    # El algoritmo ve la data de la pagina 
    # Si esta en 0, lo saca de la RAM y lo mete a memoria virtual
    index = 0
    temp_page:Pagina = MMU[index]
    while(temp_page.address == pagina.address):
      index += 1
      temp_page = MMU[index]
    
    # Si esta en 0, lo saca de la MMU y lo mete al HDD
    if temp_page.data == 0:
      temp_page:Pagina = MMU.pop(index)
      temp_page.virtual = temp_page.real
      temp_page.real = None
      temp_page.in_real = False
      temp_page.tiempo = 0
      HDD.append(temp_page)
      pagina.data = 1
      MMU.append(pagina)
      del index
      del temp_page
      return MMU, HDD
    
    # Si esta en 1, lo mueve al final de la cola y cambia su data a 0
    else:
      temp_page:Pagina = MMU.pop(index)
      temp_page.data = 0
      MMU.append(temp_page)
      del temp_page
      # En principio, hace este proceso hasta que la pagina tenga data = 0
      return self.SC(MMU, HDD, pagina)
    # Cuando pasa de Virtual a RAM, vuelve a ponerse el data en 1



  # Most Recently Used (Como FIFO, pero es LIFO)
  def MRU(self, MMU:list, HDD:list, pagina:Pagina):
    alto = 0 # Mas alto = mas reciente
    index = 0
    # Recorre la RAM en busca del mas usado
    # El valor DATA de la pagina guarda el usado mas reciente
    # Por lo que el DATA mas alto, es el mas recientemente usado
    for i in range(len(MMU)):
      # Verifica que la pagina actual tenga un valor mas alto que el ultimo usado
      # Verifica que la pagina pertenezca a un puntero diferente
      if(MMU[i].data >= alto and MMU[i].address != pagina.address):
        alto = MMU[i].data
        index = i
    
    # Para este puntro deberia de haber encontrado la pagina mas recientemente usada
    # Y que pertenezca a un puntero diferente
    temp_page:Pagina = MMU.pop(index)
    temp_page.virtual = temp_page.real
    temp_page.real = None
    temp_page.in_real = False
    temp_page.tiempo = 0
    MMU.append(pagina)
    HDD.append(temp_page)
    del alto
    del index
    del temp_page
    return MMU, HDD
    
    

  # Random 
  def RND(self, MMU:list, HDD:list, pagina:Pagina):
    # Selecciona una pagina al azar de la MMU
    mem_len = len(MMU)-1 
    rand_page = random.randint(0,mem_len)
    temp_page:Pagina = MMU[rand_page]
    
    # Si la pagina seleccionada es del mismo proceso
    # Que la pagina a insertar, selecciona una nueva
    while(temp_page.address == pagina.address):
      rand_page = random.randint(0,mem_len)
      temp_page = MMU[rand_page]
    
    # Si la pagina selecciona ya es de un proceso diferente
    # La saca de la MMU y la guarda en HDD, luego inserta
    # La pagina nueva en la MMU al final
    temp_page = MMU.pop(rand_page)
    temp_page.virtual = temp_page.real
    temp_page.real = None
    temp_page.in_real = False
    temp_page.tiempo = 0
    HDD.append(temp_page)
    MMU.append(pagina)
    del temp_page
    del rand_page
    
    return MMU, HDD


  # Optimo
  def Optimo(self, MMU:list, HDD:list, pagina:Pagina, sale:str):
    index = 0
    temp_page:Pagina = MMU[index]
    while(temp_page.address != sale):
      index += 1
      temp_page = MMU[index]

    temp_page = MMU.pop(index)
    temp_page.virtual = temp_page.real
    temp_page.real = None
    temp_page.in_real = False
    temp_page.time = 0
    HDD.append(temp_page)
    MMU.append(pagina)
    del index
    del temp_page
    return MMU, HDD