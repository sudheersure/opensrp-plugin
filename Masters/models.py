from __future__ import unicode_literals
import json
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
import hashlib
import commands

class AnnualTarget(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    service_provider = models.ForeignKey('DimAnm', db_column='service_provider')
    indicator = models.ForeignKey('DimIndicator', db_column='indicator')
    target = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'annual_target'


    def __unicode__(self):
        return unicode(self.target)

class DimAnm(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    anmidentifier = models.CharField(unique=True, max_length=100)
    phc = models.ForeignKey('DimPhc', db_column='phc')
    subcenter = models.CharField(max_length=100,)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dim_anm'
        verbose_name_plural='ANM'
	verbose_name='ANM'

    def __unicode__(self):
        return self.anmidentifier



class DimIndicator(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    indicator = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'dim_indicator'
        verbose_name_plural='INDICATOR'
	verbose_name='INDICATOR'

    def __unicode__(self):
        return unicode(self.indicator)


class DimLocation(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    village = models.CharField(max_length=100)
    subcenter = models.CharField(max_length=100)
    phc = models.ForeignKey('DimPhc', db_column='phc')
    taluka = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dim_location'
        verbose_name_plural='LOCATIONS'
	verbose_name='LOCATIONS'

    def __unicode__(self):
        return unicode(self.village)

class Subcenter(models.Model):
    subcenter = models.CharField(max_length=100)    
    class Meta:
        managed = False
        db_table = 'subcenter_tb'

class DimPhc(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    phcidentifier = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dim_phc'
        verbose_name_plural = 'PHCS'
	verbose_name='PHCS'

    def __unicode__(self):
        return unicode(self.name)


class DimServiceProvider(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    service_provider = models.IntegerField()
    type = models.ForeignKey('DimServiceProviderType', db_column='type')

    class Meta:
        managed = False
        db_table = 'dim_service_provider'
        verbose_name_plural='USER ROLE'
	verbose_name='USER ROLE'
    def __unicode__(self):
        return unicode(self.service_provider)

class DimServiceProviderType(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    type = models.CharField(unique=True,max_length=100)

    class Meta:
        managed = False
        db_table = 'dim_service_provider_type'
        verbose_name_plural='USER TYPE'
	verbose_name='USER TYPE'

    def __unicode__(self):
        return unicode(self.type)


class SchemaVersion(models.Model):
    version_rank = models.IntegerField()
    installed_rank = models.IntegerField()
    version = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    script = models.CharField(max_length=1000)
    checksum = models.IntegerField(blank=True, null=True)
    installed_by = models.CharField(max_length=30)
    installed_on = models.DateTimeField()
    execution_time = models.IntegerField()
    success = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'schema_version'


"""class ServiceProvided(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    service_provider = models.ForeignKey(DimServiceProvider, db_column='service_provider')
    externalid = models.CharField(max_length=100)
    indicator = models.ForeignKey(DimIndicator, db_column='indicator')
    location = models.IntegerField()
    date_field = models.ForeignKey(DimLocation, db_column='date_', blank=True, null=True)  # Field renamed because it ended with '_'.
    dristhi_entity_id = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'service_provided'
    def __unicode__(self):
        return unicode(self.service_provider)
    def __unicode__(self):
        return unicode(self.indicator)
    def __unicode__(self):
        return unicode(self.date_field)"""

class AuthGroup(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField(default=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class DimUserLogin(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True,max_length=30)
    password = models.CharField(max_length=128)
    user_role = models.ForeignKey(DimServiceProviderType, db_column='user_role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_user_login'
        verbose_name_plural = 'USER LOGIN'
	verbose_name='USER LOGIN'

    def __unicode__(self):
        return unicode(self.name)    

    def save(self, *args, **kwargs):
        self.name =self.name
        m = hashlib.sha1()
        m.update(self.password)
        self.password = m.hexdigest()
        super(DimUserLogin, self).save(*args, **kwargs)
     
    def __unicode__(self):
        return self.name

@receiver(post_save, sender=DimUserLogin)
def anmidentifier_post(sender,instance,**kwargs):
    usr_role = settings.USER_ROLE[str(instance.user_role)]
    user_curl = "curl -s -H -X GET http://localhost:5984/drishti/_design/DrishtiUser/_view/by_username?key="+"%22"+str(instance.name)+"%22"
    user_data = commands.getoutput(user_curl) 
    output = json.loads(user_data)
    output = dict(output)
    row = output['rows']
    if len(row)>0:
        id_val = dict(output['rows'][0])
        rev_curl = "curl -s -H -X GET http://localhost:5984/drishti/"+id_val['id']
        rev_data = commands.getoutput(rev_curl)
        rev_data = dict(json.loads(rev_data))
        delet_curl = "curl -X DELETE http://localhost:5984/drishti/"+id_val['id']+"/?rev\="+rev_data['_rev']
        user_data = commands.getoutput(delet_curl) 
    user_pwd=DimUserLogin.objects.filter(name=str(instance)).values_list('password')
    cmd = '''curl -s -H Content-Type:application/json -d '{"docs": [{"type": "DrishtiUser","username": "%s","password": "%s","active": true,"roles": ["%s"]  } ]}' -X POST http://localhost:5984/drishti/_bulk_docs''' %(str(instance.name),str(instance.password),str(usr_role))
    res = commands.getstatusoutput(cmd)
    
post_save.connect(anmidentifier_post,sender=DimUserLogin)


class DjangoAdminLog(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
   # id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ServiceProvidedReportView(models.Model):
    # id = models.IntegerField(primary_key=True)
    anmidentifier = models.CharField(max_length=100, blank=True)
    service_provided_type = models.CharField(max_length=100, blank=True)
    indicator = models.CharField(max_length=100, blank=True)
    service_date = models.DateField(blank=True, null=True)
    village = models.CharField(max_length=100, blank=True)
    subcenter = models.CharField(max_length=100, blank=True)
    phc = models.CharField(max_length=100, blank=True)
    taluka = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'service_provided_report_view'


class Token(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    nas_me = models.CharField(unique=True, max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'token'


class DrugInfo(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    drug_name = models.CharField(unique=True, max_length=100)
    frequency = models.ForeignKey('Frequency', db_column='frequency',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)
    dosage = models.ForeignKey('Dosage', db_column='dosage',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)
    direction = models.ForeignKey('Directions', db_column='direction',null=True,blank=True,limit_choices_to={'active': True},on_delete=models.SET_NULL)

    class Meta:
        managed = False
        db_table = 'drug_info'
        verbose_name_plural="DRUG INFO"
	verbose_name='DRUG INFO'
    def __unicode__(self):
        return self.drug_name

class Frequency(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    active = models.BooleanField(default=True)
    number_of_times = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'frequency'
        verbose_name_plural="FREQUENCIES"
	verbose_name='FREQUIENCIES'

    def __unicode__(self):
        return unicode(self.number_of_times)

class Dosage(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    dosage = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'dosage'
        verbose_name_plural="DOSAGE"
	verbose_name='DOSAGE'
    def __unicode__(self):
        return self.dosage

class Directions(models.Model):
    #id = models.IntegerField(primary_key=True)  # AutoField?
    directions = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'directions'
        verbose_name_plural = "DIRECTIONS"
	verbose_name='DIRECTIONS'
    def __unicode__(self):
        return self.directions

class Investigations(models.Model):
    INVESTIGATION_SERVICE_GROUP= (('radiology','Radiology'),
		                          ('laboratory','Laboratory'),
		                          ('procedures','Procedures'),
    )
    #id = models.IntegerField(primary_key=True)  # AutoField?
    service_group_name = models.CharField(max_length=200,choices=INVESTIGATION_SERVICE_GROUP)
    investigation_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'investigation'
        verbose_name_plural = "INVESTIGATION"
	verbose_name='INVESTIGATION'

    def __unicode__(self):
        return self.investigation_name

class ICD10(models.Model):
    ICD10CHAPTER = (('I - Certain infectious and parasitic diseases (A00-B99)','I- Certain infectious and parasitic diseases (A00-B99)'),
               ('II - Neoplasms (C00-D48)','II   - Neoplasms (C00-D48)'),
               ('III - Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism (D50-D89)','III - Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism (D50-D89)'),
               ('IV - Endocrine, nutritional and metabolic diseases (E00-E90)','IV - Endocrine, nutritional and metabolic diseases (E00-E90)'),
               ('V - Mental and behavioral disorders (F00-F99)','V - Mental and behavioral disorders (F00-F99)'),
               ('VI - Diseases of the nervous system (G00-G99)','VI - Diseases of the nervous system (G00-G99)'),
               ('VII - Diseases of the eye and adnexa (H00-H59)','VII - Diseases of the eye and adnexa (H00-H59)'),
               ('VIII - Diseases of the ear and mastoid process (H60-H95)','VIII - Diseases of the ear and mastoid process (H60-H95)'),
               ('IX - Diseases of the circulatory system (I00-I99)','IX - Diseases of the circulatory system (I00-I99)'),
               ('X - Diseases of the respiratory system (J00-J99)','X - Diseases of the respiratory system (J00-J99)'),
               ('XI - Diseases of the digestive system (K00-K93)','XI - Diseases of the digestive system (K00-K93)'),
               ('XII - Diseases of the skin and subcutaneous tissue (L00-L99)','XII - Diseases of the skin and subcutaneous tissue (L00-L99)'),
               ('XIII - Diseases of the musculoskeletal system and connective tissue (M00-M99)','XIII - Diseases of the musculoskeletal system and connective tissue (M00-M99)'),
               ('XIV - Diseases of the genitourinary system (N00-N99)','XIV - Diseases of the genitourinary system (N00-N99)'),
               ('XV - Pregnancy, childbirth and the puerperium (O00-O99)','XV - Pregnancy, childbirth and the puerperium (O00-O99)'),
               ('XVI - Certain conditions originating in the perinatal period (P00-P96)','XVI - Certain conditions originating in the perinatal period (P00-P96)'),
               ('XVII - Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)','XVII - Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)'),
               ('XVIII - Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)','XVIII - Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)'),
               ('XIX - Injury, poisoning and certain other consequences of external causes (S00-T98)','XIX - Injury, poisoning and certain other consequences of external causes (S00-T98)'),
               ('XX - External causes of morbidity and mortality (V01-Y98)','XX - External causes of morbidity and mortality (V01-Y98)'),
               ('XXI - Factors influencing health status and contact with health services (Z00-Z99)','XXI - Factors influencing health status and contact with health services (Z00-Z99)'),
               ('XXII - Codes for special purposes (U00-U99)','XXII - Codes for special purposes (U00-U99)'),
    )
    ICD10_Chapter = models.CharField(max_length=200,choices=ICD10CHAPTER) 
    ICD10_Code = models.CharField(max_length=100) 
    ICD10_Name = models.CharField(max_length=100) 
    can_select = models.BooleanField(default=True) 
    status = models.BooleanField(default= True) 

    class Meta: 
        managed = False
        db_table = 'icd10'
        verbose_name_plural="ICD10 CODES"
	verbose_name='ICD10 CODES'
    def __unicode_(self):
        return self.ICD10_Name

class PocInfo(models.Model):

    visitentityid = models.CharField(max_length=100) # AutoField?
    entityidec = models.CharField(max_length=100)
    anmid = models.CharField(max_length=100)
    level = models.CharField(max_length=35)
    clientversion = models.CharField(max_length=35)
    serverversion = models.CharField(max_length=35)
    visittype = models.CharField(max_length=35)
    phc = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'poc_table'
        verbose_name_plural="POC INFO"
	verbose_name='POC INFO'
    def __unicode__(self):
        return unicode(self.visitentityid)



class DocInfo(models.Model):
    docname = models.CharField(unique=True,max_length=100)
    phc = models.ForeignKey('DimPhc', db_column='phc')
    
    class Meta:
        verbose_name_plural="DOCTORS"
        managed = False
        db_table = 'doc_info'
	verbose_name='DOCTORS'

    def __unicode__(self):
        return unicode(self.docname)

class PocBackup(models.Model):
    #id = models.IntegerField(primary_key=True)
    visitentityid = models.CharField(max_length=100)
    entityidec = models.CharField(max_length=100, blank=True)
    anmid = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=35, blank=True)
    clientversion = models.CharField(max_length=35, blank=True)
    serverversion = models.CharField(max_length=35, blank=True)
    visittype = models.CharField(max_length=35, blank=True)
    phc = models.CharField(max_length=100, blank=True)
    docid = models.CharField(max_length=100, blank=True)
    class Meta:
        managed = False
        db_table = 'poc_backup'
