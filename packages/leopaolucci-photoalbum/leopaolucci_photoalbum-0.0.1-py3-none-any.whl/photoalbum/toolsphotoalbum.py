import tkinter as tk

from tkinter.messagebox import askyesno
from tkinter import filedialog

    
# Function to open a file in the system
def open_dir(tit,lng):
   pathdir = filedialog.askdirectory(title=tit)
   return(pathdir)
   

def number_of_layout(nf):
     
    num_layout = 0 
    nlin = 0
    ncol = 0
      
    try:
    
        numero_de_fotos = nf
        
        if (numero_de_fotos == 1):
        
            num_layout = 1
            nlin = 1
            ncol = 1
        
        elif ( (numero_de_fotos > 1) & (numero_de_fotos <= 4) ):
        
            num_layout = 2
            nlin = 2
            ncol = 2
        
        elif ( (numero_de_fotos > 4) & (numero_de_fotos <= 6) ):
        
            num_layout = 3  
            nlin = 2
            ncol = 3
        
        elif ( (numero_de_fotos > 6) & (numero_de_fotos <= 8) ):
        
            num_layout = 4  
            nlin = 2
            ncol = 4
        
        elif ( numero_de_fotos == 9):
            
            num_layout = 5
            nlin = 3
            ncol = 3
        
        elif ( (numero_de_fotos > 9) & (numero_de_fotos <= 12) ):
        
            num_layout = 6  
            nlin = 3
            ncol = 4
        
        elif ( (numero_de_fotos > 12) & (numero_de_fotos <= 16) ):
        
            num_layout = 7  
            nlin = 4
            ncol = 4
        
        elif ( (numero_de_fotos > 17) & (numero_de_fotos <= 20) ):
        
            num_layout = 8 
            nlin = 4
            ncol = 5
        
    finally: 
        print("O melhor layout terá ", nlin ,"linha(s) e ",ncol, "coluna(s)!")    
        return({"numero_layout":num_layout,
            "linhas":nlin,
            "colunas":ncol})
 
def photos_per_page():

    nf = 0
    while True:
        try:
            
            nf = input("Entre com o número de fotos em cada pagina (número inteiro positivo) ou ZERO para ENCERRAR !!:")
            nf = int(nf)
        
        except ValueError:
            print("Valor invalido!!!")
            print("Valor deve ser número inteiro positivo!!!")
            continue
        else:
            print(f'Voce entrou : {nf}')
            if (nf > 20):
                print("Número de fotos por página muito grande (valor máximo = 20)!!!")
                continue
            elif(nf < 0):
                print("Valor invalido!!!")
                print("Valor deve ser número inteiro positivo!!")    
                continue
            elif(nf == 0):
                print("Encerrando ...!")
                return(nf)
            else:
                print("Album terá ", nf ,"fotos por página(s)!")
                break
    return(nf)    

def number_of_pages():
    np = 0
    while True:
        try:
            
            np = input("Entre com o número de páginas do album (número inteiro positivo) ou ZERO para ENCERRAR !!:")
            np = int(np)
        
        except ValueError:
            print("Valor invalido!!!")
            print("Valor deve ser número inteiro positivo!!!")
            continue
        else:
            print(f'Voce entrou : {np}')
            if (np > 50):
                print("Número de páginas muito grande (valor máximo = 50)!!!") 
                continue
            elif(np < 0):
                print("Valor invalido!!!")
                print("Valor deve ser número inteiro positivo!!")    
                continue
            elif(np == 0):
                print("Encerrando ...!")
                return(np)
            else:
                print("Album terá ", np ,"página(s)!")
                break
    return(np)         
