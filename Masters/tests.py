from django.test import TestCase
from Masters.models import *

class CountryTbTestCase(TestCase):
    def setUp(self):
    	CountryTb.objects.create(country_name="India", country_code="91")
    
    def test_country(self):
    	country = CountryTb.objects.get(country_name="India")
    	code = CountryTb.objects.get(country_code="91")
    	self.assertEqual(country.country_name,"India")
        self.assertEqual(code.country_code,"91")
        self.assertEqual(len(country.country_name),5)
        print country
        print len(country.country_name)

class DisttabTestCase(TestCase):
	def setUp(self):
		Disttab.objects.create(country_name="India",county_name="andhra",district_name="prakasam")
	def test_district(self):
		country = Disttab.objects.get(country_name="India")
		county = Disttab.objects.get(county_name="andhra")
		district = Disttab.objects.get(district_name="prakasam")
		self.assertEqual(country.country_name,'India')
		self.assertEqual(county.county_name,'andhra')
		self.assertEqual(district.district_name,'prakasam')
		self.assertEqual(len(county.county_name),6)
		print district.district_name
		print country.country_name
		print county.county_name
		print len(district.district_name)

class SubdistrictTabTestCase(TestCase):
	def setUp(self):
		SubdistrictTab.objects.create(country="India",county="andhra",district="prakasam",subdistrict="ongole")
	def test_subdistrict(self):
		country = SubdistrictTab.objects.get(country="India")
		county = SubdistrictTab.objects.get(county="andhra")
		district = SubdistrictTab.objects.get(district="prakasam")
		subdistrict = SubdistrictTab.objects.get(subdistrict="ongole")
		self.assertEqual(country.country,'India')
		self.assertEqual(county.county,'andhra')
		self.assertEqual(district.district,'prakasam')
		self.assertEqual(subdistrict.subdistrict,'ongole')
		self.assertEqual(len(subdistrict.subdistrict),6)
                print country.country
		print county.county
		print district.district
		print subdistrict.subdistrict
		print len(subdistrict.subdistrict)

class LocationTabTestCase(TestCase):
	def setUp(self):
		LocationTab.objects.create(country="India",county="andhra",district="prakasam",subdistrict="ongole",location="kandukur")
	def test_location(self):
		country = LocationTab.objects.get(country="India")
		county = LocationTab.objects.get(county="andhra")
		district = LocationTab.objects.get(district="prakasam")
		subdistrict = LocationTab.objects.get(subdistrict="ongole")
		location = LocationTab.objects.get(location="kandukur")
		self.assertEqual(country.country,'India')
		self.assertEqual(county.county,'andhra')
		self.assertEqual(district.district,'prakasam')
		self.assertEqual(subdistrict.subdistrict,'ongole')
		self.assertEqual(location.location,'kandukur')
		self.assertEqual(len(location.location),8)
		print country.country
		print county.county
		print district.district
		print subdistrict.subdistrict
		print location.location
		print len(location.location)

class ICD10TestCase(TestCase):
	def setUp(self):
		ICD10.objects.create(ICD10_Chapter="dhanush",ICD10_Code="1245",ICD10_Name="nurse")
	def test_icd10(self):
		ICD10_Chapter = ICD10.objects.get(ICD10_Chapter="dhanush")
		ICD10_Code = ICD10.objects.get(ICD10_Code="1245")
		ICD10_Name = ICD10.objects.get(ICD10_Name="nurse")
		self.assertEqual(ICD10_Chapter.ICD10_Chapter,'dhanush')
		self.assertEqual(ICD10_Code.ICD10_Code,'1245')
		self.assertEqual(ICD10_Name.ICD10_Name,'nurse')
		self.assertEqual(len(ICD10_Name.ICD10_Name),5)
		print ICD10_Chapter.ICD10_Chapter
		print ICD10_Code.ICD10_Code
		print ICD10_Name.ICD10_Name
		print len(ICD10_Name.ICD10_Name)

class DirectionsTestCase(TestCase):
	def setUp(self):
		Directions.objects.create(directions="before breakfast")
	def test_directions(self):
		directions = Directions.objects.get(directions="before breakfast")
		self.assertEqual(directions.directions,'before breakfast')
		self.assertEqual(len(directions.directions),16)
		print directions.directions
		print len(directions.directions)

class DosageTestCase(TestCase):
	def setUp(self):
		Dosage.objects.create(dosage="500mg")
	def test_dosage(self):
		dosage = Dosage.objects.get(dosage="500mg")
		self.assertEqual(dosage.dosage,'500mg')
		self.assertEqual(len(dosage.dosage),5)
		print dosage.dosage
		print len(dosage.dosage)

class FrequencyTestCase(TestCase):
	def setUp(self):
		Frequency.objects.create(number_of_times="daily")
	def test_frequency(self):
		frequency = Frequency.objects.get(number_of_times="daily")
		self.assertEqual(frequency.number_of_times,'daily')
		self.assertEqual(len(frequency.number_of_times),5)
		print frequency.number_of_times
		print len(frequency.number_of_times)

class DrugInfoTestCase(TestCase):
    def setUp(self):
        self.direction=Directions.objects.create(directions="before breakfast")
        self.dosage=Dosage.objects.create(dosage="500mg")
        self.frequency=Frequency.objects.create(number_of_times="daily")
    def test_druginfo(self):
    	drug=DrugInfo.objects.create(drug_name="corex",frequency=self.frequency,dosage=self.dosage,direction=self.direction,anc_conditions="pallor",pnc_conditions="Blurred Vision",child_illness="Cough")
        self.assertEqual(drug.drug_name,'corex')
        self.assertEqual(drug.frequency.number_of_times,'daily')
        self.assertEqual(drug.dosage.dosage,'500mg')
        self.assertEqual(drug.direction.directions,'before breakfast')
        self.assertNotEqual(drug.anc_conditions,'pallor')
        self.assertNotEqual(drug.pnc_conditions,'Blurred Vision')
        self.assertNotEqual(drug.child_illness,'Cough')
        self.assertEqual(len(drug.drug_name),5) 
	print drug.drug_name
	print drug.frequency.number_of_times
	print drug.dosage.dosage
	print drug.direction.directions
	print drug.anc_conditions
	print drug.pnc_conditions
	print drug.child_illness
	print len(drug.drug_name)

class CountyTbTestCase(TestCase):
    def setUp(self):
        self.country=CountryTb.objects.create(country_name="India",country_code="91")
    def test_county(self):
        county = CountyTb.objects.create(country_name=self.country,county_name="andhra")
        self.assertEqual(county.country_name.country_name,'India')
        self.assertEqual(len(county.county_name),6)
	print county.country_name.country_name
	print len(county.country_name.country_name)

class HealthCentersTestCase(TestCase):
    def setUp(self):
        HealthCenters.objects.create(hospital_name="yashoda",hospital_type="country",hospital_address="begumpet",country_name="India",county_name="andhra",district_name="prakasam",subdistrict_name="ongole",location="kphb",parent_hospital="apolo",villages="ypl")
    def test_health(self):
        health=HealthCenters.objects.create(hospital_name="yashoda",hospital_type="country",hospital_address="begumpet",country_name="India",county_name="andhra",district_name="prakasam",subdistrict_name="ongole",location="kphb",parent_hospital="apolo",villages="ypl")
        self.assertEqual(health.hospital_name,'yashoda')
        self.assertEqual(health.hospital_type,'country')
        self.assertEqual(health.hospital_address,'begumpet')
        self.assertEqual(health.country_name,'India')
        self.assertEqual(health.county_name,'andhra')
        self.assertEqual(health.district_name,'prakasam')
        self.assertEqual(health.subdistrict_name,'ongole')
        self.assertEqual(health.location,'kphb')
        self.assertEqual(health.parent_hospital,'apolo')
        self.assertEqual(health.villages,'ypl')
        self.assertEqual(len(health.villages),3)
	print health.hospital_name
	print health.hospital_type
	print health.hospital_address
	print health.country_name
	print health.county_name
	print health.district_name
	print health.subdistrict_name
	print health.location
	print health.parent_hospital
	print health.villages
	print len(health.villages)



