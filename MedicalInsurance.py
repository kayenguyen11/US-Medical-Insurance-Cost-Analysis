#!/usr/bin/env python
# coding: utf-8


# This file is to build out analysis funtions and class methods


#Step 1: Import libraries and data
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from collections import defaultdict

#Step 2: Define class and functions: 
class MedicalInsurance:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.ages = []
        self.sex = []
        self.bmi = []
        self.children = []
        self.smokers = []
        self.regions = []
        self.charges = []
        self.length = 0
    def import_data(self) -> None:
        with open(self.filepath) as insurance_file:
            insurance = csv.DictReader(insurance_file)
            for row in insurance:
                self.ages.append(int(row['age']))
                self.sex.append(row['sex'])
                self.bmi.append(float(row['bmi']))
                self.children.append(int(row['children']))
                self.smokers.append(row['smoker'])
                self.regions.append(row['region'])
                self.charges.append(float(row['charges']))
                self.length += 1
#Step 3: Define fuctions to analyze age:
    def average_age(self) -> float:
        return sum(self.ages)/self.length     
        
    def median_age(self) -> float:
        return  np.median(self.ages)
        
    def max_age(self) -> int:
        return  np.max(self.ages)
        
    def min_age(self) -> int:
        return  np.min(self.ages)
        
    def age_chart(self):
        print('Average age of patents is {}.'.format(self.average_age()))
        print('Median age of patents is {}.'.format(self.median_age()))
        print('The oldest patient is {} years old'.format(self.max_age()))
        print('The youngest patent is {} years old.'.format(self.min_age()))
        plt.hist(self.ages, bins = 20)
        plt.axvline(self.median_age(), color='k', linestyle='dashed', linewidth=1)
        plt.axvline(self.average_age(), color='m', linestyle='dashed', linewidth=1)
        plt.show()

#Step 4: Define fuctions to analyze regions: 
    def region_count(self):
        count = {}
        for region in self.regions:
            count[region] = count.get(region,0) + 1
        return count
        

    def regions_chart(self):
        regions_count = self.region_count()
        for key in regions_count:
            print('There are {} people from {}'.format(key, regions_count[key]))
        plt.bar(list(regions_count.keys()), regions_count.values())
        plt.xticks = list(regions_count.keys())
        plt.xlabel('Region')
        plt.ylabel('No. of patients')
        plt.show()
        
#Step 5: Define functions to analyze smokers/non-smokers and genders:
    def smoker_count(self) -> int:
        return self.smokers.count('yes')

    def non_smoker_count(self) -> int:
        return self.length - self.smoker_count()

    def smoker_percentage(self) -> float:
        return round((self.smoker_count() / self.length) * 100, 2)

    def non_smoker_percentage(self) -> float:
        return round((self.non_smoker_count() / self.length) * 100, 2)

    def smoker_and_sex_count(self) -> int:
        male_smoker = 0
        female_smoker = 0
        for index in range(self.length):
            if self.smokers[index] == 'yes' and self.sex[index] == 'male':
                male_smoker += 1
            elif self.smokers[index] == 'yes' and self.sex[index] == 'female':
                female_smoker += 1
            else:
                pass
        print('Among the patients, {}% of them are smokers, and {}% of them are non-smokers'.format(self.smoker_percentage(), self.non_smoker_percentage()))
        print('The are ',male_smoker, ' of smokers are male')
        print('The are ',female_smoker, ' of smokers are female')

#Step 6: Define functions to check if there is any association between smoking status and insurance cost, between sex and insurance cost:
    def average_charges(self) -> float:
        return sum(self.charges) / len(self.charges)
    
    def association_chart(self):
        insurance = pd.read_csv('insurance.csv')
        sns.boxplot(data=insurance, x='sex', y='charges')
        plt.show()
        sns.boxplot(data=insurance, x='smoker', y='charges')
        plt.show()
        
    
    def smokers_vs_charges_dict(self):
        smokers_vs_charges = {}
        for index in range(self.length):
            smokers_vs_charges[self.smokers[index]] = smokers_vs_charges.get(self.smokers[index],0) + self.charges[index]
        return smokers_vs_charges

#     def avg_smoker_charges(self):
#         smoker_charges = self.smokers_vs_charges_dict()
#         return round(smoker_charges.get('yes') / self.smoker_count(), 2)

    def draw_smoker_average_cost_chart(self):
        smoker_charges = self.smokers_vs_charges_dict()
        avg_smoker_charges = round(smoker_charges.get('yes') / self.smoker_count(), 2)
        avg_non_smoker_charges = round(smoker_charges.get('no') / self.non_smoker_count(), 2)
        average_charges = self.average_charges()
        print(f'Average costs of patients is {average_charges} US dollars.')
        print(f'Average costs for smokers is {avg_smoker_charges} US dollars.')
        print(f'Average costs for non-smokers is {avg_non_smoker_charges} US dollars.')
        x = ['average cost', 'smoker costs', 'non-smoker costs']
        y = [average_charges, avg_smoker_charges, avg_non_smoker_charges]
        plt.bar(x, y)
        plt.xticks = x
        plt.ylabel('US dollars')
        plt.show()
        
        
#Step 5: Define functions to analyze children data:
    def count_children(self):
        children_count = {}
        for num in self.children:
            children_count[num] = children_count.get(num,0) + 1
        for key in children_count:
            print('There are {} patients having {} chilren.'.format(children_count[key], key))
        myexplode = [0.2, 0, 0, 0, 0, 0]
        plt.pie(children_count.values(), labels = children_count.keys(), explode = myexplode)
        plt.legend(title = 'Number of children',bbox_to_anchor=(1,1), bbox_transform=plt.gcf().transFigure)
        plt.show() 


# # END!
