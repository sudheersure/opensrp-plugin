from django.shortcuts import render
from Masters.models import *
from django.http import HttpResponse
import json
from collections import defaultdict
import time
from datetime import date, timedelta
import datetime
from django.shortcuts import render_to_response
from Masters.forms import *
from django.core.context_processors import csrf

def doc_data(request):
    result = []
    if request.method == 'GET':
        doc = str(request.GET.get('id',''))
        doc_data = DimDoctorForm.objects.filter(doctoridentifier=str(doc)).values_list('form','id')
        for data in doc_data:
            temp = {}
            temp['id']=data[1]
            temp['form_data']=data[0]
            result.append(temp)
        doc_data = json.dumps(result)
        return doc_data


def get_drugdata(request):
    all_info=defaultdict(list)
    drug_details = DrugInfo.objects.all().values_list('drug_name','frequency','dosage__dosage','direction__directions')
    for drug in drug_details:
        drug_data = {}
        drug_data['name']=drug[0]
        drug_data['frequency'] = int(drug[1])
        drug_data['dosage']=drug[2]
        drug_data['direction']=drug[3]
        all_info['drug_data'].append(drug_data)
    diagnosis = ICD10.objects.filter(can_select='True',status='True').values_list('ICD10_Chapter','ICD10_Code','ICD10_Name')
    for d in diagnosis:
        diagnosis_data={}
        diagnosis_data['ICD10_Chapter']=d[0]
        diagnosis_data['ICD10_Code']=d[1]
        diagnosis_data['ICD10_Name']=d[2]
        all_info['diagnosis_data'].append(diagnosis_data)
    investigation_info = Investigations.objects.filter(is_active=True).values_list('service_group_name','investigation_name')
    for investigation in investigation_info:
        investigation_data = {}
        investigation_data['service_group_name'] = investigation[0]
        investigation_data['investigation_name'] = investigation[1]
        all_info['investigation_data'].append(investigation_data)
    result_json = json.dumps(all_info)
    return HttpResponse(result_json)

def poc_update(request):
    if request.method =="GET":
        document_id=request.GET.get("docid","")
        poc_info=request.GET.get("pocinfo","")
        visitid=request.GET.get("visitid","")
        entityid=request.GET.get("entityid","")
        docid=request.GET.get("doctorid","")
        pending =request.GET.get("pending","")

    elif request.method =="POST":
        document_id=request.POST.get("docid","")
        poc_info=request.POST.get("pocinfo","")
        visitid=request.POST.get("visitid","")
        entityid=request.POST.get("entityid","")
        docid=request.POST.get("doctorid","")
        pending =request.POST.get("pending","")
    poc = []
    poc_data = {}
    poc_data['pending']=pending
    poc_data['poc'] = str(poc_info)
    poc.append(poc_data)
    poc_backup = json.dumps(poc)

    #Adding poc and related doctor to backup table helpful for history
    add_poc_backup = PocBackup(visitentityid=str(visit_info[0][0]),entityidec=str(visit_info[0][1]),docid=str(docid),poc=poc_backup)
    add_poc_backup.save()

    #Getting old poc value give to patient
    visit_backup = PocBackup.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).values_list('poc','id')
    if len(visit_backup)>0:
    	for visit in visit_backup:
            old_poc= json.loads(visit[0][0])
            poc.append(old_poc)

    #Reading all values from document
    result = {}
    entity_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_id/?key=%22"+str(document_id)+"%22"
    poc_output=commands.getoutput(entity_detail)
    poutput=json.loads(poc_output)
    form_ins= poutput['rows'][0]['value'][2]
    row_data = poutput['rows'][0]['value'][2]['formInstance']['form']['fields']
    #Updating docPocInfo with pending reason or poc
    for i in range((len(row_data))):
        row = row_data[i]
        if 'name' in row.keys():
            if str(row['name']) == 'docPocInfo':
                old_poc = json.loads(row['value'])
                if len(old_poc)==0:
                    poc_json = json.dumps(poc)
                    row['value']=poc_json
                    row_data[i]=row
    #Creating new document with latest docPocInfo
    result["_id"]=str(form_ins["_id"])
    result["_rev"]=str(form_ins["_rev"])
    result["anmId"]=str(form_ins["anmId"])
    result["clientVersion"]=str(form_ins["clientVersion"])
    result["entityId"]=str(form_ins["entityId"])
    result["formDataDefinitionVersion"]=str(form_ins["formDataDefinitionVersion"])
    result["formInstance"]=form_ins["formInstance"]
    result["formName"]=str(form_ins["formName"])
    result["instanceId"]=str(form_ins["instanceId"])
    result["serverVersion"]=int(round(time.time() * 1000))
    result["type"]=str(form_ins["type"])
    ord_result = json.dumps(result)
    poc_doc_update_curl = "curl -vX PUT http://202.153.34.169:5984/drishti-form/%s -d '''%s'''" %(str(document_id),ord_result)
    poc_doc_update=commands.getoutput(poc_doc_update_curl)

    if len(pending)>0:
        update_poc=PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).update(pending=str(pending),docid=str(docid))

    #Updating backup table with latest poc/pending status info
    visit_info = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).values_list('visitentityid','entityidec')
    if len(pending)==0:
        #Removing record provided POC
        del_poc = PocInfo.objects.filter(visitentityid=str(visitid),entityidec=str(entityid)).delete()
    return HttpResponse(json.dumps({"status":"success"}))


def doctor_data(request):
    ''' Method to show all pending cases on doctor home screen with patient details'''
    if request.method == "GET":
        doc_name= request.GET.get('docname',"")
        password = request.GET.get('pwd',"")
    elif request.method == "POST":
        doc_name= request.GET.get('docname',"")
        password = request.GET.get('pwd',"")
    end_res = '{}'
    doc_phc = str(DocInfo.objects.filter(docname=str(doc_name)).values_list('phc__name')[0][0])
    doc_pwd = hashlib.sha1()
    doc_pwd.update(password)
    doc_password = doc_pwd.hexdigest()
    user_pwd_db = DimUserLogin.objects.filter(name=str(doc_name)).values_list('password')
    resultdata=defaultdict(list)
    display_result=[]
    entity_list = PocInfo.objects.filter(phc=doc_phc).values_list('visitentityid','entityidec','pending','docid').distinct()

    #If no record availble for doctor screen display
    if len(entity_list) == 0:
    	return HttpResponse(json.dumps(display_result))

    #Iterating all pending cases to display over doctor home screen
    for entity in entity_list:
        if str(entity[2])!='None':
            if len(entity[2])>1 and str(doc_name) != str(entity[3]):
                continue
    	entity_detail_id=str(entity[1])
        #Curl command to read visit related data
        ancvisit_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+str(entity[0])+"%22"
        visit_output = commands.getoutput(ancvisit_detail)
        visit_data1 = json.loads(visit_output)
        row = visit_data1['rows']
        visit_data=[]
        poc_len=1
        doc_con='no'
        for i in range(len(row)):
            visit={}
            newvisitdata=defaultdict(list)
            newvisit={}
            field_data = row[i]['value'][1]['form']['fields']
            for f in range((len(field_data)-1),-1,-1):
                fd = field_data[f]
                if 'name' in fd.keys():
                    if fd['name'] == 'docPocInfo':
                        poc_len=len(fd['value'])
                    elif fd['name'] == 'isConsultDoctor':
                        doc_con = fd['value']
            #Check if record is recommended for doctor consultation
            if doc_con == 'yes':
                #-----------------PNC DATA --------------
                if row[i]['value'][0] == 'pnc_visit':
                    doc_id=row[i]['id']
                    for visitdata in row[i]['value'][1]['form']['fields']:
                        key = visitdata.get('name')
                        if 'value' in visitdata.keys(): 
                            value = visitdata.get('value')
                        else:
                        	value=''
                        if key == 'pncNumber':
                            visit['pncNumber']=value
                        elif key=='pncVisitDate':
                            visit['pncVisitDate']=value
                        elif key == 'difficulties1':
                            visit['difficulties1']=value
                        elif key == 'difficulties2':
                            visit['difficulties2']=value
                        elif key == 'abdominalProblems':
                            visit['abdominalProblems']=value
                        elif key == 'urineStoolProblems':
                            visit['urineStoolProblems']=value
                        elif key == 'hasFeverSymptoms':
                            visit['hasFeverSymptoms']=value    
                        elif key == 'breastProblems':
                            visit['breastProblems']=value
                        elif key == 'vaginalProblems':
                            visit['vaginalProblems']=value
                        elif key == 'bpSystolic':
                            visit['bpSystolic']=value
                        elif key == 'bpDiastolic':
                            visit['bpDiastolic']=value
                        elif key == 'temperature':
                            visit['temperature']=value
                        elif key == 'pulseRate':
                            visit['pulseRate']=value
                        elif key == 'bloodGlucoseData':
                            visit['bloodGlucoseData']=value
                        elif key == 'weight':
                            visit['weight']=value
                        elif key == 'pncVisitPlace':
                        	visit['pncVisitPlace']=value
                        elif key == 'pncVisitDate':
                        	visit['pncVisitDate']=value                        	
                        elif key == 'isHighRisk':
                        	visit['isHighRisk']=value
                        elif key == 'hbLevel':
                            visit['Hblevel']=value
                            visit['visit_type'] = 'PNC'
                        visit["entityid"] = entity[0]
                        visit['id']=doc_id 
                    visit_data.append(visit)

                elif row[i]['value'][0] == 'anc_visit': 
                    doc_id=row[i]['id']
                    for visitdata in row[i]['value'][1]['form']['fields']:
                        key = visitdata.get('name') 
                        if 'value' in visitdata.keys(): 
                            value = visitdata.get('value')
                        else:
                        	value=''
                        if key == 'ancVisitNumber':
                            visit['ancVisitNumber']=value
                        elif key == 'ancNumber':
                            visit['ancNumber']=value                            
                        elif key == 'ancVisitPerson':
                            visit['ancVisitPerson']=value
                        elif key=='ancVisitDate':
                            visit['ancVisitDate']=value
                        elif key == 'riskObservedDuringANC':
                            visit['riskObservedDuringANC']=value
                        elif key == 'bpSystolic':
                            visit['bpSystolic']=value
                        elif key == 'bpDiastolic':
                            visit['bpDiastolic']=value
                        elif key == 'temperature':
                            visit['temperature']=value
                        elif key == 'pulseRate':
                            visit['pulseRate']=value
                        elif key == 'bloodGlucoseData':
                            visit['bloodGlucoseData']=value
                        elif key == 'weight':
                            visit['weight']=value
                        elif key == 'fetalData':
                            visit['fetalData']=value
                            visit['visit_type'] = 'ANC'
                        visit["entityid"] = entity[0]
                        visit['id']=doc_id   
                    visit_data.append(visit)
                elif row[i]['value'][0] == 'child_illness':
                    doc_id=row[i]['id']
                    for childdata in row[i]['value'][1]['form']['fields']:
                        key = childdata.get('name') 
                        if 'value' in childdata.keys(): 
                            value = childdata.get('value')
                        else:
                        	value=''
                        if key =='dateOfBirth':
                        	visit['dateOfBirth']=value
                        	age = datetime.datetime.today()-datetime.datetime.strptime(str(value),"%Y-%m-%d")
                        	visit['age']=age.days
                        	visit['visit_type'] = 'CHILD'
                        elif key == 'childSigns':
                        	visit['childSigns']=value
                        elif key =='childSignsOther':
                        	visit['childSignsOther']=value
                        elif key =='immediateReferral':
                        	visit['immediateReferral']=value
                        elif key =='immediateReferralReason':
                        	visit['immediateReferralReason']=value
                        elif key =='reportChildDisease':
                        	visit['reportChildDisease']=value
                        elif key =='reportChildDiseaseOther':
                        	visit['reportChildDiseaseOther']=value
                        elif key =='reportChildDiseaseDate':
                        	visit['reportChildDiseaseDate']=value
                        elif key =='reportChildDiseasePlace':
                        	visit['reportChildDiseasePlace']=value
                        elif key =='numberOfORSGiven':
                        	visit['numberOfORSGiven']=value
                        elif key =='childReferral':
                        	visit['childReferral']=value
                        elif key =='submissionDate':
                        	visit['submissionDate']=value
                        elif key == 'id':
                        	visit['id']=doc_id
                        	visit["entityid"] = entity[0]
                    visit_data.append(visit)
        #CURL command to read registration related info
        entity_detail="curl -s -H -X GET http://202.153.34.169:5984/drishti-form/_design/FormSubmission/_view/by_EntityId?key=%22"+entity_detail_id+"%22"
        poc_output=commands.getoutput(entity_detail)
        poutput=json.loads(poc_output)
        row1 = poutput['rows']
        if len(visit_data)>0 and len(row1)>0:
            result=defaultdict(list)
            for data in row1[0]["value"][1]['form']['fields']:
                key=data.get('name')
                value=data.get('value')
                if key=='wifeName':
                    temp={}
                    temp={key:value}
                    result.update(temp)
                elif key=='wifeAge':
                    temp={}
                    temp={key:value}
                    result.update(temp)
                elif key=='district':
                    temp={}
                    temp={key:value}
                    result.update(temp)
                elif key=='husbandName':
                    temp={}
                    temp={key:value}
                    result.update(temp)
                elif key=='village':
                    temp={}
                    temp={key:value}
                    result.update(temp)
                elif key == 'aadharNumber':
                    temp={}
                    temp={key:value}
                    result.update(temp)
            if row1[0]['value'][0] == "anc_registration_oa" or row1[0]['value'][0]=="anc_registration":
                for data in row1[0]["value"][1]['form']['fields']:
                    key=data.get('name')
                    value=data.get('value')
                    if key=='edd':
                        temp={}
                        temp={key:value}
                        visit['edd']=value
            elif row1[0]['value'][0] == "child_registration_oa":
            	for child_data in row1[0]["value"][1]['form']['fields']:
                    key = child_data.get('name') 
                    if 'value' in child_data.keys(): 
                        value = child_data.get('value')
                    else:
                        value=''
                    if key == 'gender':
                        visit['gender']=value
                    elif key == 'name':
                        visit['name']=value
                    elif key == 'registrationDate':
                        visit['registrationDate']=value
                    elif key =='edd':
                    	visit['edd']=value
                    elif key == 'motherName':
                        temp={}
                        temp={key:value}
                        result.update(temp)
                    elif key == 'fatherName':
                        temp={}
                        temp={key:value}
                        result.update(temp)
            temp_list=[]
            temp_list.append(visit_data[-1])
            result["riskinfo"]=temp_list
            result["entityidec"] = entity_detail_id
            result["anmId"] = row1[0]['value'][2]
            display_result.append(result)
        end_res= json.dumps(display_result)
    return HttpResponse(end_res)

def admin_hospital(request):
    hosname = HospitalDetails.objects.all().values_list('hospital_name')
    hos_name=[]
    for x in hosname:
        hos_name.append(x[0])
    
    c = {}
    c.update(csrf(request))
    return render_to_response('hospital.html',{'x':hos_name,'csrf_token':c['csrf_token']})

def get_hospital(request):
    if request.method == "GET":
        type_name= request.GET.get('devata',"")
        
    elif request.method == "POST":
        type_name= request.GET.get('devata',"")
    
    if str(type_name) == 'district':
        address = DimLocation.objects.all().values_list('district').distinct()
    elif str(type_name) == 'taluka':
        address = DimLocation.objects.all().values_list('taluka').distinct()
    elif str(type_name) == 'phc':
        address = DimLocation.objects.all().values_list('phc__name').distinct()
    elif str(type_name) == 'subcenter':
        address = DimLocation.objects.all().values_list('subcenter').distinct()

    res = []
    res.append('-------')
    for a in address:
        res.append(str(a[0]))
    result = {'res':res}
    res = json.dumps(result)
    return HttpResponse(res)

def get_villages(request):
    if request.method == "GET":
        village= request.GET.get('villages',"")
        
    elif request.method == "POST":
        village= request.GET.get('villages',"")
    villages = DimLocation.objects.filter(subcenter=str(village)).values_list('village')
    res = []
    
    for v in villages:
        res.append(str(v[0]))
    result = {'res':res}
    res = json.dumps(result)
    return HttpResponse(res)

def save_hospital(request):
    if request.method == 'GET':
        country = request.GET.get('country','')
        hosname = request.GET.get('hosname','')
        hostype = request.GET.get('hostype','')
        address = request.GET.get('address','')
        villages = request.GET.get('villages','')
        parenthos = request.GET.get('parenthos','')
        active = request.GET.get('active','')
    elif request.method == 'POST':
        country = request.POST.get('country','')
        hosname = request.POST.get('hosname','')
        hostype = request.POST.get('hostype','')
        address = request.POST.get('address','')
        villages = request.POST.get('villages','')
        parenthos = request.POST.get('parenthos','')
        active = request.POST.get('active','')
    acti = 0
    if str(active) == 'on':
        acti = 1
    hospital_details = HospitalDetails(country=str(country),hospital_name=str(hosname),hospital_type=str(hostype),parent_hospital=str(parenthos),address=str(address),village=str(villages),status=acti)
    hospital_details.save()
    x = {"result":'/admin/'}
    x=json.dumps(x)
    return HttpResponse(x)

def adminadd_usermaintenance(request):
    hosname = HospitalDetails.objects.all().values_list('hospital_name')
    hos_name=[]
    for x in hosname:
        hos_name.append(x[0])
    c = {}
    c.update(csrf(request))
    return render_to_response('userdetail.html',{'x':hos_name,'csrf_token':c['csrf_token']})

def get_uservillage(request):

    if request.method == "GET":
        hospital_name = request.GET.get('hospital_name',"")
    elif request.method == "POST":
        hospital_name = request.GET.get('hospital_name',"")
    villages = HospitalDetails.objects.filter(hospital_name=str(hospital_name)).values_list('village')
    if len(villages) >0:
        res = villages[0][0].split(',')
    result = {'res':res}
    res = json.dumps(result)
    return HttpResponse(res)

def edit_hospital(request,hospital_id):
    global hos_id
    hos_id = hospital_id
    if request.method == 'GET':
        edit_details = HospitalDetails.objects.get(id=int(hospital_id))
    elif request.method == 'POST':
        edit_details = HospitalDetails.objects.get(id=int(hospital_id))
    hostype = []
    hos_type = HospitalType.objects.all().values_list('types')
    hostype.insert(0,edit_details.hospital_type)
    for hospital_types in hos_type:
        if hospital_types[0] not in hostype:
            hostype.append(str(hospital_types[0]))
    country=[]
    names= CountryTb.objects.all().values_list('country_name')
    country.insert(0,edit_details.country)
    for country_data in names:
        if country_data[0] not in country:
            country.append(str(country_data[0]))
    parent_hos =[]
    hospital_data=HospitalDetails.objects.all().values_list('hospital_name')
    parent_hos.insert(0,edit_details.parent_hospital)
    for hospital in hospital_data:
        hos_temp = hospital[0].strip()
        if hos_temp not in parent_hos:
            parent_hos.append(str(hos_temp))
    villages = edit_details.village.split(',')

    if str(edit_details.hospital_type) == 'district':
        list_location = DimLocation.objects.all().values_list('district')
    elif str(edit_details.hospital_type) == 'taluka':
        list_location = DimLocation.objects.all().values_list('taluka')
    elif str(edit_details.hospital_type) == 'phc':
        list_location = DimLocation.objects.all().values_list('phc__name')
    elif str(edit_details.hospital_type) =='subcenter':
        list_location = DimLocation.objects.all().values_list('subcenter')

    address =[]
    address.insert(0,edit_details.address)
    for l in list_location:
        if l[0] not in address:
            address.append(l[0])

    c = {}
    c.update(csrf(request))
    return render_to_response('edithospital.html',{'edit_details':edit_details,'hostype':hostype,'country':country,'x':parent_hos,'address':address,'village':villages,'csrf_token':c['csrf_token']})

def update_hospitaldetail(request):
    global hos_id
    if request.method == 'GET':
        country_name= request.GET.get('country','')
        hospitalname = request.GET.get('hosname','')
        hospitaltype = request.GET.get('hostype','')
        parenthospital = request.GET.get('parenthos','')
        hos_address = request.GET.get('address','')
        hos_village = request.GET.get('villages','')
        active = request.GET.get('active','')
    elif request.method == 'POST':
        country_name= request.POST.get('country','')
        hospitalname = request.POST.get('hosname','')
        hospitaltype = request.POST.get('hostype','')
        parenthospital = request.POST.get('parenthos','')
        hos_address = request.POST.get('address','')
        hos_village = request.POST.get('villages','')
        active = request.POST.get('active','')
    acti = 0
    if str(active) == 'on':
        acti = 1
    edit_hospital = HospitalDetails.objects.filter(id=hos_id).update(country=str(country_name),hospital_name=str(hospitalname),hospital_type=str(hospitaltype),parent_hospital=str(parenthospital),address = str(hos_address),village=str(hos_village),status=acti)
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)
    
def save_usermaintenance(request):
    if request.method == 'GET':
        userrole = request.GET.get('userrole','')
        userid = request.GET.get('userid','')
        first_name = request.GET.get('first_name','')
        last_name = request.GET.get('last_name','')
        password = request.GET.get('password','')
        mobile = request.GET.get('mobile','')
        email = request.GET.get('email','')
        active = request.GET.get('active','')
        hospital = request.GET.get('hospital','')
        village = request.GET.get('village','')
        anc = request.GET.get('anc','')
        pnc = request.GET.get('pnc','')
        ec = request.GET.get('ec','')
        fp = request.GET.get('fp','')
        child = request.GET.get('child','')

    elif request.method == 'POST':
        userrole = request.POST.get('userrole','')
        userid = request.POST.get('userid','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        mobile = request.POST.get('mobile','')
        email = request.POST.get('email','')
        active = request.POST.get('active','')
        hospital = request.POST.get('hospital','')
        village = request.POST.get('village','')
        anc = request.GET.get('anc','')
        pnc = request.GET.get('pnc','')
        ec = request.GET.get('ec','')
        fp = request.GET.get('fp','')
        child = request.GET.get('child','')
       
    acti = 0
    pnc_active = 0
    anc_active = 0
    ec_active = 0
    fp_active = 0
    child_active = 0
    if str(active) == 'on':
        acti = 1
    
    if str(anc) == 'on':
        anc_active = 1
    
    if str(pnc) == 'on':
        pnc_active = 1
    
    if str(ec) == 'on':
        ec_active = 1
    
    if str(fp) == 'on':
        fp_active = 1
    
    if str(child) == 'on':
        child_active = 1
    
    village_details = UserMaintenance(user_role=str(userrole),user_id=str(userid),firstname=str(first_name),lastname=str(last_name),password=str(password),hospital=str(hospital),village=str(village),status=acti,mobile=int(mobile),email=str(email),pnc=pnc_active,anc=anc_active,ec=ec_active,fp=fp_active,child=child_active)
    village_details.save()
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)

def edit_usermaintenance(request,batch_id):

    global doc_id
    doc_id = batch_id
    details=UserMaintenance.objects.get(id=int(batch_id))
    role = ['ANM','PHC','DOC']
    user_role = []
    anm = False
    if str(details.user_role) == 'ANM':
        anm = True
    user_role.insert(0,details.user_role)
    for r in role:
        if r not in user_role:
            user_role.append(r) 
    hos_name =[]
    hospital_data=HospitalDetails.objects.all().values_list('hospital_name')
    hos_name.insert(0,details.hospital)
    for hospital in hospital_data:
        if hospital not in hos_name:
            hos_name.append(str(hospital[0]))
    villages = details.village.split(',')
    status = details.status
    c_status=False
    if str(status) == 'True':
        c_status = True
    anc=details.anc
    anc_status=False
    if str(anc) == 'True':
        anc_status = True
    pnc=details.pnc   
    pnc_status=False
    if str(pnc) == 'True':
        pnc_status = True
    ec=details.ec
    ec_status=False
    if str(ec) == 'True':
        ec_status = True
    fp=details.fp
    fp_status=False
    if str(fp) == 'True':
        fp_status = True
    child=details.child
    child_status=False
    if str(child) == 'True':
        child_status = True
    c = {}
    c.update(csrf(request))
    return render_to_response('edituserdetails.html',{'y':details,'user_role':user_role,'village':villages,'hospital':hos_name,'status':c_status,'anc':anc_status,'pnc':pnc_status,'ec':ec_status,'fp':fp_status,'child':child_status,'anm':anm,'csrf_token':c['csrf_token']})


def  update_usermaintenance(request):
    global doc_id
    if request.method == 'GET':
        userrole = request.GET.get('userrole','')
        userid = request.GET.get('userid','')
        first_name = request.GET.get('first_name','')
        last_name = request.GET.get('last_name','')
        password = request.GET.get('password','')
        mobile = request.GET.get('mobile','')
        email = request.GET.get('email','')
        active = request.GET.get('active','')
        hospital = request.GET.get('hospital','')
        village = request.GET.get('village','')
        anc = request.GET.get('anc','')
        pnc = request.GET.get('pnc','')
        ec = request.GET.get('ec','')
        fp = request.GET.get('fp','')
        child = request.GET.get('child','')

    elif request.method == 'POST':
        userrole = request.POST.get('userrole','')
        userid = request.POST.get('userid','')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        password = request.POST.get('password','')
        mobile = request.POST.get('mobile','')
        email = request.POST.get('email','')
        active = request.POST.get('active','')
        hospital = request.POST.get('hospital','')
        village = request.POST.get('village','')
        anc = request.GET.get('anc','')
        pnc = request.GET.get('pnc','')
        ec = request.GET.get('ec','')
        fp = request.GET.get('fp','')
        child = request.GET.get('child','')

    acti = 0
    pnc_active = 0
    anc_active = 0
    ec_active = 0
    fp_active = 0
    child_active = 0
    if str(active) == 'on':
        acti = 1
    
    if str(anc) == 'on':
        anc_active = 1
    
    if str(pnc) == 'on':
        pnc_active = 1
    
    if str(ec) == 'on':
        ec_active = 1
    
    if str(fp) == 'on':
        fp_active = 1
    
    if str(child) == 'on':
        child_active = 1

    edit_details = UserMaintenance.objects.filter(id=doc_id).update(user_role=str(userrole),user_id=str(userid),firstname=str(first_name),lastname=str(last_name),password=str(password),hospital=str(hospital),village=str(village),status=acti,mobile=int(mobile),email=str(email),pnc=pnc_active,anc=anc_active,ec=ec_active,fp=fp_active,child=child_active)
    x = {"result":1}
    x=json.dumps(x)
    return HttpResponse(x)
