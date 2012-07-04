try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
from math import pow
import subprocess
import thread
import time
import htmlTemplate

if __name__ == "__main__":
    _THREAD_LIST = list()

File_path = "/tmp/rawxml"

class InformationMissing(Exception):
    pass

class Donnee:
    def __init__(self, name, fnct, optional=True, editable=True):
        self.name = name
        self.fnct = fnct
        self.optional = optional
        self.editable = editable
        
infos = list()
#infos.append(Donnee("Catégorie de l'ordinateur", "get_computer_type"))
infos.append(Donnee("Vitesse du processeur", "get_cpu_speed"))
infos.append(Donnee("Architecture du processeur", "get_cpu_bits"))
infos.append(Donnee("Description du processeur", "get_cpu_detail"))
infos.append(Donnee("Capacité de la mémoire vive", "get_memory_size"))
infos.append(Donnee("Détail de la mémoire vive", "get_memory_detail"))
infos.append(Donnee("Capacité totale de stockage", "get_disk_size"))
infos.append(Donnee("Détails des disques durs", "get_disk_detail"))
infos.append(Donnee("Carte mère", "get_mothercard_detail"))
infos.append(Donnee("Carte(s) graphique(s)", "get_video_detail"))
infos.append(Donnee("Carte(s) son(s)", "get_multimedia_detail"))
infos.append(Donnee("Ports USB", "get_usb_detail"))
infos.append(Donnee("Numéro de série", "get_serial_number", optional=False))




class RapportThread(thread.Thread):
    def __init__(self,parent,on_finish=None,progress=None):
        thread.Thread.__init__(self)
        self.on_finish = on_finish
        self.parent = parent
        self.progress = progress
        
    def run(self):
      self.parent.thread_return = None
      self.parent.thread_return = self.parent.make_rapport(self.progress)
      if self.on_finish is not None:
        self.on_finish()
        
    def stop(self):
        del self
        
class GenerateXmlThread(thread.Thread):
    def __init__(self,parent,on_finish=None):
        thread.Thread.__init__(self)
        self.on_finish = on_finish
        self.parent = parent
        
    def run(self):
      self.parent.thread_return = None
      self.parent.thread_return = self.parent._genxml()
      if self.on_finish is not None:
        self.on_finish()

class Rapport:
    def __init__(self):
        self.missing = list()
        self.critic = list()
        self.data = dict()
    
    def transform_unit(self, capacity, base=10):
        if base == 10:
            n = 3
        elif base == 2:
            n = 10
        units = ['k', 'M', 'G', 'T']
        unit = ""
        capacity = float(capacity)
        for i in range(4):
            if (capacity / (pow(base, (4 - i) * n))) > 1:
                unit = units[3 - i]
                capacity /= (pow(base, (4 - i) * n))
                break
        return str(int(capacity * 10) / 10) + " " + unit
    
    def get_computer_type(self):
        base = self.path["core"]["node"]
        try:
            type = base.findall('chassis')[0]
        except IndexError:
            raise InformationMissing()
        if type == "notebook":
            return "Ordinateur Portable"
        else:
            return "Ordinateur de Bureau"
        
    def get_cpu_speed(self):
        code,speed = subprocess.getstatusoutput("cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq")
        speed = [int(elem)*1000 for elem in speed.split("\n")]
        if code != 0:
            code,speed = subprocess.getstatusoutput("cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies |cut -d\   -f 1")
            speed = [int(elem)*1000 for elem in speed.split("\n")]
            if code != 0:
                raise InformationMissing()
        return self.transform_unit(sum(speed)/len(speed))+"Hz"
    
    def get_cpu_bits(self):
        cpu = self.path["core"]["cpu"]["node"]
        try:
          bits = cpu.findall('width')[0]
        except IndexError:
          raise InformationMissing()
        return bits.text + " " + bits.attrib["units"]
    
    def get_cpu_detail(self):
        cpu = self.path["core"]["cpu"]["node"]
        try:
          return cpu.findall('product')[0].text
        except IndexError:
          raise InformationMissing()
    
    def get_memory_size(self):
        memory = self.path["core"]["memory"]["node"]
        try:
          size = memory.findall("size")[0]
        except IndexError:
          raise InformationMissing()
        return self.transform_unit(size.text, 2) + "o"
    
    def get_memory_detail(self):
        memory = self.path["core"]["memory"]
        i = 0
        slots = list()
        while True:
            try:
                slot = memory["bank:" + str(i * 2)]["node"].findall("description")[0]
            except KeyError:
                break
            slots.append(slot.text)
            i += 1
        if len(slots) == 0:
          raise InformationMissing()
        return slots
    
    def get_disk_size(self):
        disks = self.path["core"]["pci"]["storage"]
        i = 0
        size = 0
        for key,disk in disks.items():
            if key != "node" and key != "cdrom" and key != "floppy":
                size += int(disk["node"].findall("size")[0].text)
        if size == 0:
          raise InformationMissing()
        return self.transform_unit(size, base=2) + "o"
    
    def _arch_get_disk_size(self):
        disks = self.path["core"]
        i = 0
        size = 0
        while True:
            try:
                disk = disks["scsi:" + str(i)]["disk"]["node"].findall("size")[0]
            except KeyError:
                try:
                    if "cdrom" in disks["scsi:" + str(i)].keys() or "floppy" in disks["scsi:" + str(i)].keys():
                        i += 1
                        continue
                    else:
                        break
                except KeyError:
                    break
            size += int(disk.text)
            i += 1
        if size == 0:
          raise InformationMissing()
        return self.transform_unit(size, base=2) + "o"
    
    def get_disk_detail(self):
        disks = self.path["core"]["pci"]["storage"]
        i = 0
        detail = list()
        for key,disk in disks.items():
            if key != "node" and key != "cdrom" and key != "floppy":
                disk_prod = disk["node"].findall("product")[0].text
                disk_vendor = disk["node"].findall("vendor")[0].text
                disk_size = disk["node"].findall("size")[0].text
                detail.append(disk_vendor + " " + disk_prod + " : " + self.transform_unit(disk_size, base=2) + "o")
        if len(detail) == 0:
          raise InformationMissing()
        return detail
            
    def _arch_get_disk_detail(self):
        disks = self.path["core"]
        i = 0
        detail = list()
        while True:
            try:
                disk_prod = disks["scsi:" + str(i)]["disk"]["node"].findall("product")[0].text
                disk_vendor = disks["scsi:" + str(i)]["disk"]["node"].findall("vendor")[0].text
                disk_size = disks["scsi:" + str(i)]["disk"]["node"].findall("size")[0].text
                detail.append(disk_vendor + " " + disk_prod + " : " + self.transform_unit(disk_size, base=2) + "o")
            except KeyError:
                try:
                    if "cdrom" in disks["scsi:" + str(i)].keys() or "floppy" in disks["scsi:" + str(i)].keys():
                        i += 1
                        continue
                    else:
                        break
                except KeyError:
                    break
            i += 1
        if len(detail) == 0:
          raise InformationMissing()
        return detail
            
    def get_mothercard_detail(self):
        mc = self.path["core"]["node"]
        try:
          prod = mc.findall("product")[0].text
          vendor = mc.findall("vendor")[0].text
        except IndexError:
          raise InformationMissing()
        return vendor + " " + prod
    
    def get_usb_detail(self):
        usbs = str(subprocess.check_output("lsusb"))
        usbs = usbs.split("\\n")
        usb_n = [0, 0, 0]
        for usb in usbs:
            if "root hub" in usb:
                if "Linux Foundation 1." in usb:
                    usb_n[0] += 1
                elif "Linux Foundation 2." in usb:
                    usb_n[1] += 1
                elif "Linux Foundation 3." in usb:
                    usb_n[2] += 1
        final = ""
        i = 1
        for usb in usb_n:
            if usb > 0:
                final += str(usb) + "x USB-" + str(i) + ", "
            i += 1
        return final[:-2]
    
    def get_video_detail(self):
        cards = self.explore(self.path["core"]["pci"], "display")
        videos = list()
        for card in cards:
            if card["node"].attrib["class"] == "display":
                prod = card["node"].findall("product")[0].text
                vendor = card["node"].findall("vendor")[0].text
                videos.append(vendor + " " + prod)
        if len(videos) == 0:
          raise InformationMissing()
        return videos
    
    def get_multimedia_detail(self):
        cards = self.explore(self.path["core"]["pci"], "multimedia")
        multimedia = list()
        for card in cards:
            if card["node"].attrib["class"] == "multimedia":
                prod = card["node"].findall("product")[0].text
                vendor = card["node"].findall("vendor")[0].text
                multimedia.append(vendor + " " + prod)
        if len(multimedia) == 0:
          raise InformationMissing()
        return multimedia
      
    def get_serial_number(self):
      raise InformationMissing()
    
    def explore(self, dictio, search, found=[]):
        for key, value in dictio.items():
            if key == search:
                found.append(value)
            elif type(value) == dict:
                self.explore(value, search, found)
        return found
    
    def getin(self, elem):
        path = dict()
        for node in elem.findall('node'):
            path[node.attrib["id"]] = dict()
            path[node.attrib["id"]]["node"] = node
            path[node.attrib["id"]].update(self.getin(node))
        return path
            
    def make_rapport(self,progress=None):
        step_len = float(1/len(infos))
        step = 0
        for info in infos:
            step+=step_len
            if progress is not None:
                progress([step,info.name])
            try:
                tmp = eval("self." + info.fnct + "()")
                self.data[info.fnct] = tmp
            except InformationMissing:
                if not info.optional:
                  if info.editable:
                    self.critic.append(info)
                  else:
                    print("Missing critical : "+info.name)
                    return False
                else:
                  if info.editable:
                    self.missing.append(info)
                  else:
                    self.data[info.fnct] = ""
            time.sleep(0.2)
        return True
        
    def _genxml(self):
      self.xml = subprocess.check_output(["lshw","-xml"])
        
    def generate_xml_data(self,on_finish=None):
      thread = GenerateXmlThread(self,on_finish)
      thread.start()
      
    def make(self,on_finish=None,progress=None):
      self.root = etree.fromstring(self.xml)
      #start = self.root.findall('node')[0]
      start = self.root
      self.path = self.getin(start)
      if "core" not in self.path.keys():
        for key in self.path.keys():
          if key != "node":
            node = key
          print(node)
      #self.path["core"] = self.path[node]["core"]
      thread = RapportThread(self,on_finish,progress)
      thread.start()
      
    def _make(self):
        self.root = etree.fromstring(self.xml)
        start = self.root.findall('node')[0]
        self.path = self.getin(start)
        self.make_rapport()
      
    def create_html(self):
        self.html = ""
        self.html += htmlTemplate.head
        self.html += htmlTemplate.gen_top(self.data)
        self.html += htmlTemplate.first_transition
        self.html += htmlTemplate.gen_resume(self.data)
        self.html += htmlTemplate.second_transition
        self.html += htmlTemplate.gen_detail(self.data)
        self.html += htmlTemplate.feet
        return self.html
    
    def clean(self):
        self = Rapport()

if __name__ == '__main__':
    rap = Rapport()
    rap._genxml()
    rap._make()
    print(rap.create_html())
