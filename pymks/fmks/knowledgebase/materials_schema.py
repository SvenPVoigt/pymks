from pydantic import BaseModel, Field, AnyHttpUrl
from uuid import UUID
from typing import Union, Dict, List, Set, Optional
from datetime import date, datetime, time, timedelta

import requests
import json

# from cordrapy import Objects


class CordraModel(BaseModel):
    u0040id: str = ""
    host: str = 'https://api.materialhub.org'
    token: str = ""

    def getid(self, tryagain=0, tryagainmax=0):
        data = self.json()
        r = requests.post(
            self.host + '/objects/?type=%s'%self.className,
            data=data,
            headers={
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json'
            },
            verify=False
        )

        if r.status_code == 200:
            self.u0040id = r.json()['@id']
        elif tryagain < tryagainmax:
            self.getid(tryagain+1, tryagainmax)
        else:
            print('Could not obtain an id, but no error in connecting')


    def loadbyid(self, id):
        r = requests.get(
            self.host + '/objects/%s'%id,
            headers={
                'Authorization': 'Bearer ' + self.token
            },
            verify=False
        )

        print(r.text)

        if r.status_code == 200:
            self.parse_obj(
                json.loads(
                    r.text.replace('@', 'u0040')
                )
            )
        else:
            print('Failed to load by id')


class ProcessGraphNode(CordraModel):
    name: str = ""



class Process(ProcessGraphNode):
    className: str = 'Process'
    prv: 'Material' = Field(None)
    nxt: 'Material' = Field(None)
    workExample: UUID = Field(None)
    supply: UUID = Field(None)
    # characterized_by: 'Experiment' = Field(None)
    # composed_of: 'Material' = Field(None)


class Material(ProcessGraphNode):
    className: str = 'Material'
    prv: 'Process' = Field(None)
    nxt: 'Process' = Field(None)
    supplyFor: UUID = Field(None)
    exampleOfWork: UUID = Field(None)
    # characterized_by: 'Experiment' = Field(None)
    # composed_of: 'Material' = Field(None)
