import requests
import json
from django.shortcuts import render
from sendMessage.models import Batch
import pandas as pd
from io import BytesIO
import base64
from django.core.cache import cache
import matplotlib.pyplot as plt
plt.switch_backend('Agg') 

def home(request):

    df = pd.DataFrame(list(Batch.objects.all().values()))    
    df['time'] = pd.to_datetime(df['time'])
    
    # Graph 1
    plt.hist(df['status'], color = 'cyan')    
    plt.xlabel("Message Status")
    plt.ylabel("Frequency")   
    buffer1 = BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    image_png1 = buffer1.getvalue()
    buffer1.close()
    plt.close("all")
    graphic1 = base64.b64encode(image_png1)
    graphic1 = graphic1.decode('utf-8')

    # Graph 2    
    df['time'] = df['time'].dt.date
    plt.scatter(df['status'], df['time'], color = 'green')    
    plt.xlabel("Message Status")
    plt.ylabel("By Date")     
    plt.yticks(rotation=45)
    buffer2 = BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    image_png2 = buffer2.getvalue()
    buffer2.close()
    plt.close("all")
    graphic2 = base64.b64encode(image_png2)
    graphic2 = graphic2.decode('utf-8')


    # Graph 3
    plt.hist(df['statusCode'], color = 'black')   
    plt.xlabel("Message sender status codes")
    plt.ylabel("Frequency")       
    buffer3 = BytesIO()
    plt.savefig(buffer3, format='png')
    buffer3.seek(0)
    image_png3 = buffer3.getvalue()
    buffer3.close()
    plt.close("all")
    graphic3 = base64.b64encode(image_png3)
    graphic3 = graphic3.decode('utf-8')

    # Graph 4    
    plt.scatter(df['mediaType'], df['status'], color = 'chocolate')       
    buffer4 = BytesIO()
    plt.savefig(buffer4, format='png')
    buffer4.seek(0)
    image_png4 = buffer4.getvalue()
    buffer4.close()
    plt.close("all")
    graphic4 = base64.b64encode(image_png4)
    graphic4 = graphic4.decode('utf-8')

    cached_school_data = cache.get('school_data_json')
    if cached_school_data:
        print("----data present in cache----")
        school_data = pd.DataFrame.from_dict(cached_school_data)
    else:
        print("-------no data in cache-------")
        response_API = requests.get('http://127.0.0.1:5000/get-kaggle-data/andrewmvd/us-schools-dataset?select=Private_Schools.csv')
        response_json = response_API.json()

        school_data = pd.DataFrame.from_dict(response_json)
        cache.set('school_data_json', response_json)

    city_school_data = school_data.groupby(["STATE"]).size().reset_index(name='Number of schools')

    #Graph 5
    plt.figure(figsize=(12, 5))
    plt.xlabel("STATE")
    plt.ylabel("Number of schools")   
    plt.bar(city_school_data['STATE'], city_school_data['Number of schools'], color = 'orange')       
    buffer5 = BytesIO()    
    plt.ylim(city_school_data['Number of schools'].min(), city_school_data['Number of schools'].max())
    plt.xticks(rotation='vertical')
    plt.savefig(buffer5, format='png')
    buffer5.seek(0)
    image_png5 = buffer5.getvalue()
    buffer5.close()
    plt.close("all")
    graphic5 = base64.b64encode(image_png5)
    graphic5 = graphic5.decode('utf-8')

    #Graph 6
    state_population_data = school_data.groupby(['LEVEL_']).size().reset_index(name='Population')
    colors = ['lightskyblue', 'red', 'lightcoral']
    plt.pie(state_population_data['Population'], labels = state_population_data['LEVEL_'], colors=colors)  
    plt.title("Schools in each Level all over the country")   
    buffer6 = BytesIO()    
    plt.savefig(buffer6, format='png')
    buffer6.seek(0)
    image_png6 = buffer6.getvalue()
    buffer6.close()
    plt.close("all")
    graphic6 = base64.b64encode(image_png6)
    graphic6 = graphic6.decode('utf-8')

    #Graph 7
    multiline_graph = school_data[['NAME', 'START_GRAD', 'END_GRADE']][:5]
    # multiline_graph = multiline_graph.astype(int)
    plt.figure(figsize=(12, 10)) 
    plt.plot(multiline_graph['NAME'], multiline_graph['START_GRAD'], label = "Start Grade", marker="o")
    plt.xlabel("School ID")
    plt.ylabel("Start and End Grade Range") 
    plt.plot(multiline_graph['NAME'], multiline_graph['END_GRADE'], label = "End Grade", marker="o")
    plt.legend()
    plt.title("Top 5 schools start and end grade range")  
    plt.xticks(rotation=35)
    buffer7 = BytesIO()    
    plt.savefig(buffer7, format='png')
    buffer7.seek(0)
    image_png7 = buffer7.getvalue()
    buffer7.close()
    plt.close("all")
    graphic7 = base64.b64encode(image_png7)
    graphic7 = graphic7.decode('utf-8')

    #Graph 8
    method_data = school_data[:100]
    method_data = method_data.groupby(['TEACHER_CODE']).size().reset_index(name='Frequency of TEACHER_CODE')
    print(method_data)
    plt.hist(method_data['TEACHER_CODE'], color = "lightblue", ec="black")    
    plt.xlabel("TEACHER_CODE")
    plt.ylabel("Frequency")   
    buffer8 = BytesIO()
    plt.savefig(buffer8, format='png')
    buffer8.seek(0)
    image_png8 = buffer8.getvalue()
    buffer8.close()
    plt.close("all")
    graphic8 = base64.b64encode(image_png8)
    graphic8 = graphic8.decode('utf-8')

    return render(request, 'index.html', {'graphic1':graphic1, 'graphic2':graphic2, 'graphic3':graphic3, 'graphic4':graphic4, 'graphic5':graphic5, 'graphic6':graphic6, 'graphic7':graphic7, 'graphic8':graphic8})




    