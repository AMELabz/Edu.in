## EXP 11: Unit Testing with Mocking for Autonomous Decisions

### AIM
To developstructured unit test suites using a Mocking framework that validates an autonomousdecision matrix without making actual external API calls.

### ALGORITHM
1. Installtherequired Python libraries.
2. Importtherequired modules.
3. Createafunction to simulate fetching weather information from an external API.
4. Createanautonomous decision function based on the weather data.
5. Writeunittest cases.
6. Use Mocking to replace the real API response.
7. Executealltest cases.
8. Displaythetest results.
9. End theprocess.

### PROGRAM
```python
import unittest
from unittest.mock import patch


def get_weather():
    """Normally this calls a live weather API."""
    return "Sunny"


def decision():
    weather = get_weather()
    if weather == "Sunny":
        return "Go Outside"
    elif weather == "Rainy":
        return "Stay Home"
    return "Unknown Decision"


class TestDecision(unittest.TestCase):

    @patch("__main__.get_weather", return_value="Sunny")
    def test_sunny(self, mock_weather):
        self.assertEqual(decision(), "Go Outside")

    @patch("__main__.get_weather", return_value="Rainy")
    def test_rainy(self, mock_weather):
        self.assertEqual(decision(), "Stay Home")

    @patch("__main__.get_weather", return_value="Cloudy")
    def test_unknown(self, mock_weather):
        self.assertEqual(decision(), "Unknown Decision")


print("Executing Test Cases...\n")
unittest.main(argv=[""], exit=False)
```

### OUTPUT
```text
Executing Test Cases...

...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### RESULT
The structured unit test suite was executed successfully using Mocking without calling any live external API.
