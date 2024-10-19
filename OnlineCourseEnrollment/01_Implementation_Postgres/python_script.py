import random
from faker import Faker

# Initialize Faker for generating random names and emails
fake = Faker()

# Set a random seed for consistency across different runs and systems
random.seed(42)
fake.seed_instance(42)

# File to save the generated SQL script
output_file = "/Users/harshasaijagu/Downloads/Course Work/BigData/MidSem Project/Data/insert_data.sql"

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

# Relevant instructor bios based on the course topics
def generate_bio(course_name):
    bios = {
        "Data Science": "An experienced data scientist with a decade of experience in analyzing large datasets and building predictive models.",
        "Machine Learning": "A researcher specializing in deep learning algorithms and artificial neural networks with years of teaching experience.",
        "Artificial Intelligence": "An AI expert focusing on machine learning, natural language processing, and robotics.",
        "Cloud Computing": "A cloud architect who has helped numerous companies transition to cloud platforms like AWS and Azure.",
        "Cybersecurity": "A cybersecurity consultant with expertise in ethical hacking, vulnerability assessment, and security architecture.",
        "Blockchain": "A blockchain developer with years of experience working on decentralized applications and cryptocurrency platforms.",
        "Digital Marketing": "A digital marketing expert, helping businesses grow their online presence with SEO, SEM, and content marketing.",
        "Project Management": "A certified project management professional with over 15 years of experience leading large-scale projects.",
        "Health Informatics": "A specialist in the intersection of health and technology, with experience in implementing health information systems.",
        "Biotechnology": "A biotechnologist with research experience in gene editing, pharmacology, and bioengineering.",
        "Web Development": "A full-stack developer with a deep understanding of front-end and back-end web technologies.",
        "Mobile App Development": "An app developer with a focus on building high-quality mobile applications for Android and iOS.",
        "Graphic Design": "An expert graphic designer with a creative approach to branding, typography, and visual storytelling.",
        "Finance Management": "A finance consultant with expertise in financial analysis, risk management, and corporate finance.",
        "Public Health": "A public health professional with experience in epidemiology, community health, and policy development."
    }
    return bios.get(course_name, "An expert in their field with years of experience.")  # Default bio

# Function to generate random names and emails
def random_name():
    return fake.name()

def random_email(firstname, lastname):
    return f"{firstname.lower()}.{lastname.lower()}@example.com"

# Generate random data for the tables and save as SQL script
def insert_instructors(n):
    sql_statements = []
    for _ in range(n):
        name = random_name()
        # Randomly choose a course to assign a bio
        course_name = random.choice(course_topics)[0]
        bio = generate_bio(course_name)
        escaped_bio = bio.replace("'", "''")
        sql_statements.append(f"INSERT INTO online_learning_schema.instructors (name, bio) VALUES ('{name}', '{escaped_bio}');")
    return sql_statements

def insert_categories(n):
    sql_statements = []
    for category in categories:
        sql_statements.append(f"INSERT INTO online_learning_schema.categories (categoryname) VALUES ('{category}');")
    return sql_statements

def insert_courses(n, instructor_count, category_count):
    sql_statements = []
    for i in range(n):
        course_name, category_name = course_topics[i % len(course_topics)]  # Cycle through predefined topics
        instructor_id = random.randint(1, instructor_count)
        description = f"This course covers the fundamentals of {course_name.lower()}."
        escaped_description = description.replace("'", "''")
        
        # Find the category ID for the category
        category_id = categories.index(category_name) + 1
        
        sql_statements.append(f"INSERT INTO online_learning_schema.courses (coursename, instructorid, description, categoryid) "
                              f"VALUES ('{course_name}', {instructor_id}, '{escaped_description}', {category_id});")
    return sql_statements

def insert_students(n):
    sql_statements = []
    for _ in range(n):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = random_email(firstname, lastname)
        sql_statements.append(f"INSERT INTO online_learning_schema.students (firstname, lastname, email) "
                              f"VALUES ('{firstname}', '{lastname}', '{email}');")
    return sql_statements

def insert_enrollments(student_count, course_count):
    sql_statements = []
    for student_id in range(1, student_count + 1):
        # Each student gets 3 to 4 random course enrollments
        enrolled_courses = random.sample(range(1, course_count + 1), random.randint(3, 4))
        for course_id in enrolled_courses:
            enrollment_date = fake.date_this_year()
            sql_statements.append(f"INSERT INTO online_learning_schema.enrollments (studentid, courseid, enrollmentdate) "
                                  f"VALUES ({student_id}, {course_id}, '{enrollment_date}');")
    return sql_statements

# Main function to generate the SQL script
def generate_sql_script():
    try:
        # Initialize the script content
        sql_script = []

        # Generate INSERT statements for each table
        sql_script += insert_instructors(25)
        sql_script += insert_categories(7)
        sql_script += insert_courses(30, 25, 7)
        sql_script += insert_students(500)
        sql_script += insert_enrollments(500, 30)

        # Write the generated SQL script to a file
        with open(output_file, 'w') as f:
            for statement in sql_script:
                f.write(statement + '\n')

        print(f"SQL script generated successfully! Saved as {output_file}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    generate_sql_script()
