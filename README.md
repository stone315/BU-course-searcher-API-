# A course searching API for Boston University(BU)
This project provide an advanced web API for BU course searching

The user can search courses based on the following parameters:

- sem : Fall/Summer/Spring
- year: any 4 digits
- keyword: Any string and replace space(' ') with + , ____ for no keyworld
- credits: 0,1,2,3,4,5+, any
- school: ___(for no input),CAS,ENG ...
- major: AA,AH,ME...., __(for no input)
- time: Any combination of M,T,W,R,F and _(for no input)
- condition (optional input) : Class_Closed or Class_Full


url link =  url_address/semester/year/keyword/credits/school/major/time/condition (optional)

ie. localhost:3000/Fall/2020/Electrical/3/ENG/ME/MW

this link search all 3 credits Monday Wednesday courses in Fall 2020 with the keyword "Electrical" in Engineer department ME major 

# Requirement
Django

```
python -m pip install Django
```

Python 3.8




bs4

```
pip install beautifulsoup4
```
