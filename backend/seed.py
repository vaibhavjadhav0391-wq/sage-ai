from app.core.database import SessionLocal, Base, engine
from app.models.student import Student
from app.models.concept import Concept
from app.models.student_concept import StudentConcept
from app.models.interaction import Interaction
from app.models.lesson import Lesson

print('Connecting to Railway MySQL...')
Base.metadata.create_all(bind=engine)
print('Tables created!')

db = SessionLocal()

existing = db.query(Student).filter(Student.id == 1).first()
if not existing:
    s = Student(id=1, name='Demo Student', level='beginner')
    db.add(s)
    db.flush()
    print('Student added.')
else:
    print('Student already exists.')

existing_c = db.query(Concept).filter(Concept.id == 1).first()
if not existing_c:
    c = Concept(
        id=1,
        name='Java Arrays',
        subject='Java',
        description='Arrays in Java programming',
        difficulty='easy'
    )
    db.add(c)
    db.flush()
    print('Concept added.')
else:
    print('Concept already exists.')

existing_sc = db.query(StudentConcept).filter_by(student_id=1, concept_id=1).first()
if not existing_sc:
    sc = StudentConcept(student_id=1, concept_id=1, mastery_score=0.0, attempts=0)
    db.add(sc)
    print('StudentConcept added.')
else:
    print('StudentConcept already exists.')

db.commit()
db.close()
print('Done! Database seeded successfully!')

