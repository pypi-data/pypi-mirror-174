from django.core.management.base import BaseCommand, CommandError
        
import pandas as pd
import itertools as it
from collections import defaultdict, Counter
import json
from dubletten_tool.models import  Group, Ampel
from apis_core.apis_entities.models import Person
from apis_core.apis_metainfo.models import Collection
import logging
from django.contrib.auth.models import User
from dubletten_tool.logger import init_logger

from apis_core.apis_entities.models import Person
from apis_core.apis_labels.models import LabelType, Label
from apis_core.apis_metainfo.models import Collection
from apis_core.apis_vocabularies.models import PersonPersonRelation
from apis_core.apis_relations.models import PersonPerson, AbstractRelation


log = logging.getLogger("DBLogger")

user = User.objects.get(username="GPirgie")

class MergeGroup:
    merged_col, c = Collection.objects.get_or_create(name="Vorfinale Einträge")
    rt_vorfin, c = PersonPersonRelation.objects.get_or_create(name="data merged from", name_reverse="merged into")
    lt_group, c = LabelType.objects.get_or_create(name="Result of deduplication Group")
    lt_first_name_alt, c = LabelType.objects.get_or_create(name="alternativer Vorname")
    lt_name_alt, c = LabelType.objects.get_or_create(name="alternativer Nachname")
    lt_sd_alt, c = LabelType.objects.get_or_create(name="alternatives Geburtsdatum")
    lt_ed_alt, c = LabelType.objects.get_or_create(name="alternatives Sterbedatum")
    
    rels = ["PersonInstitution", "PersonPlace", "PersonEvent", "PersonWork"] # Handle seperately:, "PersonPerson"]
    
    def __init__(self, group, create=False):
        self.group = group
        self.members = [m.person for m in group.members.all()]
        self.meta = {"name":self.members[0].name, "first_name":self.members[0].first_name, "gender":self.group.gender}
        self.create = create
        #self.additional_labels = []

    def process_names(self):
        for m in self.members[1:]:
            self.labels[MergeGroup.lt_first_name_alt].add(m.first_name)
            self.labels[MergeGroup.lt_name_alt].add(m.name)

    def process_birth_and_death(self):
        start_dates = set()
        end_dates = set()
        alt_start, alt_end = None, None
        for m in self.members:
            if m.start_date_written:
                start_dates.add(m.start_date_written)
            if m.end_date_written:
                end_dates.add(m.end_date_written)

        start_dates = list(start_dates)
        end_dates = list(end_dates)
        
        if start_dates:
            if len(start_dates) == 1:
                start_date = start_dates[0]
            else:
                start_date = start_dates[0]
                alt_start = start_dates[1:]

            #  start_date, *alt_start = [start_dates]
                
        else:
            start_date = None
            
        if end_dates:
            if len(end_dates) == 1:
                end_date = end_dates[0]
            else:
                end_date = end_dates[0]
                alt_end = end_dates[1:]
        else:
            end_date = None
            
        self.meta.update({"start_date_written":start_date, "end_date_written":end_date})


        # todo: create labels from alternative start and end date lists
        if alt_start:
            for sd in alt_start:
                self.labels[MergeGroup.lt_sd_alt].add(sd)
        if alt_end:
            for ed in alt_end:
                self.labels[MergeGroup.lt_ed_alt].add(ed)

            #self.additional_labels.append(label_type=MergeGroup.lt_ed_alt, label=ed)

            
    def process_labels(self):
        labels = defaultdict(set)
        for m in self.members:
            [labels[el.label_type].add(el.label.strip()) for el in m.label_set.all()]
 
        return labels

    def process_personinstitution(self):
        pass

    def process_all_other_relations(self):
        # todo: alle relations deduplizieren
        for m in self.members:
            for r in MergeGroup.rels:
                if r != "PersonPerson":
                    temp = getattr(m, r.lower()+"_set").values()
                    model = AbstractRelation.get_relation_class_of_name(r)
                    print(temp)
                    for t in temp:
                        t.pop("related_person_id")
                        t.pop("tempentityclass_ptr_id")
                        t.pop("id")
                        t["related_person"] = self.person
                        print(t)
                        model.objects.get_or_create(**t)
                elif r == "PersonPerson":
                    #for d in ["personA_set", "personB_set"]:
                    tempA = m.personA_set.values()
                    tempB = m.personB_set.values()
                    model = AbstractRelation.get_relation_class_of_name("PersonPerson")
                    for t in tempA:
                        t.pop("related_personA_id")
                        t.pop("tempentityclass_ptr_id")
                        t.pop("id")
                        t["related_personA"] = self.person
                        print(t)
                        model.objects.get_or_create(**t)
                    for t in tempB:
                        t.pop("related_personB_id")
                        t.pop("tempentityclass_ptr_id")
                        t.pop("id")
                        t["related_personB"] = self.person
                        print(t)
                        model.objects.get_or_create(**t)
                    

    def process_titles(self):
        titels = set()
        for m in self.members:
            [titels.add(t) for t in m.title.all()]
            
        return titels

    def process_notes(self):
        notes = ""
        for m in self.members:
            if m.notes:
                notes += f"[{m.pk}: {m.notes}]\n"
        return notes
    
    def process_references(self):
        refs = ""
        for m in self.members:
            if m.references:
                refs += f"[{m.pk}: {m.references}]\n"
        return refs

    def process_uris(self):
        #nicht nötig
        pass

    def process_collections(self):
        # nicht nötig
        pass


  
    def run_process(self):
        self.labels = self.process_labels()
        self.process_names()
        self.process_birth_and_death()

        titels = self.process_titles()
        notes = self.process_notes()
        refs = self.process_references()
        self.meta.update({"notes":notes, "references":refs})
        per = Person.objects.create(**self.meta)
        per.collection.add(MergeGroup.merged_col)
        # create Ampel
        ampel = Ampel.objects.create(person=per, status="red", note=self.group.note)
        ampel.save()
        
        #todo: handle start and end dates of labels as tuples
        for key, vals in self.labels.items():
            for v in vals:
                lab, created = Label.objects.get_or_create(label=v, label_type=key, temp_entity=per)
                #per.label_set.add(lab)
        for m in self.members:
            PersonPerson.objects.get_or_create(related_personA=per, related_personB=m, relation_type=MergeGroup.rt_vorfin)
        
        Label.objects.get_or_create(label=f"{self.group.name} ({self.group.id})", label_type=MergeGroup.lt_group, temp_entity=per)
        self.person = per
        self.process_all_other_relations()
        #print("Notes:", notes, "refs:", refs)
        

class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        merged, c = Collection.objects.get_or_create(name="Vorfinale Einträge")
        merged.tempentityclass_set.all().delete()

        gg = Group.objects.all()
        for g in gg:
            MergeGroup(g).run_process()