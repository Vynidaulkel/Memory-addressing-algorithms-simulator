"""
- - - [ PAGINA ] - - -
Cada pagina debe tener:
  - ID
  - Direccion fisica
  - Bandera que indica si esta en memoria Real o Virtual
  - Dato extra que ocupe el algoritmo de paginacion

En la bandera de memoria:
  True = Memoria REAL
  False = Memoria Virtual

En caso de que no sea necesario almacenar explicitamente
la pagina en disco duro, y solo baste con fijarse en la bandera,
no hay necesidad de tener una variable HDD ya que no se ocupa

Si la pagina esta en memoria real, la direccion fisica coresponde
  al numero de segmento en memoria real.
Si la pagina NO esta en memoria real, la direccion fisica
  no es relevante y se puede acomodar al gusto.
"""

class Pagina:
  def __init__(self, id:int, pid, address:str, in_real:bool, time:int = 0, real:str|None=None, virtual:str|None=None, data=None) -> None:
    self.id = id
    self.pid = pid
    self.address = address 
    self.real = real # Direccion en memoria Real
    self.virtual = virtual # Direccion en memoria Virtual
    self.in_real = in_real # True = Real / False = Virtual
    self.data = data
    self.time = time # Tiempo en memoria Real
  
  def __str__(self) -> str:
    string = f'Time: {self.time} Pag: {self.id} - Direccion: {self.address}'
    if self.real:
      string += f' - RAM: {self.real}'
    elif self.virtual:
      string += f' - Vritual: {self.virtual}'
    if self.data:
      string += f' - Data: {self.data}'
    return string