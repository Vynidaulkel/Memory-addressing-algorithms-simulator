import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import messagebox
import math
import time
import estructuras

vPrincipal = tk.Tk()
vPrincipal.title("Simulador")
vPrincipal.geometry("450x400+450+150")
vPrincipal.configure(bg="light blue")


#valores globales
#colores
colores=["red", "cyan",  "green", "blue", "orange", "purple", "yellow", "brown", "gray", "black", "magenta", "lime", "olive", "navy", "teal", "maroon", "gold", "light blue"]
commandList = []

#Label y command box de la semilla
labelSeed = Label(vPrincipal, text="Tiempo de espera entre comandos", font=("Arial",14),bg="light blue").place(x=30,y=50)
waitTime = tk.Entry(vPrincipal, width=15)
waitTime.place(x=320,y=50)
 
#Labels y command box de algoritmos
labelAlgoritmo = Label(vPrincipal, text="Algoritmo a simular", font=("Arial",14),bg="light blue").place(x=30,y=100)
vlist = ["FIFO", "SC", "MRU", "RND"]
algoritmo = ttk.Combobox(vPrincipal,state="readonly", values = vlist,height=800)
algoritmo.set("Ningun algoritmo")
algoritmo.pack(padx = 5, pady = 5)
algoritmo.place(x=250,y=100)


def cerrarVentanaSimulador():
    vSimulador.destroy()
    vPrincipal.deiconify()

def next(var):
    var.set(1)
def showWarning(texto):
    messagebox.showwarning("Advertencia", "La cantidad de paginas asignada en: " + texto + " excede la memoria!", parent = vSimulador)

def updateAlgoritmo(mmuAlgoritmo, ram, ProcesosCantAlgoritmo,simTimeLabelAlgo, labelRAMKBCANT, labelRamPorcentaje,
                    labelVirtualRamCant, labelVRamPorcentaje, loadedAlgoritmoCant, unloadedAlgoritmoCant,
                    trashingAlgoritmoCant, fragAlgoritmoCant, tablaAlgoritmo, mmuOptimo, ramOptimo, tablaOptimo,
                    ProcesosCantOPT, simTimeCant, labelRAMKBCANTOPT, labelRamPorcentajeOPT, labelVirtualRamCantOPT,
                    labelVRamPorcentajeOPT,loadedCant, unloadedCant, trashingCant, fragCant):
    
    """
    mmuAlgoritmo, ram2, ProcesosCantAlgoritmo,simTimeLabelAlgo,
    labelRAMKBCANT, labelRamPorcentaje, labelVirtualRamCant,
    labelVRamPorcentaje, loadedAlgoritmoCant, unloadedAlgoritmoCant, trashingAlgoritmoCant, 
    fragAlgoritmoCant, tableAlgoritmo, ram1, tableOTP,ProcesosCantOTP, simTimeCant, 
    labelRAMKBCANTOPT, labelRamPorcentajeOPT, labelVirtualRamCantOPT,
    labelVirtualRamCantOPT,loadedCant, unloadedCant, trashingCant, fragCant
    """
    #revisar que hay que quitar de la lista de punteros
    listaPunteros = []
    coloresHolder = {}
    recorridoSecuencial = []
    print(commandList)
    contador = 0
    
    useList:list = []
    for comando in commandList:
        if comando[0] == 'use' or comando[0] == 'delete':
            useList.append(comando[1])
    
    print(f'\nAntes: {useList}')
    useList.reverse()
    print(f'\nDespues: {useList}')
    
    #pid, [x(donde empieza) y y(donde termina)]
    #problema aqui, si hay fragmentacion me corta donde empieza y donde termina
    #sol que donde empieza sea una lista de todos los lugares que se le asigna a la vara  
    
    var = tk.Variable()
    #new 1 50 
    for comando in commandList:
        print(comando)
        for item in tablaAlgoritmo.get_children():
            tablaAlgoritmo.delete(item)

        for item in tablaOptimo.get_children():
            tablaOptimo.delete(item)
        var.set(0)
        if comando[0] == 'new':
            contadorDeTamanho= 0

            "sacar proceso mas ultimo"
            """
            for comando in comandoList: 
                if comando[0] = 'use':
                    utilList.append(comando[1])
            """
            """

                for comando in comandoList: 
                    comando[0] == 'new' 
                    x = mmuOptimo(comando[1], comando[2], utilList)

                    lista de utilizacion de procesos
                    [2,3]
                    [1,1,2,3,1,4,2,3]

                    mem = 4 y 2
                    vir =3 y 1

                x = ultimo proceso que se va a utilizar
                x = mmmOptimo.new(comando, tamahno, x)


            """

            x = mmuAlgoritmo.new(comando[1], comando[2])
            mmuOptimo.new(comando[1], comando[2], useList)
            if x == "None":
                showWarning(comando[0] + " (" + str(comando[1]) + "," + str(comando[2]) + ")")
            #retorna un puntero o retorna un none
            listaPunteros.append(x)

            
            #coloresholder
            # {1: rojo, 2, azul}
            
            recorridoSecuencial.append([comando[1], math.ceil(comando[2]/4)])
            #  
            #[1,5][2,5]
            #contador pinta secuencial
            if comando[1] not in coloresHolder:
                coloresHolder[comando[1]] = colores[0]
                colores.append(colores.pop(0))
            
            #{1: rojo, 2: azul}
            #[[1, 3], [1, 3], [2, 2], [2, 13]]
            
            #necesito solo los de ese proceso
            #son 8 columnas
            #primero inserta y ya si se actualiza es afuera, no se puede trabjar sobre una fila no insertada
            """for x in range(len(mmuAlgoritmo.get_list_pages())):
                tablaAlgoritmo.insert("", tk.END, values=(mmuAlgoritmo.get_list_pages()[x].id, "2", "3", "4"))"""
            # contador +=  len(mmuAlgoritmo.MMU)

        elif comando[0] == 'use':
            mmuAlgoritmo.use(listaPunteros[comando[1]-1])
            mmuOptimo.use(listaPunteros[comando[1]-1], useList)
            useList.pop(-1)
        #actualizamos ram

        #ambas quitamos de la ram 
        #cuando eliminamos de la ram sacamos proceso de colorsholder y lo metemos otra vez en colores 
        elif comando[0] == 'delete':

            mmuAlgoritmo.delete(listaPunteros[comando[1]-1])
            mmuOptimo.delete(listaPunteros[comando[1]-1])
            useList.pop(-1)

            """for x in range(len(mmuAlgoritmo.get_list_pages())):
                fila = tablaAlgoritmo.get_children()[x]
                #if mmuAlgoritmo[x].MMU[x] in 
                tablaAlgoritmo.delete(fila)"""
            


        elif comando[0] == 'kill':
            mmuAlgoritmo.kill(comando[1])
            mmuOptimo.kill(comando[1])

            print("kill = " + str(len(mmuAlgoritmo.PROCESOS)))
        

        #pintamos ram
        for x in range(len(mmuAlgoritmo.MMU)):
            pag = mmuAlgoritmo.MMU[x]
            pid = pag.pid
            color = coloresHolder[pid]
            ram[x].config(bg= color)
            ram[x].update()

        for x in range(len(mmuAlgoritmo.MMU), 100):
            ram[x].config(bg= 'light grey')
            ram[x].update() 

    

        #treeview 2
        for page in mmuAlgoritmo.get_list_pages():
            loaded = ''
            real = ''
            virtual = ''
            data = ''
            if page.in_real: loaded = 'x'
            if page.real: real = page.real
            if page.virtual: virtual = page.virtual
            if page.data: data = str(page.data)
            color = coloresHolder[page.pid]
            tablaAlgoritmo.insert("", tk.END, tag=color, values=(page.id, page.pid, loaded, page.address, real, virtual, page.time, data))
            # fila = tablaAlgoritmo.get_children()[x]
            # if mmuAlgoritmo[x].MMU[x] in 
            # tablaAlgoritmo.item(fila, values= (mmuAlgoritmo.get_list_pages()[x].id,mmuAlgoritmo.get_list_pages()[x].pid,3,4,5,6,7,8))


        #pintamos labels
        ProcesosCantAlgoritmo.config(text = len(mmuAlgoritmo.PROCESOS))
        ProcesosCantAlgoritmo.update()

        simTimeLabelAlgo.config(text= mmuAlgoritmo.tiempo_total)
        simTimeLabelAlgo.update()

        labelRAMKBCANT.config(text = len(mmuAlgoritmo.MMU)* 4)
        labelRAMKBCANT.update()
        
        labelRamPorcentaje.config(text=((len(mmuAlgoritmo.MMU)* 4)/400)*100 )
        labelRamPorcentaje.update()

        labelVirtualRamCant.config(text=((len(mmuAlgoritmo.HDD)*4)))
        labelVirtualRamCant.update()

        labelVRamPorcentaje.config(text=((len(mmuAlgoritmo.HDD)* 4)/400)*100)
        labelVRamPorcentaje.update()

        loadedAlgoritmoCant.config(text= (len(mmuAlgoritmo.MMU)))
        loadedAlgoritmoCant.update()

        unloadedAlgoritmoCant.config(text= (len(mmuAlgoritmo.HDD)))
        unloadedAlgoritmoCant.update()

        trashingAlgoritmoCant.config(text= mmuAlgoritmo.get_trash_time())
        if mmuAlgoritmo.get_trash_time() > mmuAlgoritmo.tiempo_total * 0.5:
            trashingAlgoritmoCant.config(bg= 'red')
        else:
            trashingAlgoritmoCant.config(bg= 'light grey')
        trashingAlgoritmoCant.update()

        fragAlgoritmoCant.config(text= mmuAlgoritmo.get_fragmentation())
        fragAlgoritmoCant.update()

       

        
        #labels para el optimo-------------------------------------

        #pintamos ram

        #hay que cambiar mmuAlgoritmo.mmu al optimo

        #ram
        for x in range(len(mmuOptimo.MMU)):
            pag = mmuOptimo.MMU[x]
            pid = pag.pid
            color = coloresHolder[pid]
            ramOptimo[x].config(bg= color)
            ramOptimo[x].update()

        for x in range(len(mmuOptimo.MMU), 100):
            ramOptimo[x].config(bg= 'light grey')
            ramOptimo[x].update() 


        #treeview 1
        for page in mmuOptimo.get_list_pages():
            loaded = ''
            real = ''
            virtual = ''
            data = ''
            if page.in_real: loaded = 'x'
            if page.real: real = page.real
            if page.virtual: virtual = page.virtual
            if page.data: data = str(page.data)
            color = coloresHolder[page.pid]
            tablaOptimo.insert("", tk.END, tag=color, values=(page.id, page.pid, loaded, page.address, real, virtual, page.time, data))
            # fila = tablaAlgoritmo.get_children()[x]
            # if mmuAlgoritmo[x].MMU[x] in 
            # tablaAlgoritmo.item(fila, values= (mmuAlgoritmo.get_list_pages()[x].id,mmuAlgoritmo.get_list_pages()[x].pid,3,4,5,6,7,8))



        ProcesosCantOPT.config(text = len(mmuOptimo.PROCESOS))
        ProcesosCantOPT.update()

        simTimeCant.config(text= mmuOptimo.tiempo_total)
        simTimeCant.update()

        labelRAMKBCANTOPT.config(text = len(mmuOptimo.MMU)* 4)
        labelRAMKBCANTOPT.update()

        labelRamPorcentajeOPT.config(text=((len(mmuOptimo.MMU)* 4)/400)*100 )
        labelRamPorcentajeOPT.update()

        labelVirtualRamCantOPT.config(text=((len(mmuOptimo.HDD)*4)))
        labelVirtualRamCantOPT.update()

        labelVRamPorcentajeOPT.config(text=((len(mmuOptimo.HDD)* 4)/400)*100)
        labelVRamPorcentajeOPT.update()

        loadedCant.config(text= (len(mmuOptimo.MMU)))
        loadedCant.update()

        unloadedCant.config(text= (len(mmuOptimo.HDD)))
        unloadedCant.update()


        trashingCant.config(text= mmuOptimo.get_trash_time())
        if mmuOptimo.get_trash_time() > mmuOptimo.tiempo_total * 0.5:
            trashingCant.config(bg= 'red') 
        else:
            trashingCant.config(bg= 'light grey')
        trashingCant.update()

        fragCant.config(text= mmuOptimo.get_fragmentation())
        fragCant.update()

        reanudar = tk.Button(vSimulador,text="next", command=lambda : next(var) )
        reanudar.place(x=550, y=610)

        vSimulador.wait_variable(var)
        #time.sleep(float(waitTime.get()))

    
        
    messagebox.showwarning("Atencion", "La simulacion ha terminado", parent = vSimulador)

   
    """ print(commandList)
        cont =1
        for celda in lista:
            if cont < 20:
                celda.config(bg=colores[4])
            elif cont >= 20 and cont <40:
                celda.config(bg=colores[11])
            cont+=1
    """
#ocultar ventana principal y crea ventana simulador
def crearVentanaSimulador(commandList):
    print(waitTime.get())
    global vSimulador
    vSimulador= tk.Toplevel()
    vSimulador.title("Simulador")
    vSimulador.geometry("1100x650+100+30")#tamahno y posicion de la pantalla
    vSimulador.configure(bg="light blue")
 

    
    #ram graficas
    ram1=[]
    ram2=[]
    #ram1
    x = Label(vSimulador, text= "RAM OTP", padx=471).place(x=51, y=10)
    
    for i in range(0,100):
        cell = Label(vSimulador, width=1, height=1, bd=1, relief='solid')
        cell.place(x=51+(10*i), y=30)
        ram1.append(cell)


    #ram2 

    x2 = Label(vSimulador, text= "RAM ALGORITMO ESCOGIDO", padx=410).place(x=51, y=70)
    
    for i in range(0,100):
        cell = Label(vSimulador, width=1, height=1, bd=1, relief='solid')
        cell.place(x=51+(10*i), y=90)
        ram2.append(cell)



    #tabla 1
    MMUTitle = Label(vSimulador, text= "MMU OPT", padx=230,bd=1, relief='solid').place(x=15, y=127)
    columnas = ('Page ID','PID', 'LOADED',"L-ADDR", "M-ADDR", "D-ADDR", "LOADED-T", "MARK")
    tableOTP = ttk.Treeview(vSimulador, columns = columnas, show= 'headings')
    tableOTP.place(x=15, y=150, width= 525)
    tableOTP.heading(columnas[0], text = 'Page ID')
    tableOTP.heading(columnas[1], text = 'PID')
    tableOTP.heading(columnas[2], text = 'LOADED')
    tableOTP.heading(columnas[3], text = 'L-ADDR')
    tableOTP.heading(columnas[4], text = 'M-ADDR')
    tableOTP.heading(columnas[5], text = 'D-ADDR')
    tableOTP.heading(columnas[6], text = 'LOADED-T')
    tableOTP.heading(columnas[7], text = 'MARK')


    for col in columnas:
        if col == "PID":
            tableOTP.column(col, width=35, minwidth=10, anchor=tk.CENTER)  
        elif col == "MARK" :
            tableOTP.column(col, width=47, minwidth=10, anchor=tk.CENTER) 
        elif col=="LOADED-T":
            tableOTP.column(col, width=72, minwidth=10, anchor=tk.CENTER)  
        else:
            tableOTP.column(col, width=62, minwidth=10, anchor=tk.CENTER)    
     # Insertar datos en el Treeview2
    """tableOTP.insert("", tk.END, values=("1", "2", "3", "4", "3", "4","holis"))
    tableOTP.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableOTP.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableOTP.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "16"))
    tableOTP.insert("", tk.END, text="Fila 1", values=("1", "2", "3", "4"))
    tableOTP.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableOTP.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableOTP.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "16"))
    tableOTP.insert("", tk.END, text="Fila 1", values=("1", "2", "3", "4"))
    tableOTP.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableOTP.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableOTP.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "a")) """


    #tabla 2
    MMUTitle2 = Label(vSimulador, text= "MMU Algoritmo Escogido", padx=181,bd=1, relief='solid').place(x=560, y=127)
    tableAlgoritmo = ttk.Treeview(vSimulador, columns = columnas, show= 'headings')
    tableAlgoritmo.place(x=560, y=150, width= 525)
    tableAlgoritmo.heading(columnas[0], text = 'Page ID')
    tableAlgoritmo.heading(columnas[1], text = 'PID')
    tableAlgoritmo.heading(columnas[2], text = 'LOADED')
    tableAlgoritmo.heading(columnas[3], text = 'L-ADDR')
    tableAlgoritmo.heading(columnas[4], text = 'M-ADDR')
    tableAlgoritmo.heading(columnas[5], text = 'D-ADDR')
    tableAlgoritmo.heading(columnas[6], text = 'LOADED-T')
    tableAlgoritmo.heading(columnas[7], text = 'MARK')

    # Agregar colores a las filas
    for color in colores:
        tableAlgoritmo.tag_configure(color, background=color)
        tableOTP.tag_configure(color, background=color)

    for col in columnas:
            if col == "PID":
                tableAlgoritmo.column(col, width=35, minwidth=10, anchor=tk.CENTER)  
            elif col == "MARK" :
                tableAlgoritmo.column(col, width=47, minwidth=10, anchor=tk.CENTER) 
            elif col=="LOADED-T":
                tableAlgoritmo.column(col, width=72, minwidth=10, anchor=tk.CENTER)  
            else:
                tableAlgoritmo.column(col, width=62, minwidth=10, anchor=tk.CENTER)    
    
 
    """# Insertar datos en el Treeview2
    tableAlgoritmo.insert("", tk.END, text="Fila 1", values=("1", "2", "3", "4"))
    tableAlgoritmo.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableAlgoritmo.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableAlgoritmo.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "16"))
    tableAlgoritmo.insert("", tk.END, text="Fila 1", values=("1", "2", "3", "4"))
    tableAlgoritmo.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableAlgoritmo.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableAlgoritmo.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "16"))
    tableAlgoritmo.insert("", tk.END, text="Fila 1", values=("1", "2", "3", "4"))
    tableAlgoritmo.insert("", tk.END, text="Fila 2", values=("5", "6", "7", "8"))
    tableAlgoritmo.insert("", tk.END, text="Fila 3", values=("9", "10", "11", "12"))
    tableAlgoritmo.insert("", tk.END, text="Fila 4", values=("13", "14", "15", "16"))"""
    

    #PROCESOS Y SIM TIME--------------------------------------
    #OTP
    #cuadro de procesos
    cantProcesos = 0
    ProcesosTitleOTP = Label(vSimulador, text= "Procesos", width = 31, relief='solid').place(x=30, y=400)
    ProcesosCantOTP = Label(vSimulador, text = cantProcesos, width = 31, relief='solid')
    ProcesosCantOTP.place(x=30, y=423)

    #cuadro de sim time 
    simTimeOTP = 0
    simTimeLabel = Label(vSimulador, text= "SIM-TIME",  width = 31, relief='solid').place(x=282, y=400)
    simTimeCant = Label(vSimulador, text = simTimeOTP,  width = 31, relief='solid')
    simTimeCant.place(x=282, y=423)

    #ALGORITHM
    #cuadro de procesos
    cantProcesosAlgo = 0
    ProcesosTitleAlgo = Label(vSimulador, text= "Procesos", width = 31, relief='solid').place(x=572, y=400)
    ProcesosCantAlgoritmo = Label(vSimulador, text = cantProcesosAlgo, width = 31, relief='solid')
    ProcesosCantAlgoritmo.place(x=572, y=423)
    
    #cuadro de sim time 
    simTimeAlgo = 0
    simTimeLabelAlgoritmo = Label(vSimulador, text= "SIM-TIME ALGORITMO", width = 31, relief='solid').place(x=823, y=400)
    simTimeLabelAlgo = Label(vSimulador, text = simTimeAlgo, width = 31, relief='solid')
    simTimeLabelAlgo.place(x=823, y=423)

    
    #RAM TABLE ------------------------------------------------------


    #RAM FOR OPTIMAL
    ramKB = 400
    labelRAMKB = Label(vSimulador, text= "RAM KB", width = 15, relief='solid').place(x=30, y=460)
    labelRAMKBCANTOPT = Label(vSimulador, text = 0,  width = 15, relief='solid')
    labelRAMKBCANTOPT.place(x=30, y=483)

    labelRamPorcentaje= Label(vSimulador, text= "RAM %", width = 15, relief='solid').place(x=154, y=460)
    labelRamPorcentajeOPT = Label(vSimulador, text = 0, width = 15, relief='solid')
    labelRamPorcentajeOPT.place(x=154, y=483)

    #virtual ram
    labelVirtualRam = Label(vSimulador, text= "V-RAM KB", width = 15, relief='solid').place(x=282, y=460)
    labelVirtualRamCantOPT = Label(vSimulador, text = 0,  width = 15, relief='solid')
    labelVirtualRamCantOPT.place(x=282, y=483)

    labelVRamKB= Label(vSimulador, text= "V-RAM %", width = 15, relief='solid').place(x=406, y=460)
    labelVRamPorcentajeOPT = Label(vSimulador, text = 0, width = 15, relief='solid')
    labelVRamPorcentajeOPT.place(x=406, y=483)

    #RAM FOR ALGORITHM

    labelRAMKB = Label(vSimulador, text= "RAM KB", width = 15, relief='solid').place(x=572, y=460)
    labelRAMKBCANT = Label(vSimulador, text = 0,  width = 15, relief='solid')
    labelRAMKBCANT.place(x=572, y=483)

    labelRamPorcentaje1= Label(vSimulador, text= "RAM %", width = 15, relief='solid').place(x=694, y=460)
    labelRamPorcentaje = Label(vSimulador, text = 0, width = 15, relief='solid')
    labelRamPorcentaje.place(x=694, y=483)

    #virtual ram
    labelVirtualRam = Label(vSimulador, text= "V-RAM KB", width = 15, relief='solid').place(x=823, y=460)
    labelVirtualRamCant = Label(vSimulador, text = 0,  width = 15, relief='solid')
    labelVirtualRamCant.place(x=823, y=483)

    labelVRamKB= Label(vSimulador, text= "V-RAM %", width = 15, relief='solid').place(x=947, y=460)
    labelVRamPorcentaje = Label(vSimulador, text = 0, width = 15, relief='solid')
    labelVRamPorcentaje.place(x=947, y=483)
    #PAGES-----------------------------------------------------------------------------------------------

    #OPTIMO

    #PAGINAS
    Pages = Label(vSimulador, text= "Pages", width = 31, relief='solid').place(x=30, y=520)
    loadedLabel = Label(vSimulador, text= "Loaded", width = 15, relief='solid').place(x=30, y=543)
    unloadedLabel =Label(vSimulador, text= "Unloaded", width = 15, relief='solid').place(x=154, y=543)

    loaded = 0
    unloaded = 0
    loadedCant = Label(vSimulador, text= loaded, width = 15, relief='solid')
    loadedCant.place(x=30, y=566)
    unloadedCant = Label(vSimulador, text= unloaded, width = 15, relief='solid')
    unloadedCant.place(x=154, y=566)

    #trashing
    trashingLabel = Label(vSimulador, text= "Thrasing", width = 15, relief='solid').place(x=282, y=520)
    trashing = 0 
    trashingCant = Label(vSimulador, text= trashing, width = 15, relief='solid', height = 2)
    trashingCant.place(x=282, y=543)

    #fragmentacion
    fragLabel = Label(vSimulador, text= "Fragmentacion", width = 15, relief='solid').place(x=406, y=520)
    fragmentacion = 0
    fragCant= Label(vSimulador, text= fragmentacion, width = 15, relief='solid', height = 2)
    fragCant.place(x=406, y=543)


    #ALGORITHM

    #PAGINAS
    PagesAlgoritmo = Label(vSimulador, text= "Pages", width = 31, relief='solid').place(x=572, y=520)
    loadedAlgortimoLabel = Label(vSimulador, text= "Loaded", width = 15, relief='solid').place(x=572, y=543)
    unloadedAlgoritmoLabel =Label(vSimulador, text= "Unloaded", width = 15, relief='solid').place(x=694, y=543)

    loadedAlgoritmo = 0
    unloadedAlgoritmo = 0
    loadedAlgoritmoCant = Label(vSimulador, text= loadedAlgoritmo, width = 15, relief='solid')
    loadedAlgoritmoCant.place(x=572, y=566)
    unloadedAlgoritmoCant = Label(vSimulador, text= unloadedAlgoritmo, width = 15, relief='solid')
    unloadedAlgoritmoCant.place(x=694, y=566)

    #trashing
    trashingAlgoritmoLabel = Label(vSimulador, text= "Thrasing", width = 15, relief='solid').place(x=823, y=520)
    trashingAlgoritmo = 0 
    trashingAlgoritmoCant = Label(vSimulador, text= trashingAlgoritmo, width = 15, relief='solid', height = 2)
    trashingAlgoritmoCant.place(x=823, y=543)

    #fragmentacion
    fragAlgoritmoLabel = Label(vSimulador, text= "Fragmentacion", width = 15, relief='solid').place(x=947, y=520)
    fragmentacionAlgoritmo = 0
    fragAlgoritmoCant= Label(vSimulador, text= fragmentacionAlgoritmo, width = 15, relief='solid', height = 2)
    fragAlgoritmoCant.place(x=947, y=543)
    

    




    
    

    #cerramos ventana principal
    
    vPrincipal.withdraw()
    vSimulador.update()
    vSimulador.deiconify()
    
    #creamos optimo

    mmuOptimo  = estructuras.Mmu(5)
    #empezamos a hacer el mmu del algoritmo escogido
    if algoritmo.get() == "FIFO":
        mmuAlgoritmo = estructuras.Mmu(1)
    elif algoritmo.get() == "SC":
        mmuAlgoritmo = estructuras.Mmu(2)
    elif algoritmo.get() == "MRU":
        mmuAlgoritmo = estructuras.Mmu(3)
    elif algoritmo.get() == "RND":
        mmuAlgoritmo = estructuras.Mmu(4)
    #delete solo para puntero
    test = "new(1,200)"
    
    """for pagina in mmuAlgoritmo.MMU:
        print(pagina.data)
"""
    #mark if none dejamos vacio, else 1 
    #tira en cantidad de paginas, convertimos a 1 celdas por pag

    #loaded and unloaded len mmu or hdd
    #trashing todavia no esta para get
    #
    #print(mmuAlgoritmo.get_total_time())

    #
    #print(mmuAlgoritmo.tiempo_total)
    #mmuOTP


    cerrarSimulador = tk.Button(vSimulador, text="volver", command=cerrarVentanaSimulador, font=("Arial",10)).place(x=1000, y=610)
    next = tk.Button(vSimulador,text= "start", command=lambda : updateAlgoritmo(mmuAlgoritmo, ram2, ProcesosCantAlgoritmo,simTimeLabelAlgo,
                                                                               labelRAMKBCANT, labelRamPorcentaje, labelVirtualRamCant,
                                                                               labelVRamPorcentaje, loadedAlgoritmoCant, unloadedAlgoritmoCant, trashingAlgoritmoCant, 
                                                                               fragAlgoritmoCant, tableAlgoritmo, mmuOptimo,ram1, tableOTP,ProcesosCantOTP, simTimeCant, labelRAMKBCANTOPT, labelRamPorcentajeOPT,
                    labelVirtualRamCantOPT, labelVRamPorcentajeOPT, loadedCant, unloadedCant, trashingCant, fragCant)).place(x=490, y=610)
    #reanudar = tk.Button(vSimulador,text="    ", command=lambda : update(ram2)).place(x=550, y=610)
#Abrir archivo
def open_file():
    file_path = filedialog.askopenfilename()
    
    with open(file_path, 'r') as archivo:
        contenido = archivo.readlines()
    for linea in contenido:
        partes = linea.split("(")
        instruccion = partes[0]
        valores = partes[1].strip(")\n").split(",")
        valores = [int(num.strip("")) for num in valores]        
        sublist = [instruccion] + valores
        commandList.append(sublist)

    crearVentanaSimulador(commandList)

abrirArchivo = tk.Button(vPrincipal, text="Escoger y simular archivo", command=open_file, font=("Arial",10)).place(x=127, y=150)



#Label y entry box de la cantidad de procesos a simular
labelProcesos = Label(vPrincipal, text="Procesos a simular", font=("Arial",14), bg="light blue").place(x=30,y=200)

pCant = [10,50,100]
procesos = ttk.Combobox(vPrincipal,state="readonly", values = pCant,height=800)
procesos.set("Random")
procesos.pack(padx = 5, pady = 5)
procesos.place(x=250,y=200)


#Label y entry box de la cantidad de las operaciones a simular
labelOperaciones = Label(vPrincipal, text="Cantidad de operaciones", font=("Arial",14), bg="light blue").place(x=30,y=250)
oCant = [500,1000,5000]
operaciones = ttk.Combobox(vPrincipal,state="readonly", values = oCant,height=800)
operaciones.set("Random")
operaciones.pack(padx = 5, pady = 5)
operaciones.place(x=250,y=250)

simularSinArchivo = tk.Button(vPrincipal, text="Simular sin archivo",font=("Arial",10),
 command= crearVentanaSimulador).place(x=150, y=310)




vPrincipal.mainloop()