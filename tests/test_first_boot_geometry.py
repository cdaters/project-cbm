import importlib.util
import unittest
from pathlib import Path
import copy
spec=importlib.util.spec_from_file_location('first_boot',Path(__file__).resolve().parents[1]/'build/pigen/stage-cbm/files/first_boot.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.doc={'partitiontable':{'label':'dos','unit':'sectors','sectorsize':512,'id':'0x12345678','partitions':[
            {'node':'/dev/mmcblk0p1','type':'c','start':2048,'size':1048576},
            {'node':'/dev/mmcblk0p2','type':'83','start':1050624,'size':4194304}]}}
    def test_sd_usb_nvme_and_already_full(self):
        for disk,sep in [('mmcblk0','p'),('sda',''),('nvme0n1','p')]:
            doc=copy.deepcopy(self.doc)
            for index,p in enumerate(doc['partitiontable']['partitions'],1): p['node']=f'/dev/{disk}{sep}{index}'
            size=(1050624+4194304)*512
            self.assertEqual(module.geometry(doc,f'/dev/{disk}{sep}2',size)['free_tail_bytes'],0)
    def test_unsafe_geometry_rejected(self):
        variants=[]
        doc=copy.deepcopy(self.doc);doc['partitiontable']['label']='gpt';variants.append(doc)
        doc=copy.deepcopy(self.doc);doc['partitiontable']['partitions'][1]['start']=4096;variants.append(doc)
        doc=copy.deepcopy(self.doc);doc['partitiontable']['partitions'][1]['type']='8e';variants.append(doc)
        doc=copy.deepcopy(self.doc);doc['partitiontable']['partitions'].reverse();variants.append(doc)
        for doc in variants:
            with self.subTest(doc=doc),self.assertRaises(ValueError): module.geometry(doc,'/dev/mmcblk0p2',8*1024**3)
        with self.assertRaises(ValueError): module.geometry(self.doc,'/dev/mmcblk0p2',1024**3)
