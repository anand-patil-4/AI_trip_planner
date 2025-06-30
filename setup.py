from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return a list of requirements.
    '''
    requirement_list:List[str] = [] #creating an empty list
    try:
        with open("requirements.txt",'r') as file: #opening requirements.txt file in read mode
            lines = file.readlines() #reading all the lines
            for line in lines: #processing each line
                requirement=line.strip() #removing whitespace, new line, tabs
                if requirement and requirement!='-e .': #ignore empty lines and '-e .'
                    requirement_list.append(requirement) #add requirements in the list except '-e .'
    except FileNotFoundError:
        print("Requirements.txt file not found!")

    return requirement_list
print(get_requirements())
setup(
    name = "AI-TRAVEL-PLANNER",
    version = "0.0.1",
    author="Anand Kumar Patil",
    author_email="patilanand9562@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)






