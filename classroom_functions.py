import csv
import os

root = None


class ClassroomApp:
    """Class representing classroom applications"""
    def __init__(self):
        global root

    def validate_grade_input(text):
        """
        Ensures that the user input follows the correct/expected grading format
        Arguments:
        - text (str): test for input validation
        - Returns:
        - Bool: if True the test is a valid grade formate, if not False
        """
        return re.match(r'^\d+(\.\d+)?$', text) is not None

    def add_name_to_csv(self, name, classroom_number):
        """
        Adds names to specific csv files
        Arguments:
        - name(str): adds name to csv
        - classroom_number (int): the classroom number

        Returns:
        - Bool: if True the name is sucessfully added, unless False
        """


        csv_filename = f"classroom_{classroom_number}.csv"

        if not os.path.exists(csv_filename):
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name])
                return True

        else:
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                students = list(reader)

                if len(students) > 3:
                    print('Max limit')
                    return False

            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name])
                return True

    def remove_name_from_csv(self, name, classroom_number):
        """
        Removes a name from a specific csv file
        Arguments:
        - name (str): name that is removed from csv
        - classroom_number (int): the classroom number
        Returns:
        - Bool: Name is removed if True, otherwise False
        """
        csv_filename = f"classroom_{classroom_number}.csv"
        temp_filename = f"{csv_filename}.temp"
        name_removed = False

        if os.path.exists(csv_filename):
            with open(csv_filename, mode='r', newline='') as file, open(temp_filename, mode='w', newline='') as temp_file:
                reader = csv.reader(file)
                writer = csv.writer(temp_file)

                for row in reader:
                    if row and row[0] == name:
                        name_removed = True
                    else:
                        writer.writerow(row)

            if name_removed:
                os.replace(temp_filename, csv_filename)
            else:
                os.remove(temp_filename)

        return name_removed

    def delete_student_csv(self, student_name):
        """
        Deletes the csv file with the names of specific students
        Arguments:
        - student_name (str): the name of the student
        Returns:
        - Bool: if True file is deleted, otherwise False
        """
        csv_filename = f"{student_name}.csv"

        if os.path.exists(csv_filename):
            os.remove(csv_filename)
            print(f"CSV file '{csv_filename}' deleted.")
            return True
        else:
            print(f"CSV file '{csv_filename}' does not exist.")
            return False

    def get_students_list(self, classroom_number):
        """
        Gets list of students for the specific classroom
        Arguments:
        -classroom_number (int): classroom number
        Returns:
        - list: the list of student names
        """
        csv_filename = f"classroom_{classroom_number}.csv"
        students_list = []

        if os.path.exists(csv_filename):
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    students_list.append(row[0])
        return students_list

    def add_grade_to_student(self, student_name, grade):
        """
        Adds a grade to specific student csv files
        Arguments:
        - student_name (str): name of the student
        - grade (str): the grade to add
        Returns:
        - None
        """
        csv_filename = f"{student_name}.csv"

        if not os.path.exists(csv_filename):
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Grade'])

        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([grade])

    def get_student_grades(self, student_name):
        """
        Gets the grades of specific students
        Arguments:
        - student_name(str): Name of the student
        Returns:
        - list: list of the grades for the student
        """
        csv_filename = f"{student_name}.csv"
        grades = []

        if os.path.exists(csv_filename):
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    grades.append(row[0])

        return grades

    def remove_grade_from_student(self, student_name, grade_to_remove):
        """
        Removes a specific grade
        Arguments:
        - student_name (str): name of the student
        - grade_to_remove (str): the grade to remove
        Returns:
        - None
        """
        csv_filename = f"{student_name}.csv"
        if os.path.exists(csv_filename):
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                grades = [row[0] for row in reader]

            if grade_to_remove in grades:
                grades.remove(grade_to_remove)

                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for grade in grades:
                        writer.writerow([grade])

                print(f"Grade '{grade_to_remove}' removed for '{student_name}'")
            else:
                print(f"Grade '{grade_to_remove}' not found for '{student_name}'")
