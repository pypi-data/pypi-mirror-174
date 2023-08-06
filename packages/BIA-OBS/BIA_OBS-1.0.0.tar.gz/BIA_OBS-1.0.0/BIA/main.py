#Flask Requirements
from flask import Flask, render_template, request, redirect
import webbrowser
#DateTime 
from datetime import date

#Dict to YAML conversion
import yaml

#Import Path writing
import os.path

# Import DateTime
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def default_route():

    return render_template("home.html")


@app.route("/Componenten")
def componentent_route():
    return render_template("home.html")

@app.route("/submit_data", methods=["POST"])
def submit_route():
    if request.method == "POST":
        form_data={}
        

        #Form creation
        report_name = request.form['naam_bia']
        form_data[f'{report_name}'] = {}

        #Generiek informatie
        form_data[f'{report_name}']['Generieke_Informatie'] = {} 
        form_data[f'{report_name}']['Generieke_Informatie']['aansprakelijk_bia'] = request.form['aansprakelijk_bia']
        form_data[f'{report_name}']['Generieke_Informatie']['coordinator_bia'] = request.form['coordinator_bia']
        form_data[f'{report_name}']['Generieke_Informatie']['startdatum_bia'] = request.form['startdatum_bia']
        form_data[f'{report_name}']['Generieke_Informatie']['einddatum_bia'] = request.form['einddatum_bia']
        
        #Beschrijving Informatie
        form_data[f'{report_name}']['Beschrijving_Informatie'] = {}
        form_data[f'{report_name}']['Beschrijving_Informatie']['beschrijving_bes'] = request.form['beschrijving_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['orgkennis_bes'] = request.form['orgkennis_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['getal_koppelingen_bes'] = request.form['getal_koppelingen_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['koppelingen_bes'] = request.form['koppelingen_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['support_bes'] = request.form['support_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['beveiliging_bes'] = request.form['beveiliging_bes']
        form_data[f'{report_name}']['Beschrijving_Informatie']['aantal_gebruikers_bes'] = request.form['aantal_gebruikers_bes']

        #Scoping  informatie
        form_data[f'{report_name}']['Scoping_Informatie'] = {}
        form_data[f'{report_name}']['Scoping_Informatie']['beschrijving_sco'] = request.form['beschrijving_sco']
        form_data[f'{report_name}']['Scoping_Informatie']['menselijk_risico_sco'] = request.form['menselijk_risico_sco']
        form_data[f'{report_name}']['Scoping_Informatie']['proces_risico_sco'] = request.form['proces_risico_sco']
        form_data[f'{report_name}']['Scoping_Informatie']['tech_risico_sco'] = request.form['tech_risico_sco']
         
        #Belanghebbende  informatie
        form_data[f'{report_name}']['Belanghebbende_Informatie'] = {}
        form_data[f'{report_name}']['Belanghebbende_Informatie']['projectleider_bel'] = request.form['projectleider_bel']
        form_data[f'{report_name}']['Belanghebbende_Informatie']['risicoeigenaar_bel'] = request.form['risicoeigenaar_bel']
        form_data[f'{report_name}']['Belanghebbende_Informatie']['producteigenaar_bel'] = request.form['producteigenaar_bel']
        form_data[f'{report_name}']['Belanghebbende_Informatie']['technischbeheerder_bel'] = request.form['technischbeheerder_bel']
        form_data[f'{report_name}']['Belanghebbende_Informatie']['beveiligingsmanager_bel'] = request.form['beveiligingsmanager_bel']
        form_data[f'{report_name}']['Belanghebbende_Informatie']['contactpunt_bel'] = request.form['contactpunt_bel']
        
       

        #Application Table, could use some work
        #iterate through all values and create new name per 72 entries
        form_data[f'{report_name}']['Applicatie_Table'] = {}
        complete_list = request.form.getlist('app_input')
        name_list = request.form.getlist('app_name')
        #Split list per 72 entries
        composite_list = [complete_list[x:x+72] for x in range(0, len(complete_list),72)]

        i = 0
        for name in name_list:
            print(name)
            form_data[f'{report_name}']['Applicatie_Table'][f'{name}'] = composite_list[i]
            i += 1
        



        #Beschikbaarheidsvereisten Table
        form_data[f'{report_name}']['Beschikbaarheidsvereisten_Table'] = {}
        complete_list = request.form.getlist('bes_input')
        name_list = request.form.getlist('besv_app_name')
        composite_list = [complete_list[x:x+4] for x in range(0, len(complete_list),4)]

        i = 0
        for name in name_list:
            print(name)
            form_data[f'{report_name}']['Beschikbaarheidsvereisten_Table'][f'{name}'] = composite_list[i]
            i += 1


    

        #print(form_data)
        yaml_file = yaml.dump(form_data)
      
        
        # Define Date/Time to use in name string
        now = datetime.now()
        dt_string = str(now.strftime("%d-%m-%Y %Hh%Mm%Ss"))

        directory = './Output/'
        filename = f"{dt_string}.yaml"
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        file.write(yaml_file)
        file.close()
        

    return redirect('/')


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)



# Watch for changes to compile tailwind/flowbite CSS
# npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
