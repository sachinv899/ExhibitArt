import numpy as np
import pandas as pd

from flask import Flask,request,jsonify,render_template
import pickle

application = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))


@application.route('/')
def home():
    areacode =  [' OH', ' WY', ' WA', ' KY', ' PA', ' AL', ' WV', ' CA', ' ND', ' GA', ' DC', ' TX', ' CO', 'A', ' OR', 'D', ' MI', 'F', ' NM', ' AR', ' VT', ' IA', ' MN', ' NH', ' SC', ' OK', ' HI', ' RI', ' LA', ' DE', ' ID', ' CT', ' MS', ' FL', ' VA', ' MA', ' KS', ' ME', ' NC', ' NV', ' MD', ' SD', ' WI', ' MT', ' IL', ' AZ', ' AK', ' NY', ' NJ', ' TN', ' NE', ' MO', ' IN', ' UT']
    return render_template('index.html',predictFlag=True,areacode=areacode)

@application.route('/predict',methods=['POST'])
def predict():
    materialDict = {"Material_Brass": 0, "Material_Clay": 0, "Material_Aluminium": 0, "Material_Wood": 0,
                    "Material_Marble": 0, "Material_Bronze": 0, "Material_Stone": 0}
    areasdisct = {'OH': 0, 'WY': 0, 'WA': 0, 'KY': 0, 'PA': 0, 'AL': 0, 'WV': 0, 'CA': 0, 'ND': 0, 'GA': 0, 'DC': 0,
                  'TX': 0, 'CO': 0, 'A': 0, 'OR': 0, 'D': 0, 'MI': 0, 'F': 0, 'NM': 0, 'AR': 0, 'VT': 0, 'IA': 0,
                  'MN': 0, 'NH': 0, 'SC': 0, 'OK': 0, 'HI': 0, 'RI': 0, 'LA': 0, 'DE': 0, 'ID': 0, 'CT': 0, 'MS': 0,
                  'FL': 0, 'VA': 0, 'MA': 0, 'KS': 0, 'ME': 0, 'NC': 0, 'NV': 0, 'MD': 0, 'SD': 0, 'WI': 0, 'MT': 0,
                  'IL': 0, 'AZ': 0, 'AK': 0, 'NY': 0, 'NJ': 0, 'TN': 0, 'NE': 0, 'MO': 0, 'IN': 0, 'UT': 0}
    binarycolumns={
        'Yes':0,'No':0
    }
    transportdict={
        'Airways':0,'RoadWays':0,'Waterways':0
    }

    '''
    for rendering result in gui
    Artist Name,Artist Reputation,Height,Width,Weight,Material
    '''
    print('Values ',request.form.values())
    if request.method=='POST':
        input_features=[str(x) for x in request.form.values()]
        areacodes = getValues(request,'areacode',areasdisct)
        materials = getValues(request,'material_a',materialDict)
        fragile=getValues(request,'fragile',binarycolumns)
        transport=getValues(request,'transportation',transportdict)
        internationallabel=getValues(request,'International',binarycolumns)
        expressshipmet=getValues(request,'express',binarycolumns)
        installations=getValues(request,'installation',binarycolumns)
        customerinfor=getValues(request,'cutomerinfo',binarycolumns)
        remotelocation=getValues(request,'remoteloc',binarycolumns)

        artistrep=request.form.get('Artist_Reputation')
        height=request.form.get('Height')
        Width=request.form.get('Width')
        weight=request.form.get('Weight')
        pos=request.form.get('Price_Of_Sculpture')
        bsp=request.form.get('Base_Shipping_Price')
        delivery=request.form.get('deliver')
        list = [[artistrep,height,Width,weight,pos,bsp,delivery,0]+materials+internationallabel+expressshipmet+installations+transport+fragile+customerinfor+remotelocation+areacodes]
        print(list)
        predict_cost = model.predict(list)
        print(predict_cost)
        predict_cost = format(predict_cost[0],'.4f')
        return render_template('index.html',predict_cost=predict_cost,predictFlag=False)

    return render_template('index.html')

def getValues(request,inputlabel,inputvalue):
    name = request.form.get(inputlabel)
    inputvalue.update({name:1})
    return list(inputvalue.values())

if __name__=='__main__':
    application.run()

