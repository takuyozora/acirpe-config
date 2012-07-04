#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, GLib, GObject, WebKit
from time import sleep
import thread
import os
import subprocess
import rapport
import platform

SPEED_DEBUG = False
DEBUG = True

def get_cwd():
    path = os.getcwd()
    if DEBUG:
        return path
    else:
        return path+"/src/"

def protect_path(path):
    new_path = ""
    for char in path:
        if char in (" ","\"","'","(",")"):
            new_path += "\\"+char
        else:
            new_path += char
    return new_path

def all_quit(*args,**kwargs):
    thread.all_stop()
    Gtk.main_quit()
        
class ProgressList(Gtk.VBox):
    def __init__(self,width=200,mtop=30,mside=10,mbottom=100,*args,**kwargs):
        Gtk.VBox.__init__(self,spacing=2,*args,**kwargs)
        self.set_property("width_request",width)
        self.set_property("margin-top",mtop)
        self.set_property("margin-right",mside)
        self.set_property("margin-left",mside)
        self.set_property("margin-bottom",mbottom)
        self._elems = list()
        self._old = 0
        self._active = 0
        self._order = dict()
        self.connect("map",self._update)
        
    def place(self):
        sep = Gtk.VBox()
        sep.pack_start(Gtk.HSeparator(),False,False,0)
        sep.pack_start(self,True,True,0)
        box = Gtk.EventBox()
        box.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(0.9,0.9,0.9,0.5))
        box.add(sep)
        return box
        
    def pack_end(self,title,label,*args,**kwargs):
        self._elems.insert(0,{"title":title,"widget":label,"label":label.get_label()})
        self._order[title] = len(self._elems)-1
        Gtk.VBox.pack_end(self,label,*args,**kwargs)
        label.set_property("padding",8)
        label.set_property("justify",Gtk.Justification.LEFT)
        label.set_line_wrap(True)
        
    def pack_start(self,title,label,*args,**kwargs):
        self._elems.append({"title":title,"widget":label,"label":label.get_label()})
        for title in self._order.keys():
            self._order[title] += 1
        self._order[title] = 0
        Gtk.VBox.pack_start(self,label,*args,**kwargs)
        label.set_alignment(0,0)
        label.set_line_wrap(True)
    
    def gtk_widget_draw(self):
        self._update()
        Gtk.VBox.gtk_widget_draw(self)
        
    def next_active(self,*args):
        self._old = self._active
        self._active += 1
        if self._active >= len(self._elems):
            self._active = 0
        self._update()
        
    def prev_active(self,*args):
        self._old = self._active
        self._active -= 1
        if self._active < 0:
            self._active = len(self._elems)-1
        self._update()
        
    def _update(self,*args):
        self._elems[self._old]["widget"].set_label(self._elems[self._old]["label"])
        self._elems[self._active]["widget"].set_markup("<b>"+self._elems[self._active]["label"]+"</b>")
        
class Step():
    def __init__(self,title,next_step,*args,**kwargs):
        self.next_step = next_step
        self.box = Gtk.VBox()
        self.box.set_property("width_request",400)
        self.box.set_property("margin-left",20)
        self.box.set_property("margin-right",20)
        self.box.set_property("margin-top",10)
        self.box.set_property("margin-bottom",10)
        self.title = Gtk.Label(label="<b><big>"+title+"</big></b>",use_markup=True)
        self.box.pack_start(self.title,False,True,0)
        self.title.set_property("margin-top",10)
        self.title.set_property("margin-bottom",25)
    def validate(self):
        pass
        
class StepPreparation(Step):
    def __init__(self,next_step,*args,**kwargs):
        Step.__init__(self, "Préparation",next_step)
        text = Gtk.Label(label="""Vous vous apretez à créer une rapport sur la configuration de votre ordianteur, pour cela cliquez sur le bouton <i>Créer un nouveau rapport</i>. Vous pouvez également convertir un rapport en PDF. """,use_markup=True,wrap=True,width_request=300)
        self.box.pack_start(text,False,True,0)
        box_select_type = Gtk.HBox()
        box_select_type.set_property("margin-left",30)
        box_select_type.set_property("margin-top",10)
        box_select_type.pack_start(Gtk.Label(label="Format de sortie :"),False,False,0)
#        self.select_type = Gtk.ComboBoxText()
#        self.select_type.set_property("margin-left",30)
#        self.select_type.set_entry_text_column(0)
#        self.select_type.append_text("PDF")
#        self.select_type.append_text("HTML")
#        self.select_type.append_text("RawData")
#        self.select_type.set_active(0)
#        box_select_type.pack_start(self.select_type,False,False,0)
#        self.box.pack_start(box_select_type,False,False,0)
        self.continue_button = Gtk.Button(label="Créer un nouveau rapport")
        self.continue_button.set_property("halign",Gtk.Align.END)
        self.continue_button.set_property("valign",Gtk.Align.END)
        self.continue_button.set_property("margin-top",30)
        self.continue_button.connect("clicked",self.next_step,self)
        self.pdf_button = Gtk.Button(label="Convertir en PDF",margin_top=20,halign=Gtk.Align.START,valign=Gtk.Align.END)
        self.pdf_button.connect("clicked",self.export_pdf)
        box = Gtk.HBox()
        box.pack_start(self.pdf_button,True,True,0)
        box.pack_start(self.continue_button,True,True,0)
        self.box.pack_start(box,True,True,0)
        
    def validate(self):
#        Config.format = self.select_type.get_active_text()
        pass
    
    def export_pdf(self,widget=None):
        dialog = Gtk.FileChooserDialog("Sélectionner un fichier", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        
        folder = get_cwd()+"/../rapport/"
        dialog.set_current_folder(os.path.normpath(folder))

        filter_html = Gtk.FileFilter()
        filter_html.set_name("html")
        filter_html.add_mime_type("text/html")
        dialog.add_filter(filter_html)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Touts les fichiers")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            self.pdf_step(filename)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            
    def pdf_step(self,filepath):
        filename = ".".join(filepath.split(".")[:-1])+".pdf"
        path = protect_path(get_cwd())
#        if not DEBUG:
#            path += "/src/"
        cmd = path+"/html2pdf "+protect_path(filepath)+" "+protect_path(filename)
        return_code,response = subprocess.getstatusoutput(cmd)
        print("html2pdf :: "+response)
        try:
            os.chmod(filename, int("666",8))
        except:
            pass
        if return_code != 0:
            dialog = Gtk.MessageDialog(window, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, message_format="Impossible d'enregistrer la rapport dans le fichier selectionné.\nSelectionez-en un autre.")
            dialog.run()
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(parent=window, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE, message_format="Le rapport a corretcement été enrgistré en pdf")
            dialog.run()
            dialog.destroy()
        
class Step():
    def __init__(self,title,next_step,*args,**kwargs):
        self.next_step = next_step
        self.box = Gtk.VBox()
        self.box.set_property("width_request",400)
        self.box.set_property("margin-left",20)
        self.box.set_property("margin-right",20)
        self.box.set_property("margin-top",10)
        self.box.set_property("margin-bottom",10)
        self.title = Gtk.Label(label="<b><big>"+title+"</big></b>",use_markup=True)
        self.box.pack_start(self.title,False,True,0)
        self.title.set_property("margin-top",10)
        self.title.set_property("margin-bottom",25)
    def validate(self):
        pass
        
class StepPreparation(Step):
    def __init__(self,next_step,*args,**kwargs):
        Step.__init__(self, "Préparation",next_step)
        text = Gtk.Label(label="""Vous vous apretez à créer une rapport sur la configuration de votre ordianteur, pour cela cliquez sur le bouton <i>Créer un nouveau rapport</i>. Vous pouvez également convertir un rapport en PDF. """,use_markup=True,wrap=True,width_request=300)
        self.box.pack_start(text,False,True,0)
        box_select_type = Gtk.HBox()
        box_select_type.set_property("margin-left",30)
        box_select_type.set_property("margin-top",10)
        box_select_type.pack_start(Gtk.Label(label="Format de sortie :"),False,False,0)
#        self.select_type = Gtk.ComboBoxText()
#        self.select_type.set_property("margin-left",30)
#        self.select_type.set_entry_text_column(0)
#        self.select_type.append_text("PDF")
#        self.select_type.append_text("HTML")
#        self.select_type.append_text("RawData")
#        self.select_type.set_active(0)
#        box_select_type.pack_start(self.select_type,False,False,0)
#        self.box.pack_start(box_select_type,False,False,0)
        self.continue_button = Gtk.Button(label="Créer un nouveau rapport")
        self.continue_button.set_property("halign",Gtk.Align.END)
        self.continue_button.set_property("valign",Gtk.Align.END)
        self.continue_button.set_property("margin-top",30)
        self.continue_button.connect("clicked",self.next_step,self)
        self.pdf_button = Gtk.Button(label="Convertir en PDF",margin_top=20,halign=Gtk.Align.START,valign=Gtk.Align.END)
        self.pdf_button.connect("clicked",self.export_pdf)
        box = Gtk.HBox()
        box.pack_start(self.pdf_button,True,True,0)
        box.pack_start(self.continue_button,True,True,0)
        self.box.pack_start(box,True,True,0)
        
    def validate(self):
#        Config.format = self.select_type.get_active_text()
        pass
    
    def export_pdf(self,widget=None):
        dialog = Gtk.FileChooserDialog("Sélectionner un fichier", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        
        folder = get_cwd()+"/../rapport/"
        dialog.set_current_folder(os.path.normpath(folder))

        filter_html = Gtk.FileFilter()
        filter_html.set_name("html")
        filter_html.add_mime_type("text/html")
        dialog.add_filter(filter_html)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Touts les fichiers")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            self.pdf_step(filename)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            
    def pdf_step(self,filepath):
        filename = ".".join(filepath.split(".")[:-1])+".pdf"
        path = protect_path(get_cwd())
#        if not DEBUG:
#            path += "/src/"
        cmd = path+"/html2pdf-"+platform.architecture()[0]+" "+protect_path(filepath)+" "+protect_path(filename)
        return_code = subprocess.getstatusoutput(cmd)
        try:
            os.chmod(filename, int("666",8))
        except:
            pass
        if return_code[0] != 0:
            dialog = Gtk.MessageDialog(window, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, message_format="Impossible d'enregistrer la rapport dans le fichier selectionné.\nSelectionez-en un autre.")
            dialog.run()
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(parent=window, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE, message_format="Le rapport a corretcement été enrgistré en pdf")
            dialog.run()
            dialog.destroy()

        
    
class StepFinish(Step):
    def __init__(self,next_step):
        Step.__init__(self, "Rapport enregistré avec succes",next_step)
        text = Gtk.Label(label="""Le rapport a bien été sauvegardé, il peut maintenant être modifier manuellement si besoin avant de l'exporter définitvement vers un pdf.""",wrap=True,width_request=300)
        self.continue_button = Gtk.Button(label="Retour au début",margin_top=20,halign=Gtk.Align.START,valign=Gtk.Align.END)
        self.continue_button.connect("clicked",self.next_step)
        self.box.pack_start(text,False,False,0)
        self.box.pack_start(self.continue_button,True,True,0)
        
    def exit_prog(self,widget):
        self.next_step()
class StepShow(Step):
    def __init__(self,next_step,prev_step):
        Step.__init__(self, "Apperçus du rapport", next_step)
        self.prev_step = prev_step
        text = Gtk.Label(label="Vous pouvez apercevoir le rendu du rapport qui vient d'être généré. Si des informations manquent toujours vous pouvez veneir en arrière pour les modifier",wrap=True,width_request=300)
        self.box.pack_start(text,False,False,0)
        self.view = WebKit.WebView(margin_top=15,margin_bottom=20) 
        self.sw = Gtk.ScrolledWindow(width_request=580,height_request=450)
        self.sw.add(self.view)
        self.view.load_html_string(Config.create_html(),"")
        self.view.set_zoom_level(0.55)
        self.box.pack_start(self.sw,True,False,0)
        self.continue_button = Gtk.Button(label="Continuer",margin_top=20,halign=Gtk.Align.END,valign=Gtk.Align.END)
        self.continue_button.connect("clicked",self.next_step,self)
        self.prev_button = Gtk.Button(label="Retour",margin_top=20,halign=Gtk.Align.START,valign=Gtk.Align.END)
        self.prev_button.connect("clicked",self.prev_step,self,False)
        box = Gtk.HBox()
        box.pack_start(self.prev_button,True,True,0)
        box.pack_start(self.continue_button,True,True,0)
        self.box.pack_start(box,True,True,0)
        
        
class StepExport(Step):
    def __init__(self,next_step,prev_step):
        Step.__init__(self, "Enregistrement du rapport", next_step)
        self.prev_step = prev_step
        text = Gtk.Label(label="Le rapport est maintenant terminé et doit encore être éxporté.\nVeuillez selectioner un emplacement pour enregistrer le rapport",wrap=True,width_request=300)
        self.box.pack_start(text,False,False,0)
        self.continue_button = Gtk.Button(label="Enregistrer sous",margin_top=20,halign=Gtk.Align.END,valign=Gtk.Align.END)
        self.continue_button.connect("clicked",self.choose_file)
        self.prev_button = Gtk.Button(label="Retour",margin_top=20,halign=Gtk.Align.START,valign=Gtk.Align.END)
        self.prev_button.connect("clicked",self.prev_step,self,False)
        box = Gtk.HBox()
        box.pack_start(self.prev_button,True,True,0)
        box.pack_start(self.continue_button,True,True,0)
        self.box.pack_start(box,True,True,0)
        
    def next(self,widget):
        pass
    
    def choose_file(self,widget):
        dialog = Gtk.FileChooserDialog("Sélectionné un fichier", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        
        folder = get_cwd()+"/../rapport/"
        default_file = "ACIRPE-"+Config.data["get_acirpe_number"]+".html"
        dialog.set_current_folder(folder)
        dialog.set_current_name(default_file)

        filter_html = Gtk.FileFilter()
        filter_html.set_name("html")
        filter_html.add_mime_type("text/html")
        dialog.add_filter(filter_html)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Touts les fichiers")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if self.try_file(dialog.get_filename()):
                self.next_step(None,self)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()
        
    def try_file(self,path):
        ext = path.split(".")[-1]
        if "htm" not in ext:
            path += ".html"
        with open(path,"w") as file:
            file.write(Config.html)
            try:
                os.chmod(path, int("666",8))
            except:
                pass
            return True
        dialog = Gtk.MessageDialog(window, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, message_format="Impossible d'enregistrer la rapport dans le fichier selectionné.\nSelectionez-en un autre.")
        dialog.run()
        dialog.destroy()
        return False

class StepFillConfig(Step):
    def __init__(self,next_step):
        Step.__init__(self, "Modification et validation du rapport", next_step)
        text = Gtk.Label(label="Les informations collectées doivent maintenant être completées avant de valider le rapport de la configuration",wrap=True,width_request=300)
        self.box.pack_start(text,False,False,0)
        frame_label = Gtk.Label(label="<b>Informations indispensables</b>",use_markup=True,margin_bottom=5)   
        self.needed = list()
        self.missing = list()     
        self.needed_frame = Gtk.Frame(label_widget=frame_label,margin_top=15)
        self.needed_frame.set_shadow_type(Gtk.ShadowType.IN)
        self.needed_frame.set_label_align(0.1,0.0)
        self.needed_box = Gtk.VBox()
        if "get_acirpe_number" not in Config.data.keys():
            Config.critic.append(rapport.Donnee("Numéro ACIRPE","get_acirpe_number"))
        self.create_champ_indisp()
        self.needed_frame.add(self.needed_box)
        self.box.pack_start(self.needed_frame,False,False,0)
        self.needed_frame.show_now()
        if len(Config.missing) > 0:
            frame_label = Gtk.Label(label="<b>Informations Manquantes</b>",use_markup=True,margin_bottom=5)        
            self.missing_frame = Gtk.Frame(label_widget=frame_label,margin_top=15)
            self.missing_frame.set_shadow_type(Gtk.ShadowType.IN)
            self.missing_frame.set_label_align(0.1,0.0)
            self.missing_box = Gtk.VBox()
            self.create_champ_missing()
            self.missing_frame.add(self.missing_box)
            self.box.pack_start(self.missing_frame,False,False,0)
            self.missing_frame.show_now()
        self.continue_button = Gtk.Button(label="Continuer",margin_top=20,halign=Gtk.Align.END,valign=Gtk.Align.END,sensitive=False)
        self.continue_button.connect("clicked",self.next)
        self.box.pack_start(self.continue_button,True,True,0)
        self.is_needed_ok()
        self.continue_button.show()
        
    def create_champ(self,title,content="",critic=True):
        box = Gtk.HBox()
        text = Gtk.Label(label=title,halign=Gtk.Align.START)
        entry = Gtk.Entry(text=content,halign=Gtk.Align.END)
        if critic:
            entry.connect("changed",self.is_needed_ok)
        box.pack_start(text,True,True,0)
        box.pack_start(entry,False,False,0)
        return box
    
    def is_needed_ok(self,widget=None):
        for needed in self.needed:
            if needed[0].get_text() == "":
                self.continue_button.set_sensitive(False)
                return False
        self.continue_button.set_sensitive(True)
        
    def next(self,widget):
        for indisp in self.needed:
            Config.data[indisp[1]] = indisp[0].get_text()
        for missing in self.missing:
            Config.data[missing[1]] = missing[0].get_text()
        self.next_step(None,self)
        
    
    def create_champ_indisp(self):
        for indisp in Config.critic:
            box = self.create_champ(indisp.name, Config.data.get(indisp.fnct,""),critic=True)
            self.needed.append([box.get_children()[1],indisp.fnct])
            self.needed_box.pack_start(box,False,False,0)
            
    def create_champ_missing(self):
        for missing in Config.missing:
            box = self.create_champ(missing.name, Config.data.get(missing.fnct,""))
            self.missing.append([box.get_children()[1],missing])
            self.missing_box.pack_start(box,False,False,0)

class StepMakeConfig(Step):
    def __init__(self,next_step):
        Step.__init__(self,"Création du rapport",next_step)
        self.createAutoConf()
        
    def prepare_xml(self):
        if SPEED_DEBUG:
            self.finish()
            return None
        self.progress_bar.set_text("Analyse de la configuration de l'ordinateur")
        Config.generate_xml_data(on_finish=self.get_info)
        
    def get_info(self):
        self.progress_bar.stop()
        Config.make(on_finish=self._finish,progress=self.progress)
        
    def finish(self):
        self.progress_bar.set_text("Terminé")
        button = Gtk.Button(label="Continuer")
        button.set_property("margin-top",20)
        button.set_property("halign",Gtk.Align.END)
        button.set_property("valign",Gtk.Align.END)
        button.connect("clicked",self.next_step,self)
        self.box.pack_start(button,True,True,0)
        button.show()
        #self.box.show_now()
        
    def _finish(self):
        GObject.idle_add(self.finish)
        
    def progress(self,avance):
        GObject.idle_add(self.progress_bar.set_text,avance[1])
        GObject.idle_add(self.progress_bar.set_fraction,avance[0])
#        GObject.idle_add
        
    def createAutoConf(self):
        text = Gtk.Label(label="Le script va annalyser la configuration de l'ordinateur pour créer le rapport, si il manque des informations, celles-ci devront être ajoutées manuellement",wrap=True,width_request=300)
        self.progress_bar = PulseProgressBar()
        self.progress_bar.set_property("margin-top",30)
        self.progress_bar.set_show_text(True)
        self.progress_bar.start()
        self.box.pack_start(text,False,False,0)
        self.box.pack_start(self.progress_bar,False,False,0)
        self.prepare_xml()
        #Config.generate_xml_data(on_finish=self.progress_bar.stop)
        #Config.make(on_finish=self.progress_bar.stop)
        
    def next(self,w):
        pass
    
    def pulse(self,widget):
        if self.progress_bar.running:
            self.progress_bar.stop()
        else:
            self.progress_bar.start()
#        self.progress_bar.speed += 0.2

class PulseProgressBarThread(thread.Thread):
    def __init__(self,progress_bar):
        thread.Thread.__init__(self)
        self.progress_bar = progress_bar
        
    def run(self):
        while self.progress_bar.running:
            GObject.idle_add(self.progress_bar.pulse)
            #self.progress_bar.pulse()
            sleep(1/(self.progress_bar.speed*20))
        
        

class PulseProgressBar(Gtk.ProgressBar):
    def __init__(self,*args,**kwargs):
        Gtk.ProgressBar.__init__(self,*args,**kwargs)
        self.connect("destroy",self.stop)
        self.speed = 2
        self.set_property("pulse_step",0.02)
        self.running = False
        
    def start(self):
        self.running = True
        thread = PulseProgressBarThread(self)
        thread.start()
        
    def _run(self):
        while self.running:
            self.pulse()
            sleep(1/(self.speed*10))
            
    def stop(self,*args):
        self.running = False
            
        
class MainWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self,title="Rapport de configuration",icon_name=Gtk.STOCK_DND)

        self._begin()
        
        self.connect("delete-event", all_quit)
        
    def _begin(self):
        self.progressList = ProgressList()
        self.progressList.pack_start("prepa",Gtk.Label(label="Préparation"),False,False,0)
        self.progressList.pack_start("crea",Gtk.Label(label="Création de la configuration"),False,False,0)
        self.progressList.pack_start("valid",Gtk.Label(label="Modification et validation"),False,False,0)
        self.progressList.pack_start("aprecu",Gtk.Label(label="Aperçus"),False,False,0)
        self.progressList.pack_start("export",Gtk.Label(label="Export"),False,False,0)
        self.progressList.pack_start("fin",Gtk.Label(label="Terminé"),False,False,0)
        
        self.main = Gtk.HBox()
        self.main.pack_start(self.progressList.place(),True,True,0)
        self.main.pack_start(Gtk.VSeparator(),False,False,0)
        
        self.current_step = StepPreparation(self.stepMakeConfig)
        self.main.pack_end(self.current_step.box,True,True,0)
        self.add(self.main)
        
    def stepMakeConfig(self,widget,prev_step,next=True):
        prev_step.validate()
        self.current_step = StepMakeConfig(next_step=self.stepFillConfig)
        #prev_step.box.set_visible(False)
        self.main.remove(prev_step.box)
        #self.remove(self.main)
        self.main.pack_end(self.current_step.box,True,True,0)
        if next:
            self.progressList.next_active()
        else:
            self.progressList.prev_active()
        self.current_step.box.show_all()
        
        #self.add(self.main)
     
        
    def stepFillConfig(self,widget,prev_step,next=True):
        prev_step.validate()
        self.current_step = StepFillConfig(next_step=self.stepShow)
        self.main.remove(prev_step.box)
        self.main.pack_end(self.current_step.box,True,True,0)
        if next:
            self.progressList.next_active()
        else:
            self.progressList.prev_active()
        self.current_step.box.show_all()
        
    def stepShow(self,widget,prev_step,next=True):
        prev_step.validate()
        self.current_step = StepShow(next_step=self.stepExport,prev_step=self.stepFillConfig)
        self.main.remove(prev_step.box)
        self.main.pack_end(self.current_step.box,True,True,0)
        if next:
            self.progressList.next_active()
        else:
            self.progressList.prev_active()
        self.current_step.box.show_all()
        
    def stepExport(self,widget,prev_step,next=True):
        prev_step.validate()
        self.current_step = StepExport(next_step=self.stepFinish,prev_step=self.stepShow)
        self.main.remove(prev_step.box)
        self.main.pack_end(self.current_step.box,True,True,0)
        if next:
            self.progressList.next_active()
        else:
            self.progressList.prev_active()
        self.current_step.box.show_all()

    def stepFinish(self,widget,prev_step,next=True):
        prev_step.validate()
        self.current_step = StepFinish(next_step=self.begin)
        self.main.remove(prev_step.box)
        self.main.pack_end(self.current_step.box,True,True,0)
        if next:
            self.progressList.next_active()
        else:
            self.progressList.prev_active()
        self.current_step.box.show_all()
        
    def begin(self,widget=None):
        Config.clean()
        self.remove(self.main)
        self._begin()
        self.show_all()
        
GLib.threads_init()
window = MainWindow()
Config = rapport.Rapport()
#Gdk.threads_init()
#Gdk.threads_enter()
window.show_all()
Gtk.main()
#Gdk.threads_leave()
