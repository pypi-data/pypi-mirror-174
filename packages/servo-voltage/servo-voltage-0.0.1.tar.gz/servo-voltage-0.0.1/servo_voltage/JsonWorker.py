import json


class JsonWorker:
    dictionary = None

    @staticmethod
    def SaveToJson(servoId: int,
                   servoVoltage: int,
                   path: str = 'voltage.json'):
        dictionary = \
            {
                "servo_id": servoId,
                "servo_voltage": servoVoltage
            }

        voltage = json.dumps(dictionary, indent=2)
        with open(path, "w") as outfile:
            outfile.write(voltage)

        outfile.close()

    @staticmethod
    def GetJson(servoId: int,
                servoVoltage: int):
        dictionary = \
            {
                "servo_id": servoId,
                "servo_voltage": servoVoltage
            }
        voltage = json.dumps(dictionary, indent=2)
        return voltage

    @staticmethod
    def ReadFromJson(path: str = 'voltage.json'):
        with open(path, 'r') as openfile:
            voltage = json.load(openfile)

        openfile.close()
        return voltage

