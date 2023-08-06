"""Assembly a photo album.

Usage:
------

    $ photoalbum [lng] 


Contact:
--------

- leobia2009@yahoo.com.br

More information is available at:

- https://pypi.org/project/leopaolucci-photoalbum/
- https://github.com/leobia2009/EDUCATION/photoalbum


Version:
--------

- leopaolucci-photoalbum v0.0.1
"""

#standard libs imports
import locale
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox as mb
from PyPDF2 import PdfFileMerger

from datetime import date, datetime

#photoalbum imports
import photoalbum
from photoalbum import toolsphotoalbum as tl


def main() -> None:

    #dictionary of languages
    lng_keys = {1: 'ptbr', 2: 'en'}
    language =""
 
    msg_dict = {1: {'msg1':"Clique SIM para fazer busca das fotos ou NÃO para sair!",
                    'msg2':"Selecione o diretorio das fotos!!:",
                    'msg3':"Clique SIM para escolher onde GRAVAR album ou NÃO para sair!",
                    'msg4':"Selecione o diretorio para Gravação!!",
                    'msg5':"Você escolheu SAIR !",
                    'msg6':"Encerrando ...!!!",
                    'msg7':"Numero de fotos insuficiente !!!!\n",
                    'msg8':"Voce possui ",
                    'msg9':" fotos !!!!\n",
                    'msg10':"Aguarde gerando pagina do album ...!",
                    'msg11':"Rotina retornou um ERRO!!!",
                    'msg12':"Album de fotografias_",
                    'msg13':"Idiomas disponiveis:"}, 
                #messages in english    
                2: {'msg1':"Click YES to search the photos or NO to exit!",
                    'msg2':"Select the photo directory!!:",
                    'msg3':"Click YES to choose where to RECORD album or NO to exit!",
                    'msg4':"Select the directory for Recording!!",
                    'msg5':"You have chosen EXIT !",
                    'msg6':"Closing...!!!",
                    'msg7':"Insufficient number of photos !!!!\n",
                    'msg8':"You own ",
                    'msg9':" pictures !!!!\n",
                    'msg10':"Please wait, generating album page...!",
                    'msg11':"Routine returned an ERROR!!!",
                    'msg12':"Photo album_",
                    'msg13':"Languages availables: "}
                }
 
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    # An language [lng] ID is given, show language version
    try:
        if args:
            for lng_id in args:
                for key, value in lng_keys.items():
                    if lng_id == value:
                        language = key
                        break
                    else:
                        if  key == len(lng_keys.items()):
                            language = 2 
                            messages = msg_dict.get(language) 
                            #print("Rotina retornou um ERRO!!!")
                            print(messages.get('msg11'))
                            print(''.join([messages.get('msg13'),": ",str(lng_keys.values())]))
                            #print("Encerrando ...!!!")
                            print(messages.get('msg6'))
                            print(key)
                            print(value)
                            return
                       
                   
        # No [lng]ID is given, 
        else:
            #default language english
            language = 2 

                
    except KeyError:
    
        language = 2 
        messages = msg_dict.get(language) 
        #print("Rotina retornou um ERRO!!!")
        print(messages.get('msg11'))
        #print("Encerrando ...!!!")
        print(messages.get('msg6'))
        return
            
    finally:     
        pass    
          
    #select the messages for the language
    messages = msg_dict.get(language)   
    
    wDir = os.getcwd()
    cDirt = "" 
    npages = 0
    nfotos = 0  
    nlayout = 0

    today = date.today()
    actual = datetime.now()

    dia = str(today.day)
    mes = str(today.month)
    ano = str(today.year)
    data = ('-'.join([dia,mes,ano]))

    hora = str(actual.hour)+'h'
    minuto = str(actual.minute)+'m' 
    segundo = str(actual.second)+'s'  
    hora = (''.join([hora,minuto,segundo]))


   
            
   
    while True:
        
        
        #val1 = messagebox.askyesno("", "Clique SIM para fazer busca das fotos ou NÃO para sair!")
        val1 = mb.askyesno("", messages.get('msg1'))
        
        #if (res == 'yes'):
        if (val1 == True):    
           #tit = "Selecione o diretorio das fotos!!:"
           tit = messages.get('msg2')
           cDirt = tl.open_dir(tit,language)
           
           if (cDirt == ""):
               #print("Você escolheu SAIR !")
               print(messages.get('msg5'))
               #print("Encerrando ...!!!")
               print(messages.get('msg6'))
               exit(0)
              
           matpath = os.listdir(cDirt)
              
           # val2 = messagebox.askyesno("", "Clique SIM para escolher onde GRAVAR album ou NÃO para sair!")
           val2 = mb.askyesno("", messages.get('msg3'))
           if (val2 == True):
              #tit = "Selecione o diretorio de Gravação!!:"
              tit = messages.get('msg4')
              cGrava = tl.open_dir(tit,language)
              
           else:
              #print("Você escolheu SAIR !")
              print(messages.get('msg5'))
              #print("Encerrando ...!!!")
              print(messages.get('msg6'))
              exit(0)
        else:
           #print("Você escolheu SAIR !")
           print(messages.get('msg5'))
           #print("Encerrando ...!!!")
           print(messages.get('msg6'))
           exit(0)
        
        npages  = tl.number_of_pages()
        nfotos  = tl.photos_per_page()
        
        if ( (npages == 0) | (nfotos == 0) ):
            break
        

        nlayout = tl.number_of_layout(nfotos)

        cont_page = 1
        inifoto = 0
        fimfoto = 0
        cp = 0
        
        if (nfotos*npages > len(matpath)):
            #print("Numero de fotos insuficiente !!!!\n")
            print(messages.get('msg7'))
            #print(''.join(["Voce possui ",str(nfotos)," fotos !!!!\n"]))
            print(''.join([messages.get('msg8'),str(nfotos),messages.get('msg9')]))
            continue
         
          
        cp = len(matpath) - nfotos * npages
        fimfoto = int( (len(matpath)-cp)/npages - 1)
        
        while (cont_page <= npages):
        
            try:
                titulo = ''.join(["Pag.",str(cont_page),"_",data," ",hora,"_.pdf"])
                if ( os.path.exists(''.join([cGrava,"/", titulo]))):
                      os.remove((''.join([cGrava,"/", titulo])))
             
                print(''.join([cGrava,"/", titulo]))
                nl = nlayout["linhas"]
                nc = nlayout["colunas"]
                          
                if (nl > len(matpath)):
                  nl <- len(matpath)

                
                #print("Aguarde gerando pagina do album ...!")
                print(messages.get('msg10'))
                lista_de_fotos = tuple(range(inifoto,fimfoto+1))   
                
                fig = plt.figure(cont_page)        
                for iplot in tuple(range(1,nfotos+1)):
                  fig.add_subplot(nl,nc,iplot)
                  plt.tick_params(axis='x', which='both', bottom=False, 
                                  top=False, labelbottom=False) 
                  plt.tick_params(axis='y', which='both', right=False, 
                                  left=False, labelleft=False)
                  
                  print(matpath[lista_de_fotos[iplot-1]])
                  file_to_read = (''.join([cDirt,"/",matpath[lista_de_fotos[iplot-1]]]))
                  print(file_to_read)
                  img = mpimg.imread(file_to_read)
                  plt.imshow(img)
                  
                  wdir = os.getcwd()
                  os.chdir(cGrava)
                  fig.savefig((''.join(["Pag.",str(cont_page),"_",data," ",hora,"_.pdf"])))
                  os.chdir(wdir)
                               
            except ValueError:
                  #print("Rotina retornou um ERRO!!!")
                  print(messages.get('msg11'))
                  #print("Encerrando ...!!!")
                  print(messages.get('msg6'))
                  break
            
            finally:     
                  pass
                               
                   
            cont_page += 1
            inifoto +=  nfotos
            fimfoto +=  nfotos
        
        wdir = os.getcwd()
        os.chdir(cGrava)
        matpdf = os.listdir(cGrava)    
        #output = ''.join(["Album de fotografias_",data," ",hora,"_.pdf"])
        output = ''.join([messages.get('msg12'),data," ",hora,"_.pdf"])
        
        merger = PdfFileMerger()
        for isave in matpdf:
            with open(isave, 'rb') as f: 
                merger.append(f)  
                
        with open(output, 'wb') as f: 
            merger.write(f)    
             
        merger.close()
        #print("Encerrando ...!!!")
        print(messages.get('msg6'))
        for cont_page in tuple(range(1,npages+1)):
            if ( os.path.exists(''.join([cGrava,"/","Pag.",str(cont_page),"_",data," ",hora,"_.pdf"]))):
                          os.remove(''.join([cGrava,"/","Pag.",str(cont_page),"_",data," ",hora,"_.pdf"]))
                      
        break



if __name__ == "__main__":
    main()