# Pakete Import
import tkinter as tk
from tkinter import ttk
import tkintermapview
import geocoder
from geopy import distance

#Programmversion
progver="1.0"

#auswahl der Farbe für das gesamten Fenster
bgcolor="#FFDEAD" #Hintergrundfarbe
bgcolor1="LightGoldenrod" # für Label
fgcolor="black" #Schriftfarbe

#auswahl der Schrift für das gesamten Fenster
schrift="Helvetica"
schriftgröße=12
schriftart="bold"

#erstellung fenster
app=tk.Tk()
app.geometry('1200x750')#größe festlegen
app.resizable(width=0, height=0)#größenänderung gesperrt
app.configure(bg=bgcolor)
app.title(f"Kartendarstellung V.{progver}") #Titel für das Programmfenster

# Erstellung der Ausgabekarte
map_ausgabe=tkintermapview.TkinterMapView(app, width=700, height=450,corner_radius=0,relief="ridge")
map_ausgabe.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",max_zoom=22)

erklaerung=f"--- Eingabe und Anzeige von Orten in einer Karte ---\n\nDie Kartendarstellung ist änderbar, dabei ist 'Google normal' die Standarteinstellung.\nEs können Orte oder GPS-Koordinaten [Eingabebeispiel:71.256235, 21.25458] eingegeben werden.\nDeweiteren kann die Darstellung zwischen Maker oder und Linien ausgewählt werden.\n\nBevor jedoch die beiden vorherigen genannten Auswahlmöglichkieten verändert werden,\nbitte die Karte zurücksetzen!\n\nMit 'Entfernung berechnen' wir die Distanz zwischem der ersten und letzten Eingabe berechnet."

## Eingabe / Ausgabe Textfelder
# Eingabe
eingabe1_txt=tk.Entry(app,font=(schrift,schriftgröße,schriftart),width = 22)

# Ausgabe
ausgabe_entfernung_lbl=tk.Label(app,font=(schrift,schriftgröße,schriftart),
                            width = 18,height=4,relief="sunken",
                            bg="LightSteelBlue",fg=fgcolor)
ausgabe_entfernung_lbl.configure(text='Benötigt\nwerden mindestens\nzwei Einträge')

# Combobox Eingabe
eingabe_auswahl = ttk.Combobox(app,font=(schrift,schriftgröße,schriftart),
                               width = 20,values=["Ort", "GPS-Koordinaten"])
eingabe_auswahl.set('Ort')

eingabe_zusatz = ttk.Combobox(app,font=(schrift,schriftgröße,schriftart),
                              width = 20,values=["Maker und Linie","Maker","Linie"])
eingabe_zusatz.set('Maker und Linie')

eingabe_ansicht= ttk.Combobox(app,font=(schrift,schriftgröße,schriftart),
                               width = 15,values=["Google normal", "Google satellite",
                                                  "OpenStreetMap","painting style","black and white"])
eingabe_ansicht.set("Google normal")

# Label
label_erklaerung=tk.Label(app,text=erklaerung,
                          font=(schrift,schriftgröße,schriftart),
                          bg=bgcolor1,fg=fgcolor,
                          borderwidth = 2,
                          width = 110,
                          height= 11,
                          relief="ridge")

label_eingabe1=tk.Label(app,text="Eingabefeld",
                          font=(schrift,schriftgröße,schriftart),
                          bg=bgcolor1,fg=fgcolor,
                          borderwidth = 2,
                          width = 22,
                          relief="ridge")

label_eingabe_auswahl=tk.Label(app,text="Was wird eingegeben",
                          font=(schrift,schriftgröße,schriftart),
                          bg=bgcolor1,fg=fgcolor,
                          borderwidth = 2,
                          width = 22,
                          relief="ridge")

label_eingabe_zusatz=tk.Label(app,text="Was soll angezeigt werden",
                          font=(schrift,schriftgröße,schriftart),
                          bg=bgcolor1,fg=fgcolor,
                          borderwidth = 2,
                          width = 22,
                          relief="ridge")

label_eingabe_kartendarstellung=tk.Label(app,text="Kartendarstellung",
                          font=(schrift,schriftgröße,schriftart),
                          bg="sienna1",fg=fgcolor,
                          borderwidth = 2,
                          width = 22,
                          relief="ridge")

fuss_lbl=tk.Label(app,text=f"Programmversion {progver}",relief="solid",bg=bgcolor,fg=fgcolor)

#Listen für Funktionen
eingabe_liste_ort=[]
eingabe_liste_gps=[]

## Funktionen
# Darstellung der Karte
def karte_erstellen(liste_fuer_karte,zusatzangabe,auswahleingabe):
    
    if auswahleingabe=="Ort":
        if zusatzangabe =="Linie":
            map_ausgabe.set_address(liste_fuer_karte[0])
            map_ausgabe.set_path([geocoder.osm(i).latlng for i in liste_fuer_karte])
            
        elif zusatzangabe == "Maker":
            for i in liste_fuer_karte:
                map_ausgabe.set_address(i, marker=True)
            map_ausgabe.set_address(liste_fuer_karte[0])
            
        elif zusatzangabe == "Maker und Linie":
            for i in liste_fuer_karte:
                map_ausgabe.set_address(i, marker=True)
            map_ausgabe.set_address(liste_fuer_karte[0])        
            map_ausgabe.set_path([geocoder.osm(i).latlng for i in liste_fuer_karte])
    
    elif auswahleingabe=="GPS-Koordinaten":
        if zusatzangabe =="Linie":
            map_ausgabe.set_position(float(liste_fuer_karte[0].split(", ")[0]),
                                     float(liste_fuer_karte[0].split(", ")[1]))
            map_ausgabe.set_path([tuple(float(s) for s in i.split(", ")) for i in liste_fuer_karte])
        
        elif zusatzangabe =="Maker":
            for i in liste_fuer_karte:
                map_ausgabe.set_position(float(i.split(", ")[0]),
                                         float(i.split(", ")[1]),
                                         marker=True)
            map_ausgabe.set_position(float(liste_fuer_karte[0].split(", ")[0]),
                                     float(liste_fuer_karte[0].split(", ")[1]))
        
        elif zusatzangabe == "Maker und Linie":
            for i in liste_fuer_karte:
                map_ausgabe.set_position(float(i.split(", ")[0]),
                                         float(i.split(", ")[1]),
                                         marker=True)    
                map_ausgabe.set_position(float(liste_fuer_karte[0].split(", ")[0]),
                                     float(liste_fuer_karte[0].split(", ")[1]))
                map_ausgabe.set_path([tuple(float(s) for s in i.split(", ")) for i in liste_fuer_karte])
        
# Hinzufügen der Eingaben
def add():
    global eingabe_liste_ort
    global eingabe_liste_gps
    
    try:
    #Befüllen der Listen
        if eingabe_auswahl.get() == "GPS-Koordinaten":
            eingabe_liste_ort=[]
            eingabe_liste_gps.append(eingabe1_txt.get())
            karte_erstellen(eingabe_liste_gps,eingabe_zusatz.get(),eingabe_auswahl.get())                
        elif eingabe_auswahl.get() == "Ort":
            eingabe_liste_gps=[]
            eingabe_liste_ort.append(eingabe1_txt.get())
            karte_erstellen(eingabe_liste_ort,eingabe_zusatz.get(),eingabe_auswahl.get())
        else:
            None
       
    except:
        pass

# Kartendarstellung ändern
def change_map():
    if eingabe_ansicht.get() == "OpenStreetMap":
        map_ausgabe.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
    elif eingabe_ansicht.get() == "Google normal":
        map_ausgabe.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif eingabe_ansicht.get() == "Google satellite":
        map_ausgabe.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    elif eingabe_ansicht.get() == "painting style":   
        map_ausgabe.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")
    elif eingabe_ansicht.get() == "black and white":   
        map_ausgabe.set_tile_server("http://a.tile.stamen.com/toner/{z}/{x}/{y}.png")
        
# Berechnung der Entfernung
def entfernung_berechnen():
    if len(eingabe_liste_gps)>=2 or len(eingabe_liste_ort)>=2:
        if eingabe_auswahl.get() == "GPS-Koordinaten":
            message=f'Entfernung zwischen\nerstem und letztem\nPunkt: {round((distance.distance(eingabe_liste_gps[0],eingabe_liste_gps[len(eingabe_liste_gps)-1]).km),2)} km'
        elif eingabe_auswahl.get() == "Ort":
            liste=[geocoder.osm(gps).latlng for gps in eingabe_liste_ort]
            message=f'Entfernung zwischen\nerstem und letztem\nPunkt: {round((distance.distance(liste[0],liste[len(liste)-1]).km),2)} km'
    else:
        message='Benötigt\nwerden mindestens\nzwei Einträge'
    
    ausgabe_entfernung_lbl.configure(text=message)
    
# Listen zurücksetzten, Marker/Linien entfernen, eingabefeld leeren
def reset():
    # Global stellen der Liste
    global eingabe_liste_ort
    global eingabe_liste_gps
               
    eingabe_liste_ort=[]
    eingabe_liste_gps=[]
    
    map_ausgabe.delete_all_marker()
    map_ausgabe.delete_all_path()
    
    for i in app.winfo_children():
        if isinstance(i,tk.Entry):
            eingabe1_txt.delete(0,'end')
        if isinstance(i,ttk.Combobox):
            eingabe_auswahl.set('Ort')
            eingabe_zusatz.set('Maker und Linie')
            eingabe_ansicht.set("Google normal")
        if isinstance(i,tk.Label):
            ausgabe_entfernung_lbl.configure(text='Benötigt\nwerden mindestens\nzwei Einträge')
    
# Button
button_reset=tk.Button(app,text="Zurücksetzen",
                       bg="yellow2",fg=fgcolor,relief="ridge",
                       font=(schrift,schriftgröße,schriftart),
                       command=reset)

button_add=tk.Button(app,text="Eingabe\nHinzufügen",
                     bg="SpringGreen3",fg=fgcolor,relief="ridge",
                     font=(schrift,schriftgröße,schriftart),
                     command=add)

button_change_map=tk.Button(app,text="Kartendarstellung\nändern",
                     bg="sienna1",fg=fgcolor,relief="ridge",
                     font=(schrift,schriftgröße,schriftart),
                     command=change_map)

button_berrechnung_entfernung=tk.Button(app,text="Entfernung\nberechnen",
                     bg="LightSteelBlue",fg=fgcolor,relief="ridge",
                     font=(schrift,schriftgröße,schriftart),
                     command=entfernung_berechnen)

button_close=tk.Button(app,text="Beenden",
                       bg="OrangeRed",fg=fgcolor,relief="ridge",
                       font=(schrift,schriftgröße,schriftart),
                       command=app.destroy)

#Positionierung
label_erklaerung.place(x=50, y=10)
label_eingabe_auswahl.place(x=780, y=240)
eingabe_auswahl.place(x=952, y=275)
label_eingabe_zusatz.place(x=780, y=310)
eingabe_zusatz.place(x=952, y=345)
label_eingabe1.place(x=780, y=380)
eingabe1_txt.place(x=952, y=415)
button_add.place(x=1050, y=450)
label_eingabe_kartendarstellung.place(x=780,y=450)
eingabe_ansicht.place(x=780,y=490)
button_change_map.place(x=780,y=530)
map_ausgabe.place(x=50,y=240)
button_berrechnung_entfernung.place(x=800,y=600)
ausgabe_entfernung_lbl.place(x=950,y=550)
button_reset.place(x=935,y=657)
button_close.place(x=1070,y=657)
fuss_lbl.pack(side = 'bottom')

app.mainloop()