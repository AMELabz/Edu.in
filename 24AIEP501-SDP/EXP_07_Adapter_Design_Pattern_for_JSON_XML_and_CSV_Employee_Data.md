## EXP 7: Adapter Design Pattern for JSON, XML and CSV Employee Data

### AIM
To implement the Adapter Design Pattern in Python for reading employee data from different file formats (JSON, XML, and CSV) and integrating them into a unified enterprise automation pipeline using a common interface.

### ALGORITHM
1. Import the required Python libraries (json, csv, xml.etree.ElementTree, and abc).
2. Create an abstract class DataSource containing the abstract method get_data().
3. Create the JSONData class to read employee records from the emp.json file.
4. Create the XMLData class to read employee records from the emp.xml file.
5. Create the CSVData class to read employee records from the emp.csv file.
6. Implement JSONAdapter, XMLAdapter, and CSVAdapter classes that convert the different data sources into the common get_data() interface.
7. Create the AutomationPipeline class to process and display the records received through the adapters.
8. Instantiate the adapters for the JSON, XML, and CSV data sources.
9. Pass each adapter to the automation pipeline for processing.
10. Display the employee records and the total number of records processed from each file format.

### PROGRAM
```python
import csv
import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

# Create sample files
with open("emp.json", "w") as f:
    f.write('{"employees": [{"id": 101, "name": "Alice"}, {"id": 102, "name": "Bob"}]}')

with open("emp.xml", "w") as f:
    f.write(
        "<employees>"
        "<employee><id>201</id><name>Charlie</name></employee>"
        "<employee><id>202</id><name>David</name></employee>"
        "</employees>"
    )

with open("emp.csv", "w") as f:
    f.write("id,name\n301,Eve\n302,Frank\n")


# Target interface
class DataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass


# Adapters
class JSONAdapter(DataSource):
    def get_data(self):
        with open("emp.json") as f:
            return json.load(f)["employees"]


class XMLAdapter(DataSource):
    def get_data(self):
        root = ET.parse("emp.xml").getroot()
        return [
            {"id": e.find("id").text, "name": e.find("name").text}
            for e in root.findall("employee")
        ]


class CSVAdapter(DataSource):
    def get_data(self):
        with open("emp.csv") as f:
            return list(csv.DictReader(f))


# Pipeline
class AutomationPipeline:
    def process(self, adapter, format_name):
        print(f"\n=== Processing {format_name} Data ===")
        records = adapter.get_data()
        for record in records:
            print(record)
        print("Total Records :", len(records))


pipeline = AutomationPipeline()
pipeline.process(JSONAdapter(), "JSON")
pipeline.process(XMLAdapter(), "XML")
pipeline.process(CSVAdapter(), "CSV")
```

### OUTPUT
```text

=== Processing JSON Data ===
{'id': 101, 'name': 'Alice'}
{'id': 102, 'name': 'Bob'}
Total Records : 2

=== Processing XML Data ===
{'id': '201', 'name': 'Charlie'}
{'id': '202', 'name': 'David'}
Total Records : 2

=== Processing CSV Data ===
{'id': '301', 'name': 'Eve'}
{'id': '302', 'name': 'Frank'}
Total Records : 2
```

### RESULT
The program was executed successfully. Data from JSON, XML, and CSV files was read and processed using the Adapter Design Pattern. All the data was converted into a common format and displayed through the unified enterprise automation pipeline.
