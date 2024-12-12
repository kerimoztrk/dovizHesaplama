import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
def fiyatlariGetir():
    url='https://bigpara.hurriyet.com.tr/doviz/'
    response=requests.get(url)
    if response.status_code==200:
        soup=BeautifulSoup(response.content,'html.parser')
        ul_list=soup.find_all('ul',style=True)
        fiyatlar=[]
        for ul in ul_list:
            dovizCinsiElement=ul.find('li',class_='cell010 tal')
            if dovizCinsiElement:
                dovizCinsi=dovizCinsiElement.text.strip()
                satisFiyatiElement=ul.find_all('li',class_='cell015')
                if satisFiyatiElement and len(satisFiyatiElement)>1:
                    satisFiyati = float(satisFiyatiElement[1].text.strip().replace(',', '.'))

                    fiyatlar.append((dovizCinsi,satisFiyati))
        return fiyatlar
    else:
        messagebox.showerror('HATA','Döviz fiyatları çekilemedi')
        return None

def hesapla():
    try:
        tlMiktari=float(entryYatirim.get())
        fiyatlar=fiyatlariGetir()
        if fiyatlar:
            for widget in resultCanvasFrame.winfo_children():
                widget.destroy()
            for i ,(dovizCinsi,satisFiyati)in enumerate(fiyatlar):
                alinabilecekMiktar=tlMiktari/satisFiyati
                dovizLabel=tk.Label(resultCanvasFrame,text=dovizCinsi,font=("Arial",12),anchor="w")
                dovizLabel.grid(row=i, column=0,padx=10,pady=5,sticky="w")
                miktarLabel=tk.Label(resultCanvasFrame,text=f"{alinabilecekMiktar:.2f}",font=("Arial",12),anchor="e")
                miktarLabel.grid(row=i, column=1,padx=10,pady=5,sticky="e")

                resultCanvas.update_idletasks()
                resultCanvas.config(scrollregion=resultCanvas.bbox("all"))

    except ValueError:
        messagebox.showerror("hata","Lütfen geçerli bir tl miktarı giriniz.")

root=tk.Tk()
root.title('Döviz hesaplayıcı')
root.geometry('400x500')
root.config(bg="#e6e6fa")

titleLabel=tk.Label(root,text='Döviz hesaplayıcısı',font=("Arial",24,"bold"),bg="#e6e6fa")

titleLabel.pack(pady=20)

entryFrame=tk.Frame(root,bg="#e6e6fa")
entryFrame.pack(pady=10)

entryLabel=tk.Label(entryFrame,text="yatırım miktarı (TL): ",font=("Arial",14),bg="#e6e6fa")
entryLabel.grid(row=0,column=0,padx=5)
entryYatirim=tk.Entry(entryFrame,font=("Arial",14),width=10)
entryYatirim.grid(row=0,column=1,padx=5)

hesaplaButton=tk.Button(root,text="hesapla",font=("Arial",14),command=hesapla,bg="#4CAF50",fg="white")
hesaplaButton.pack(pady=20)

resultFrame=tk.Frame(root,bg="#f0f0f0",bd=2,relief="solid")
resultFrame.pack(pady=10,fill="both")
resultCanvas=tk.Canvas(resultFrame,bg="#f0f0f0")
resultCanvas.pack(side="left",fill="both",expand=True)

scrollBar=tk.Scrollbar(resultFrame,orient="vertical",command=resultCanvas.yview)
scrollBar.pack(side="right",fill="y")

resultCanvas.configure(yscrollcommand=scrollBar.set)

resultCanvasFrame=tk.Frame(resultCanvas,bg="#f0f0f0")
resultCanvas.create_window((0,0),window=resultCanvasFrame,anchor="nw")
        

root.mainloop()