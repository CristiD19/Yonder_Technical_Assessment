import datetime
import requests
import openpyxl
import pandas as pd

class DriversLicense: 
    def __init__(self,data):
        self._id = data['id']
        self._nume = data['nume'] 
        self._prenume = data['prenume']
        self._categorie = data['categorie']
        self._data_de_emitere = data['dataDeEmitere']
        self._data_de_expirare = data['dataDeExpirare']
        self._suspendat = data['suspendat']

    def __str__(self):
        return f'ID: {self._id}, Name: {self._nume} {self._prenume}, Category: {self._categorie}, Issue Date: {self._data_de_emitere}, Expiry Date: {self._data_de_expirare}, Suspended: {self._suspendat}'

    def to_list(self):
        return [self._id, self._nume, self._prenume, self._categorie, self._data_de_emitere, self._data_de_expirare, self._suspendat]
    
    def suspendat(self):
        return self._suspendat
    
    def is_valid(self): 
        date = datetime.datetime.today()
        if datetime.datetime.strptime(self._data_de_expirare, '%d/%m/%Y') <= date :
            return False
        return True 
    
    def categorie(self):
        return self._categorie
    

class Utils: 

    @staticmethod
    def get_data():
        url = "http://localhost:30000/drivers-licenses/list"
        params = {"length": 150}
        response = requests.get(url, params)
        return response.json()
        

    @staticmethod
    def excel(licenses, exc='data'):

        wb = openpyxl.Workbook()
        ws_write = wb['Sheet']
        for l in licenses:
            ws_write.append(l.to_list())

        wb.save(filename=exc+'.xlsx')

    
    @staticmethod 
    def get_suspended_licenses(licenses):
        listt = [license for license in licenses if license.suspendat()]
        Utils.excel(listt, 'suspended')
        return listt

    @staticmethod 
    def get_valid_licenses(licenses): 
        listt = [license for license in licenses if license.is_valid()]
        Utils.excel(listt, 'valid_license')
        return listt
    
    @staticmethod 
    def get_licenses_by_category(licenses):
        d = {}
        for license in licenses:
            if license.categorie() not in d:
                d[license.categorie()] = 1 
            else: 
                d[license.categorie()] += 1
        
        wb = openpyxl.Workbook()
        ws = wb.active

        for categorie in d:
            ws.append([categorie, d[categorie]])

        wb.save('categories.xlsx') 

        return d


if __name__ == "__main__":
    data = Utils.get_data()
    licenses = [DriversLicense(d) for d in data]

    while True:
        print("\nOperation Menu:")
        print("1. List suspended licenses")
        print("2. Extract valid licenses issued until today's date")
        print("3. Find licenses based on category and their count")
        print("4. Exit")
        
        operation_id = input("Enter the operation ID: ")
        
        if operation_id == "1":
            suspended_licenses = Utils.get_suspended_licenses(licenses)
            print("Suspended Licenses:")
            for license in suspended_licenses:
                print(license)
        
        elif operation_id == "2":
            valid_licenses = Utils.get_valid_licenses(licenses)
            print("Valid Licenses Issued Until Today's Date:")
            for license in valid_licenses:
                print(license)
        
        elif operation_id == "3":
            license_counts = Utils.get_licenses_by_category(licenses)
            print("License Counts by Category:")
            for key in license_counts.keys():
                print(key + " => " + str(license_counts[key]))

        
        elif operation_id == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid operation ID. Please enter a valid operation ID.")





    


