# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
#       with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   GArdoin,11/22/2026,Added Person and Student data classes and used Student objects
# ------------------------------------------------------------------------------------------ #
import json  # Lets the program read and write JSON files

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = ''  # Holds the choice made by the user.
students: list = []  # A table of student data (a list of Student objects)


# Data --------------------------------------- #
class Person:
    """
    A class representing person data.

    Properties:
    - first_name (str): The person's first name.
    - last_name (str): The person's last name.

    ChangeLog: (Who, When, What)
    GArdoin,11/22/2026,Created Class
    """

    def __init__(self, first_name: str = '', last_name: str = ''):
        """ This constructor sets the first and last name of a new Person object

        ChangeLog: (Who, When, What)
        GArdoin,11/22/2026,Created constructor

        :param first_name: string with the person's first name
        :param last_name: string with the person's last name
        """
        self.first_name = first_name  # Uses the first_name setter below
        self.last_name = last_name  # Uses the last_name setter below

    @property  # (getter or accessor)
    def first_name(self):
        """ Returns the first name in title case (for example, "vic" becomes "Vic") """
        return self.__first_name.title()

    @first_name.setter  # (setter or mutator)
    def first_name(self, value: str):
        """ Saves the first name, but only if it is all letters or empty """
        if value.isalpha() or value == "":  # Letters or the default empty string
            self.__first_name = value
        else:
            raise ValueError("The first name should only contain letters.")

    @property
    def last_name(self):
        """ Returns the last name in title case """
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        """ Saves the last name, but only if it is all letters or empty """
        if value.isalpha() or value == "":  # Letters or the default empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should only contain letters.")

    def __str__(self):
        """ Returns the person's data as comma-separated values """
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
    A class representing student data. It inherits the name properties from Person.

    Properties:
    - first_name (str): The student's first name.
    - last_name (str): The student's last name.
    - course_name (str): The name of the course the student is registered for.

    ChangeLog: (Who, When, What)
    GArdoin,11/22/2026,Created Class
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        """ This constructor sends the names to Person's constructor, then sets the course

        ChangeLog: (Who, When, What)
        GArdoin,11/22/2026,Created constructor

        :param first_name: string with the student's first name
        :param last_name: string with the student's last name
        :param course_name: string with the name of the course
        """
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name  # Uses the course_name setter below

    @property
    def course_name(self):
        """ Returns the course name """
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        """ Saves the course name if it has only letters, numbers, and spaces (or is empty) """
        if value.replace(" ", "").isalnum() or value == "":  # For example, "Python 100"
            self.__course_name = value
        else:
            raise ValueError("The course name can only have letters, numbers, and spaces.")

    def __str__(self):
        """ Returns the student's data as comma-separated values (overrides Person) """
        return f"{self.first_name},{self.last_name},{self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    GArdoin,11/22/2026,Changed functions to work with Student objects
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads a list of dictionary rows from a JSON file,
        then turns each row into a Student object

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        GArdoin,11/22/2026,Converted dictionary rows into Student objects

        :param file_name: string with the name of the file to read from
        :param student_data: list to be filled with Student objects
        :return: list of Student objects
        """
        file = None  # Holds a reference to an opened file.
        try:
            file = open(file_name, "r")
            json_students = json.load(file)  # A list of dictionary rows

            # Turn each dictionary row into a Student object
            for row in json_students:
                student = Student(first_name=row["FirstName"],
                                  last_name=row["LastName"],
                                  course_name=row["CourseName"])
                student_data.append(student)
        except FileNotFoundError as e:
            message = "The file " + file_name + " must exist before running this script!"
            IO.output_error_messages(message=message, error=e)
        except ValueError as e:
            message = "One of the rows in " + file_name + " has data that is not valid!"
            IO.output_error_messages(message=message, error=e)
        except Exception as e:
            message = "There was a non-specific error while reading the file!"
            IO.output_error_messages(message=message, error=e)
        finally:
            # Close the file if it is still open
            if file is not None and file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function turns each Student object into a dictionary row,
        writes the rows to a JSON file, then shows what was written

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        GArdoin,11/22/2026,Converted Student objects into dictionary rows

        :param file_name: string with the name of the file to write to
        :param student_data: list of Student objects to be written to the file
        :return: None
        """
        file = None  # Holds a reference to an opened file.
        try:
            # Turn each Student object into a dictionary row
            json_students: list = []
            for student in student_data:
                row = {"FirstName": student.first_name,
                       "LastName": student.last_name,
                       "CourseName": student.course_name}
                json_students.append(row)

            file = open(file_name, "w")
            json.dump(json_students, file, indent=2)
            file.close()
            print("The following data was saved to file!")
            IO.output_student_courses(student_data=student_data)
        except TypeError as e:
            IO.output_error_messages(message="Please check that the data is a valid JSON format", error=e)
        except Exception as e:
            message = "There was a non-specific error while saving the file!\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            # Close the file if it is still open
            if file is not None and file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    GArdoin,11/22/2026,Changed functions to work with Student objects
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error message to the user,
        plus the technical details when an error is passed in

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with the message to show the user
        :param error: the Exception object with the technical details (optional)
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param menu: string with the menu text to show
        :return: None
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(message=e.__str__())  # No technical message is needed here
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays each student's data as comma-separated values

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        GArdoin,11/22/2026,Used the Student object's __str__() method

        :param student_data: list of Student objects to be displayed
        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(student)  # print() calls the Student's __str__() method
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets a student's first name, last name, and course name,
        then adds a new Student object to the list

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        GArdoin,11/22/2026,Created a Student object instead of a dictionary

        :param student_data: list of Student objects to add the new student to
        :return: list of Student objects
        """
        try:
            student = Student()  # Starts with empty names and course
            # Each line below runs a property setter, which checks the value
            student.first_name = input("Enter the student's first name: ")
            student.last_name = input("Enter the student's last name: ")
            student.course_name = input("Please enter the name of the course: ")
            student_data.append(student)
            print(f"You have registered {student.first_name} {student.last_name} "
                  f"for {student.course_name}.")
        except ValueError as e:
            message = "One of the values was not entered correctly!"
            IO.output_error_messages(message=message, error=e)
        except Exception as e:
            message = "There was a non-specific error with the data you entered!"
            IO.output_error_messages(message=message, error=e)
        return student_data


# Beginning of the main body of this script
# When the program starts, read the file data into a list of Student objects
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
