import os


class Settings:
    def __init__(self, filename='settings.properties'):
        self._filename = filename

        if not os.path.exists(filename):
            raise FileNotFoundError(f"Settings file '{filename}' not found")

        self._settings = self._parse_properties(filename)


    #parse the settings.properties file in order to find out what repo we use and the file name
    def _parse_properties(self, filename):
        settings = {}

        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                #use key tuples
                if '=' in line:
                    key, value = line.split('=', 1)

                    #key is: repo, student...
                    #value is: binary/text.... or the name of the file

                    key = key.strip()
                    value = value.strip().strip('"\'')
                    settings[key] = value

        return settings

    def get_repository_type(self):
        return self._settings.get('repository')

    def get_student_file(self):
        return self._settings.get('students')

    def get_assignment_file(self):
        return self._settings.get('assignments')

    def get_grade_file(self):

        return self._settings.get('grades')