import tkinter as tk
import re
from classroom_functions import ClassroomApp
from tkinter import messagebox


def validate_input(text):
    """
        Validates the inputted text
        Arguments:
        - text (str): text for validation
        Returns:
        - Bool: if text only contains letters and proper punctuation True, otherwise False
        """
    return re.match("^[A-Za-z -]*$", text) is not None


def open_classroom():
    """
    Opens a new window for the classrooms
    """
    selected_classroom = classroom_var.get()
    if selected_classroom != 0:
        new_window = tk.Toplevel(root)
        new_window.title("Classroom " + str(selected_classroom))
        new_window.geometry("500x500")
        new_window.resizable(False, False)

        back_button = tk.Button(new_window, text="Back", command=new_window.destroy)
        back_button.pack()

        add_label = tk.Label(new_window, text="Enter student's name:")
        add_label.pack()

        add_entry = tk.Entry(new_window)
        add_entry.pack()

        def add_student():
            selected_classroom_students = classroom.get_students_list(selected_classroom)
            if len(selected_classroom_students) < 3:
                name = add_entry.get()

                if validate_input(name):
                    added_successfully = classroom.add_name_to_csv(name, selected_classroom)
                    add_entry.delete(0, tk.END)  # Clear the entry after adding the name

                    if added_successfully:
                        print(f"Name '{name}' added to 'classroom_{selected_classroom}.csv'.")
                    else:
                        messagebox.showinfo("Error", "Maximum students limit reached for this classroom.")
                else:
                    messagebox.showinfo("Error", "Please enter only letters and hyphens.")

        add_button = tk.Button(new_window, text="Add", command=add_student)
        add_button.pack()

        remove_label = tk.Label(new_window, text="Enter student's name to remove:")
        remove_label.pack()

        remove_entry = tk.Entry(new_window)
        remove_entry.pack()

        def remove_student():
            name = remove_entry.get()
            remove_entry.delete(0, tk.END)  # Clear the entry after removing the name
            print(f"Name '{name}' removed from 'classroom_{selected_classroom}.csv'.")

        remove_button = tk.Button(new_window, text="Remove", command=remove_student)
        remove_button.pack()

        def update_students_list():
            students_list.delete(0, tk.END)
            classroom_data = classroom.get_students_list(selected_classroom)
            for student in classroom_data:
                students_list.insert(tk.END, student)

        students_list_label = tk.Label(new_window, text="Students in Classroom:")
        students_list_label.pack()

        students_list = tk.Listbox(new_window, width=40, height=10)
        students_list.pack()

        update_students_list()

    def refresh_students():
        update_students_list()
        update_dropdown()

    update_button = tk.Button(new_window, text="Update", command=refresh_students)
    update_button.pack()

    update_students_list()

    def update_dropdown():
        students_dropdown['menu'].delete(0, 'end')  # Clear previous names
        classroom_data = classroom.get_students_list(selected_classroom)
        for student in classroom_data:
            students_dropdown['menu'].add_command(label=student, command=tk._setit(selected_student, student))

    def get_selected_student():
        print("Selected student:", selected_student.get())

    students_dropdown_label = tk.Label(new_window, text="Select a student:")
    students_dropdown_label.pack()

    selected_student = tk.StringVar(new_window)
    students_dropdown = tk.OptionMenu(new_window, selected_student, "")
    students_dropdown.pack()

    update_dropdown()

    selected_student.trace('w', get_selected_student)

    def grade_student():
        global new_window
        selected = selected_student.get()
        if selected:
            new_window = tk.Toplevel(root)
            new_window.title(selected)
            new_window.geometry("400x400")
            new_window.resizable(False, False)

            back_button = tk.Button(new_window, text="Back", command=new_window.destroy)
            back_button.pack()

            grade_label = tk.Label(new_window, text="Enter grade:")
            grade_label.pack()

            grade_entry = tk.Entry(new_window)
            grade_entry.pack()

            def add_grade():
                grade = grade_entry.get()

                if re.match(r'^\d+(\.\d+)?$', grade):
                    classroom.add_grade_to_student(selected, grade)
                    print(f"Grade '{grade}' added for '{selected}'")
                    grade_entry.delete(0, tk.END)  # Clear the entry after adding the grade
                else:
                    messagebox.showinfo("Error", "Please enter only numbers or dot for grade.")

            add_grade_button = tk.Button(new_window, text="Add Grade", command=add_grade)
            add_grade_button.pack()

            student_grades = classroom.get_student_grades(selected)
            grades_listbox = tk.Listbox(new_window)
            grades_listbox.pack()
            for grade in student_grades:
                grades_listbox.insert(tk.END, grade)

        def update_grades():
            selected = selected_student.get()
            if selected:
                grades_listbox.delete(0, tk.END)
                student_grades = classroom.get_student_grades(selected)
                for grade in student_grades:
                    grades_listbox.insert(tk.END, grade)

        def remove_grade():
            selected_grade = grades_listbox.get(tk.ACTIVE)
            classroom.remove_grade_from_student(selected, selected_grade)
            update_grades()  # Refresh displayed grades after removal

        remove_grade_button = tk.Button(new_window, text="Remove Grade", command=remove_grade)
        remove_grade_button.pack()

        update_grades_button = tk.Button(new_window, text="Update", command=update_grades)
        update_grades_button.pack()

    grade_button = tk.Button(new_window, text="Grade", command=grade_student)
    grade_button.pack()


root = tk.Tk()
root.title("Classroom Selection")
root.geometry("400x300")
root.resizable(False, False)

label = tk.Label(root, text="Select a classroom:")
label.pack()

classroom_var = tk.IntVar(value=0)
classroom = ClassroomApp()

for classroom_num in range(1, 5):
    classroom_button = tk.Radiobutton(root, text="Classroom " + str(classroom_num), variable=classroom_var,
                                      value=classroom_num)
    classroom_button.pack(anchor=tk.W)

go_button = tk.Button(root, text="Go to Classroom", command=open_classroom)
go_button.pack()

root.mainloop()
