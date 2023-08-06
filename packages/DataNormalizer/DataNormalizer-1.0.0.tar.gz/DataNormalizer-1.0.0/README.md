# General Information
DataNormalizer helps with importing datasets inside the platform by normalizing it. 

```python
import DataNormalizer
```

### Setting variables
The DataNormalizer library might need the details of the target app. These setting are set through properties.
```python
Clappform.Auth(baseURL="https://dev.clappform.com/", username="user@email.com", password="password")
Diagnose = DataNormalizer.Diagnose()
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.rules = json.load(open('../rules.json'))
```

### checkRules
Function that will check the custom rules against your dataframe
```python
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.rules = json.load(open('../rules.json'))
dataframe = DataNormalizer.Diagnose.checkRules()
```
Rules are added in a JSON file. Every column has its own rule however Rules without a column name are seen as global rules. 
```json
{
    "reset-coverage":"True",
    "action": "np.nan"
},
{ 
    "column": "gemeente",
    "check-coverage": "10",
    "selection": [ "Aa en Hunze", "Aalsmeer", "Aalten", "Achtkarspelen"]
},
{
    "column": "postalCode",
    "type": "postal_code"
}
```
Supported keys are
keys          | value                                   | explanation
------------- | -------------                           | -------------
column        | gemeente                                | On which column does this rule apply
type          | postal_code / int / string...           | What should the values of this column be
selection     | [ "Aa en Hunze", "Aalsmeer", "Aalten"]  | The values must be one of these values
check-coverage| 50                                      | Take a smaller sample of the column, in percentage
coverage-reset| True / False                            | If an error is found in the sample, fall back to 100%
regex         | [1-9][0-9]?$^100$                       | Column value should look like this regex
action        | np-nan                                  | What to do with the value if incorrect
mapping       | {"bad": "0","moderate": "1"}            | Map values to something else

Supported values for types
type          | explanation        
------------- | -------------
int         | accepts ints and floats get decimal removed
positive-int | same as int but only positive and zero  
negative-int | same as int but only negative   
string | characters accepted   
float | decimal numbers accepted   
boolean | makes lowercase and accepts true / false    
postal_code | accepts 1111AB format. Removes special chars then makes string uppercase
latitude / longitude | accepts 32.111111 format
letters | only accepts letters 

Supported values for action
action          | explanation        
------------- | -------------
np.nan         | Replaces mismatches with np.nan

### obtainKeys
Function that will find keys needed for the app, needs appData
```python
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
DataNormalizer.Diagnose.obtainKeys()
```

### matchKeys
Function that will find missing keys, needs appData and dataFrame
```python
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
DataNormalizer.Diagnose.matchKeys()
```

### fixMismatch
Function that will suggest changes to your dataset based on missing keys, needs appData and dataFrame
```python
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
DataNormalizer.Diagnose.fixMismatch(strictness = 0.8)
```


