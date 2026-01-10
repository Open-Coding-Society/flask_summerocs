from __init__ import app, db
from sqlalchemy import JSON
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

# Persona categories - different domains/types of archetypes
PERSONA_CATEGORIES = [
    'student',    # Computer Science student learning archetypes (technologist, scrummer, planner, closer)
    'social',     # Dating/matchmaking personality archetypes
    'fantasy'     # Superhero/superpower archetypes
]

class Persona(db.Model):
    __tablename__ = 'personas'

    id = db.Column(db.Integer, primary_key=True)
    _category = db.Column(db.String(32), nullable=False)
    _alias = db.Column(db.String(32), unique=True, nullable=False)
    _title = db.Column(db.String(64), nullable=False)
    _bio = db.Column(db.Text, nullable=False)
    _archetype = db.Column(JSON, nullable=False)
    _personality_type = db.Column(JSON, nullable=True)
    _says = db.Column(JSON, nullable=True)
    _thinks = db.Column(JSON, nullable=True)
    _feels = db.Column(JSON, nullable=True)
    _does = db.Column(JSON, nullable=True)
    

    def __init__(self, _alias, _title, _bio, _archetype, _category, _personality_type=None, _says=None, _thinks=None, _feels=None, _does=None):
        self._alias = _alias
        self._title = _title
        self._bio = _bio
        self._archetype = _archetype
        self._category = _category
        self._personality_type = _personality_type
        self._says = _says
        self._thinks = _thinks
        self._feels = _feels
        self._does = _does

    @validates('_category')
    def validate_category(self, key, value):
        if value not in PERSONA_CATEGORIES:
            raise ValueError(f"Invalid category '{value}'. Must be one of: {', '.join(PERSONA_CATEGORIES)}")
        return value

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        return {
            "id": self.id,
            "category": self._category,
            "alias": self._alias,
            "title": self._title,
            "bio": self._bio,
            "archetype": self._archetype,
            "personality_type": self._personality_type,
            "says": self._says,
            "thinks": self._thinks,
            "feels": self._feels,
            "does": self._does
        }


"""Database Creation and Testing"""

def initPersonas():
    """Initialize persona database with student archetype empathy maps."""
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        
        """Student archetype personas for team matching"""
        
        # Technologist Persona - Indy
        p1 = Persona(
            _alias='indy',
            _category='student',
            _title='Technologist',
            _bio='I am a driven CS student who enjoys individual work and tackling the hardest technical challenges. I am motivated by mastery and recognition, and often surprise others with exceptional problem-solving skills. I excel in individual assignments and competitions, but group work can be frustrating, especially when team members are less focused on code or schedules are unclear. Building trust and communication with peers is an ongoing challenge, but when I am engaged, I can elevate the whole project.',
            _archetype=['Introvert', 'Analytical', 'Independent'],
            _personality_type=['Ambitious', 'Focused'],
            _says=[
                'Look at this new feature I created.',
                'I just want to ask you and be sure to get it right.',
                "Those people can't help me, they don't understand themselves."
            ],
            _thinks=[
                'Prefers not to seek help from students, perceiving it as a potential slowdown.',
                'Secretly hopes to be a hero, one who makes the project exceptional.',
                'Believes the teacher is a valuable resource, but also recognizes the importance of self-driven learning for unlimited potential.'
            ],
            _feels=[
                'Values individual effort, but is open to building trust and communication with peers.',
                'Often feels excluded due to language difficulties or social barriers.',
                'Fears opening up or communicating with others or trusting they will complete tasks correctly.'
            ],
            _does=[
                'Often wants to come in before or stay after class for preferred individual review or help with Teacher.',
                "When properly engaged, often surprises others' expectations by solving cognitively challenging problems.",
                'Typically does well on traditional assignments, like AP exams or practices.',
                'Can loop or get frustrated on materials they have not been able to grasp, sometimes compounded by not reaching out to peers early.'
            ]
        )
        
        # Scrummer Persona - Salem
        p2 = Persona(
            _alias='salem',
            _category='student',
            _title='Scrummer',
            _bio='I am a collaborative learner who grows through teamwork and iteration. I enjoy working in teams, contributing to group success, and learning from others. Seeing my team each day makes me happy and excited to solve problems together. While I thrive in Agile environments, I sometimes find it challenging to show my unique contributions and can be unsure how my individual work impacts my grade, especially when groupthink makes it easy to blend in with the team.',
            _archetype=['Collaborative', 'Optimistic', 'Team-oriented'],
            _personality_type=['Agile', 'Growth Mindset'],
            _says=[
                'I like working in teams and collaborating with peers.',
                "It is OK that we don't get things right as we have iteration opportunities."
            ],
            _thinks=[
                'Believes in team and has a growth mindset.',
                'Sometimes is unsure how their individual work impacts their grade in class.'
            ],
            _feels=[
                'Thinks about solving issues together.',
                'Hopes to get things done through group effort.',
                'Feels happy and excited to see team each day.'
            ],
            _does=[
                'Is engaged in team conversations.',
                'Is actively involved in Agile Ceremonies.',
                'Often starts discussing or solving problems before all directions are completed.',
                'Some scrummers allow the overshadow of team accomplishments to be an excuse for poor individual contribution.'
            ]
        )
        
        # Planner Persona - Phoenix
        p3 = Persona(
            _alias='phoenix',
            _category='student',
            _title='Planner',
            _bio='I am an organized CS student who excels at planning, tracking, and communicating with my team. I champion process management and issue tracking, and I am motivated by seeing a comprehensive plan come together. I gain satisfaction from seeing projects that are working and highly functional. Sometimes, I struggle to balance planning with hands-on technical work, especially when there is a lot to organize or integrate.',
            _archetype=['Organized', 'Detail-oriented', 'Strategic'],
            _personality_type=['Process Manager', 'Communicator'],
            _says=[
                'It is satisfying seeing something I worked on become useful.',
                'I have read every detail written with exactness.',
                'I notice these inconsistencies in requirements.'
            ],
            _thinks=[
                'Believes a comprehensive plan should incorporate all requirements.',
                'Thinks they need to read all provided information.',
                'Desires feedback from team members on accomplishments related to plan.'
            ],
            _feels=[
                'Feels responsibility for communicating plans with others.',
                'Hopes that all team members will do their assigned portion of the work.'
            ],
            _does=[
                'Often a champion of issue tracking and kanban boards.',
                'Seeks guidance on issues that present barriers or impede progress on the plan.',
                'Seeks opportunities for the instructor to let them lead larger classroom projects or prepare for seminar activities like AP Testing.',
                'Sometimes struggles with prioritizing coding, as there is always so much to organize, plan, or integrate.'
            ]
        )
        
        # Closer Persona - Cody
        p4 = Persona(
            _alias='cody',
            _category='student',
            _title='Closer',
            _bio='I am a detail-oriented CS student who thrives on completing tasks and meeting milestones. I feel most confident when requirements are clear and feedback is available, and I take pride in finishing work efficiently. While I excel in structured environments, I may hesitate or feel anxious with open-ended assignments. Seeking confirmation from teachers or peers helps me stay on track and achieve success.',
            _archetype=['Detail-oriented', 'Driven', 'Perfectionist'],
            _personality_type=['Finisher', 'Reliable'],
            _says=[
                'It makes me happy to finish tasks.',
                'I listened to your instructions, do you think my idea is OK?',
                'Here is my work after our last conversation, does it meet the requirements?'
            ],
            _thinks=[
                'Focuses on how tasks map to requirements.',
                'Worries about meeting exact grade requirements.',
                'Thinks of long term success, often beyond classroom (ie career and college).'
            ],
            _feels=[
                'Hopes to achieve a path to success by obtaining extra assurances.',
                'Feel confident and satisfied when coding and meeting requirements on vetted issues and meeting milestones.',
                'Desires to be active collaborator and communicator.'
            ],
            _does=[
                'Quickly acts on well-defined plans and completes technical work efficiently.',
                'Regularly meets personal and project milestones.',
                'Seeks to be first in line for preliminary reviews, but will trend toward back of line on summative reviews.',
                'Seeks confirmation from teachers or peers before moving on to the next task.',
                'May get stuck or hesitate when faced with open-ended or creative assignments.'
            ]
        )
        
        personas = [p1, p2, p3, p4]
        
        for persona in personas:
            try:
                persona.create()
                print(f"Created persona: {persona._title} ({persona._alias})")
            except IntegrityError:
                db.session.rollback()
                print(f"Persona already exists: {persona._alias}")
