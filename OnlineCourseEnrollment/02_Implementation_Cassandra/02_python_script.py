import random
from faker import Faker

# Initialize Faker for generating random names and emails
fake = Faker()

# Set a random seed for consistency across different runs and systems
random.seed(42)
fake.seed_instance(42)

# File to save the generated CQL script
output_file = "/Users/harshasaijagu/Downloads/Course Work/BigData/MidSem Project/Data/insert_data_cql.cql"

# Predefined course and category names with relevant mappings
course_topics = [
    ("Data Science", "Technology"), 
    ("Machine Learning", "Technology"), 
    ("Artificial Intelligence", "Technology"), 
    ("Cloud Computing", "Technology"),
    ("Cybersecurity", "Technology"),
    ("Blockchain", "Finance"),
    ("Digital Marketing", "Business"),
    ("Project Management", "Business"),
    ("Health Informatics", "Health"),
    ("Biotechnology", "Science"),
    ("Web Development", "Technology"),
    ("Mobile App Development", "Technology"),
    ("Graphic Design", "Arts"),
    ("Finance Management", "Finance"),
    ("Public Health", "Health")
]

categories = ["Technology", "Business", "Health", "Science", "Arts", "Education", "Finance"]

# Function to generate random names and emails
def random_name():
    return fake.name()

def random_email(firstname, lastname):
    return f"{firstname.lower()}.{lastname.lower()}@example.com"

# Generate a unified enrollment data set
def generate_enrollment_data(student_count, course_count):
    enrollment_data = []
    for student_id in range(1, student_count + 1):
        enrolled_courses = random.sample(range(1, course_count + 1), random.randint(3, 4))  # 3-4 courses per student
        for course_id in enrolled_courses:
            enrollment_date = fake.date_this_year()
            course_name = course_topics[course_id % len(course_topics)][0]
            instructor_id = random.randint(1, 25)
            category_name = course_topics[course_id % len(course_topics)][1]
            category_id = categories.index(category_name) + 1
            firstname = fake.first_name()
            lastname = fake.last_name()
            email = random_email(firstname, lastname)
            
            enrollment_data.append({
                "student_id": student_id,
                "course_id": course_id,
                "enrollment_date": enrollment_date,
                "course_name": course_name,
                "instructor_id": instructor_id,
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "category_id": category_id,
                "category_name": category_name
            })
    return enrollment_data

# Generate CQL queries based on the unified enrollment data
def generate_cql_queries(enrollment_data):
    cql_statements = []

    # Queries for courses_by_student
    for record in enrollment_data:
        cql_statements.append(f"INSERT INTO courses_by_student (studentid, courseid, enrollment_date, coursename, instructorid) "
                              f"VALUES ({record['student_id']}, {record['course_id']}, '{record['enrollment_date']}', "
                              f"'{record['course_name']}', {record['instructor_id']});")

    # Queries for students_by_course
    for record in enrollment_data:
        cql_statements.append(f"INSERT INTO students_by_course (courseid, studentid, enrollment_date, firstname, lastname, email) "
                              f"VALUES ({record['course_id']}, {record['student_id']}, '{record['enrollment_date']}', "
                              f"'{record['firstname']}', '{record['lastname']}', '{record['email']}');")

    # Queries for enrollments_by_course
    for record in enrollment_data:
        cql_statements.append(f"INSERT INTO enrollments_by_course (courseid, enrollment_date, studentid) "
                              f"VALUES ({record['course_id']}, '{record['enrollment_date']}', {record['student_id']});")

    return cql_statements

def insert_instructors_by_course(course_count):
    cql_statements = []
    for course_id in range(1, course_count + 1):
        instructor_id = random.randint(1, 25)
        instructor_name = random_name()
        course_name = course_topics[course_id % len(course_topics)][0]
        bio = f"Experienced in {course_name} with a rich teaching background."
        cql_statements.append(f"INSERT INTO instructors_by_course (courseid, instructorid, name, bio) "
                              f"VALUES ({course_id}, {instructor_id}, '{instructor_name}', '{bio}');")
    return cql_statements

def insert_courses_by_category(course_count):
    cql_statements = []
    for course_id in range(1, course_count + 1):
        category_name = course_topics[course_id % len(course_topics)][1]
        category_id = categories.index(category_name) + 1
        course_name = course_topics[course_id % len(course_topics)][0]
        description = f"Fundamentals of {course_name.lower()}."
        cql_statements.append(f"INSERT INTO courses_by_category (categoryid, courseid, coursename, description) "
                              f"VALUES ({category_id}, {course_id}, '{course_name}', '{description}');")
    return cql_statements

# Main function to generate the CQL script
def generate_cql_script():
    try:
        # Initialize the script content
        cql_script = []

        # Generate unified enrollment data
        enrollment_data = generate_enrollment_data(500, 30)

        # Generate CQL queries from enrollment data
        cql_script += generate_cql_queries(enrollment_data)

        # Generate additional queries for other tables
        cql_script += insert_instructors_by_course(30)
        cql_script += insert_courses_by_category(30)

        # Write the generated CQL script to a file
        with open(output_file, 'w') as f:
            for statement in cql_script:
                f.write(statement + '\n')

        print(f"CQL script generated successfully! Saved as {output_file}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    generate_cql_script()
