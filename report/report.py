import json
import datetime
from datetime import date
import pandas as pd
from tabulate import tabulate
from LLL import *
from Service import *
class report:
    def __init__(self):
        pass

    def create_member_weekly_reports(self):
        today = date.today()
        with open("Member/MemberDirectory.json", mode="r") as memberFile:
            all_members = json.load(memberFile)
        for member in all_members["members"]:
            name = member["MemberName"]
            with open(f"Member/{name}/{name}_profile.json", "r") as aMemberFile:
                aMember = json.load(aMemberFile)
            with open(f"Member/{name}/{name}_{today}", "w") as f:
                json.dump(aMember, f,indent=4)
            dates = [datetime.strptime(service["Date of Service "], "%Y-%m-%d") for service in aMember["Services"]]
            date_diff = (dates[-1] - dates[0]).days
            if date_diff > 7:
                aMember['Services'] = []
                with open(f"Member/{name}/{name}_profile.json", "w") as file:
                    json.dump(aMember,file,indent=4)
            
    
    def create_provider_weekly_reports(self):
        today = date.today()
        with open("Provider/ProviderList.json", mode="r") as providerFile:
            all_providers = json.load(providerFile)
        for provider in all_providers["providers"]:
            name = provider["ProviderName"]
            with open(f"Provider/{name}/{name}_profile.json", "r") as aProviderFile:
                aProvider = json.load(aProviderFile)
            with open(f"Provider/{name}/{name}_{today}", "w") as f:
                json.dump(aProvider, f, indent=4)
            dates = [datetime.strptime(service["Date of Service "], "%Y-%m-%d") for service in aProvider["Services"]]
            date_diff = (dates[-1] - dates[0]).days
            if date_diff > 7:
                aProvider['Services'] = []
                aProvider["TotalConsultations"] = 0
                aProvider["TotalFees"] = " "
                with open(f"Provider/{name}/{name}_profile.json", "w") as file:
                    json.dump(aProvider,file,indent=4)
    
    def create_EFT_report(self):
        with open("Provider/ProviderList.json", mode="r") as providerFile:
            all_providers = json.load(providerFile)
        for provider in all_providers["providers"]:
            name = provider["ProviderName"]
            with open(f"Provider/{name}/{name}_profile.json", "r") as aProviderFile:
                aProvider = json.load(aProviderFile)
            provider_number = aProvider["ProviderID"]
            total_fees_transfer = aProvider["TotalFee"]
            with open("Provider/EFT.json", "r") as EFTfile:
                new_data = json.load(EFTfile)
            new_record = {
                "ProviderName":name,
                "ProviderId":provider_number,
                "TotalAmount":total_fees_transfer
            }
            new_data["EFT_Data"].append(new_record)
            with open("Provider/EFT.json", "w") as EFTfile:
                json.dump(new_data,EFTfile,indent=4)
            

            with open('Provider/EFT.json') as f:
                data = json.load(f)
            
            

# Create DataFrame from EFT_Data
            df = pd.DataFrame(data['EFT_Data'])

# Rename columns
            df = df.rename(columns={
                'ProviderName': 'Provider Name',
                'ProviderId': 'Provider ID',
                'TotalAmount': 'Total Fees'
            })

# Convert DataFrame to table format
            table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False, numalign='left')

# Print table
            print(table)
            data["EFT_Data"] = []
            with open("Provider/EFT.json", "w") as EFTfile:
                json.dump(data, EFTfile, indent=4)
    def create_summary_report(self):
        # create an instance of the RecordList class
        s = Service()
        record_list = RecordList()
        record_list.load_from_file("report/reports.txt")

# create a dictionary to store the provider information
        provider_info = {}

# iterate over the records in the list and update the provider information
        for record in record_list:
            provider_number = record.provider_number
            fee = s.get_fee(record.service_code)  # function to look up fee for service code
            if provider_number in provider_info:
                provider_info[provider_number]['consultations'] += 1
                provider_info[provider_number]['total_fee'] += fee
            else:
                provider_info[provider_number] = {'consultations': 1, 'total_fee': fee}

# print the summary report
        print("Accounts Payable Summary Report")
        print("------------------------------")
        total_providers = len(provider_info)
        total_consultations = 0
        total_fee = 0
        for provider_number, info in provider_info.items():
            consultations = info['consultations']
            fee = float(info['total_fee'].strip('$'))
            total_consultations += consultations
            total_fee += fee
        print(f"Provider {provider_number}: {consultations} consultations, ${fee:.2f} fee")
        print("------------------------------")
        print(f"Total providers: {total_providers}")
        print(f"Total consultations: {total_consultations}")
        print(f"Overall fee total: ${total_fee:.2f}")


            
            