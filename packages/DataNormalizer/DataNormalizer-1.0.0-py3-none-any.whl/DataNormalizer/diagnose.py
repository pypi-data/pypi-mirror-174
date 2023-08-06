# See if we can find the mismatch causing the error and fix it in normalise
import json
from math import floor
import re
from difflib import SequenceMatcher
from collections import namedtuple
import bisect
import numpy as np

class Diagnose:

    def __init__(self):
        self._appData = None
        self._dataFrame = None
        self._rules = None

    @property
    def appData(self):
        return self._appData
    
    @appData.setter
    def appData(self, value):
        self._appData = json.dumps(value)

    @property
    def dataFrame(self):
        return self._dataFrame
    
    @dataFrame.setter
    def dataFrame(self, value):
        self._dataFrame = value

    @property
    def rules(self):
        return self._rules
    
    @rules.setter
    def rules(self, value):
        self._rules = value

    def obtainKeys(self):
        keys = {}
        jsonData = self._appData

        # Find uuid rename keys using negative lookahead regex; text between { and "type": "rename"
        renameUUIDKeys = re.findall(
            '\{(?:(?!\{|' + re.escape('"type": "rename"') + ')[\s\S])*' + re.escape('"type": "rename"'), jsonData)
        uuidRegex = re.compile(
            '[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        uuidDollarRegex = re.compile(
            '\$[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        renameUUIDKeys = list(set(re.findall(uuidRegex, str(renameUUIDKeys))))

        # Find all $uuid keys
        dollarUUIDKeys = re.findall(uuidDollarRegex, jsonData)
        dollarUUIDKeys = [s.replace('$', '') for s in dollarUUIDKeys]

        # Remove styling parts
        jsonData = re.sub(
            re.escape('config": [') + '.*?' + re.escape('"id"'), '', jsonData)
        jsonData = re.sub(
            re.escape('styling": {') + '.*?' + re.escape('}'), '', jsonData)
        jsonData = re.sub(
            re.escape('styling": [') + '.*?' + re.escape(']'), '', jsonData)

        # Search normal and join keys
        normal_keys = re.findall(r'"key": "(.*?)"', jsonData)
        join_keys = re.findall(r'"join_key": "(.*?)"', jsonData)

        # Merge all key findings
        keys = set(normal_keys + join_keys + renameUUIDKeys + dollarUUIDKeys)
        return keys

    def matchKeys(self):
        keys = Diagnose.obtainKeys(self)

        # Compare the two lists of keys to eachother
        additionalKeys = list(self._dataFrame.columns.difference(keys))
        missingKeys = list(keys.difference(self._dataFrame.columns))

        values = namedtuple('keys', 'missingKeys additionalKeys')
        return values(missingKeys, additionalKeys)

    def fixMismatch(self, strictness=0.8):
        keys = Diagnose.matchKeys(self)
        dataframe = self._dataFrame

        if len(keys.missingKeys) < 1:
            return print("No missing keys")

        suggestions = []

        for i, missingKey in enumerate(keys.missingKeys):
            for additionalKey in keys.additionalKeys:
                similarity = SequenceMatcher(None, missingKey, additionalKey)

                # Check if missingKey looks like additionalKey
                if similarity.ratio() > strictness:
                    values = namedtuple('keys', 'missingKey additionalKey')
                    suggestions.append(values(missingKey, additionalKey))
                    keys.missingKeys.pop(i)

        print("\nWe did not find " + str(len(keys.missingKeys)) +
              " keys:\n" + str(sorted(keys.missingKeys, key=len)) + "\n")

        if len(suggestions) < 1:
            print("No matches, try lowering strictness")
            return dataframe

        # Propose suggestions
        for i, suggestion in enumerate(suggestions):
            print("Suggestion {}: missing '{}' might be additional: '{}'".format(
                i + 1, suggestion.missingKey, suggestion.additionalKey))

        # Ask user which suggestions to fix and then rename dataframe columns
        suggestionsToFix = list(map(int, input(
            "Which suggestion(s) do you want to fix? (example: 1 2 3): ").split()))
        for i in suggestionsToFix:
            dataframe = dataframe.rename(
                columns={suggestions[i - 1].additionalKey: suggestions[i - 1].missingKey})

        return dataframe

    def checkRules(self):
        dataframe = self._dataFrame
        rules = self._rules

        # Global settings
        resetCoverage = False
        globalAction = False

        # Contains "action" parameter
        errorsFound = False
        def handleError(i, value, columnValues):
            nonlocal errorsFound
            errorsFound = True

            action = globalAction
            if "action" in rules[j]:
                action = rules[j]["action"]

            if action == "np.nan":    
                columnValues[i] = np.nan
                
            print(str(rules[j]["column"]) + " mismatch row "+ str(i) + " - " + str(value))

        j = -1
        while j < len(rules):
            j += 1
            if j >= len(rules):
                break

            if not("column" in rules[j]):
                if ("reset-coverage" in rules[j]):
                    if (bool)(rules[j]["reset-coverage"]):
                        resetCoverage = bool(rules[j]["reset-coverage"])

                if ("action" in rules[j]):    
                    globalAction = rules[j]["action"]

                continue

            # Column not found in dataset
            try:
                columnValues = dataframe[rules[j]["column"]]
            except:
                continue                    

            if "mapping" in rules[j]:
                mapping = rules[j]["mapping"]
                for key, value in mapping.items():
                    columnValues = columnValues.replace(key, value)

            if "reset-coverage" in rules[j]:
                if (bool)(rules[j]["reset-coverage"]):
                    resetCoverage = (bool(rules[j]["reset-coverage"]))

            if "check-coverage" in rules[j]:
                if errorsFound and resetCoverage: errorsFound = False
                else:
                    if re.match(r"^[1-9][0-9]?$|^100$", rules[j]["check-coverage"]):
                        columnValues = columnValues.sample(frac=int(rules[j]["check-coverage"]) / 100)

            if "selection" in rules[j]:
                sortedSelection = sorted(rules[j]["selection"])
                for i, value in columnValues.items():                    
                    index = bisect.bisect_left(sortedSelection, str(value))
                    if index >= len(sortedSelection) or sortedSelection[index] != value:
                        handleError(i, value, columnValues)

            if "regex" in rules[j]:
                for i, value in columnValues.items():
                    if not re.match(rules[j]["regex"], str(value)):
                        handleError(i, value)

            if "type" in rules[j]:
                
                match rules[j]["type"]:

                    case "percentage":
                        for i, value in columnValues.items():
                            # Regex to match float between 0 and 100
                            if not re.match(r"^([0-9]|[1-9][0-9]|100)(\.[0-9]+)?$", str(value)):
                                handleError(i, value)
                            
                    case "boolean":
                        for i, value in columnValues.items():
                            columnValues[i] = str(value).lower()
                            if not re.match(r"^(true|false)$", str(value)):
                                handleError(i, value)

                    case "float":
                        if (dataframe['int'].dtype == float):
                            continue

                        for i, value in columnValues.items():
                            if(type(value) != int):
                                handleError(i, value)
                                
                    case "int":                        
                        if (dataframe['int'].dtype == int):
                            continue

                        for i, value in columnValues.items():
                            if(type(value) != int):
                                handleError(i, value)
                            else:
                                if (type(value) == float): handleError(i, value)
                                columnValues[i] = int(value)

                    case "positive-int":
                        for i, value in columnValues.items():
                            if (type(value) == int and value >= 0 == False):
                                handleError(i, value)

                    case "negative-int":
                        for i, value in columnValues.items():
                            if (type(value) == int and value < 0 == False):
                                handleError(i, value)

                    case "letters":
                        for i, value in columnValues.items():
                            if (value.isalpha() == False):
                                handleError(i, value)

                    # Normalise to 1111AB
                    case "postal_code":
                        columnValues.str.replace(r"[^a-zA-Z0-9]+", "").str.upper()

                        for i, value in columnValues.items():
                            if not re.match(r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$", str(value)):
                                handleError(i, value)
                    
                    case "longitude":
                        for i, value in columnValues.items():
                            if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                                handleError(i, value)

                    case "latitude":
                        for i, value in columnValues.items():
                            if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                                handleError(i, value)              

            # Loop again because error in sample
            if (resetCoverage and errorsFound and len(columnValues) < len(dataframe[rules[j]["column"]])): 
                j -= 1
                continue

            dataframe[rules[j]["column"]].update(columnValues)
        return dataframe