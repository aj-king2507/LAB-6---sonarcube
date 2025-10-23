def student_module():
    print("=== Software Security Module Marks Entry ===")

    coursework_marks = []
    total_coursework = 0
    for i in range(1, 5):
        while True:
            try:
                mark = float(input(f"Enter marks for Coursework {i} (out of 25): "))
                if 0 <= mark <= 25:
                    coursework_marks.append(mark)
                    total_coursework += mark
                    break
                else:
                    print("Invalid input. Please enter a mark between 0 and 25.")
            except ValueError:
                print(" Please enter a valid number.")

    while True:
        try:
            exam_mark = float(input("Enter marks for Exam (out of 100): "))
            if 0 <= exam_mark <= 100:
                break
            else:
                print("Invalid input. Please enter a mark between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    total_marks = total_coursework + exam_mark
    max_marks = (4 * 25) + 100 # 200 total

    percentage = (total_marks / max_marks) * 100

    print("\n=== Results ===")
    for i, mark in enumerate(coursework_marks, start=1):
        print(f"Coursework {i}: {mark}/25")
    print(f"Exam: {exam_mark}/100")
    print(f"Total Marks: {total_marks}/{max_marks}")
    print(f"Percentage: {percentage:.2f}%")

if __name__ == "__main__":
    student_module()