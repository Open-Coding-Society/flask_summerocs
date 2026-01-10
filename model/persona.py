from __init__ import app, db
from sqlalchemy import JSON
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

# Persona categories - different domains/types of archetypes
PERSONA_CATEGORIES = [
    'student',      # Computer Science student learning archetypes (technologist, scrummer, planner, closer)
    'social',       # Social interest archetypes (gamer, musician, athlete, explorer, foodie, artist)
    'achievement',  # Achievement-oriented archetypes (builder, innovator, competitor, mentor)
    'fantasy'       # Superhero/superpower archetypes (speed, strength, intelligence, flight)
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
        
        """Social interest personas for teen engagement"""
        
        # Gamer Persona
        s1 = Persona(
            _alias='pixel',
            _category='social',
            _title='Gamer',
            _bio='I live for the rush of competition and the thrill of leveling up. Gaming is where I connect with friends, strategize, and express myself. Whether it\'s esports, RPGs, or casual mobile games, I find community and purpose in virtual worlds.',
            _archetype=['Competitive', 'Strategic', 'Connected'],
            _personality_type=['Team Player', 'Problem Solver'],
            _says=['Did you see that clutch play?', 'We should squad up later.', 'I just hit Diamond rank!'],
            _thinks=['Gaming teaches real skills like teamwork and quick thinking.', 'My online friends understand me better than most IRL people.'],
            _feels=['Most alive when in the zone during intense matches.', 'Frustrated when people dismiss gaming as just entertainment.'],
            _does=['Streams gameplay or watches Twitch/YouTube gaming content.', 'Analyzes strategies and optimizes character builds.', 'Coordinates with teammates across time zones.']
        )
        
        # Musician Persona
        s2 = Persona(
            _alias='melody',
            _category='social',
            _title='Musician',
            _bio='Music is my language and my escape. I express emotions through sound, whether creating beats, playing instruments, or curating the perfect playlist. Music connects me to culture, identity, and community in ways words cannot.',
            _archetype=['Creative', 'Expressive', 'Passionate'],
            _personality_type=['Artist', 'Connector'],
            _says=['This song perfectly captures the vibe.', 'Want to hear what I\'ve been working on?', 'Music is everything to me.'],
            _thinks=['Different genres reflect different parts of my identity.', 'Creating music is how I process my feelings.'],
            _feels=['Energized by discovering new artists and sounds.', 'Vulnerable when sharing original work with others.'],
            _does=['Spends hours perfecting a track or practicing an instrument.', 'Makes playlists for every mood and occasion.', 'Attends concerts and connects with other musicians online.']
        )
        
        # Athlete Persona
        s3 = Persona(
            _alias='ace',
            _category='social',
            _title='Athlete',
            _bio='I thrive on movement, competition, and pushing my physical limits. Fitness isn\'t just exercise—it\'s discipline, confidence, and mental health. Whether team sports or solo workouts, I find strength in the grind and community in shared goals.',
            _archetype=['Driven', 'Disciplined', 'Energetic'],
            _personality_type=['Leader', 'Motivator'],
            _says=['No pain, no gain.', 'Let\'s hit the gym together.', 'I PR\'d today!'],
            _thinks=['Physical strength builds mental resilience.', 'My routine keeps me grounded and focused.'],
            _feels=['Accomplished after a tough workout or game.', 'Restless when unable to train or compete.'],
            _does=['Tracks progress with fitness apps and sets measurable goals.', 'Encourages friends to join workouts or sports.', 'Follows athletes and fitness influencers for inspiration.']
        )
        
        # Explorer Persona
        s4 = Persona(
            _alias='wanderlust',
            _category='social',
            _title='Explorer',
            _bio='I crave new experiences, cultures, and perspectives. Travel and adventure feed my curiosity about the world. Even locally, I seek hidden gems, try new foods, and collect stories that broaden my understanding of life.',
            _archetype=['Curious', 'Adventurous', 'Open-minded'],
            _personality_type=['Seeker', 'Storyteller'],
            _says=['I need to visit there someday.', 'Let\'s try that new place downtown.', 'Travel changes you.'],
            _thinks=['Every place has a story worth discovering.', 'Comfort zones are meant to be expanded.'],
            _feels=['Alive when exploring somewhere new.', 'Inspired by different cultures and perspectives.'],
            _does=['Plans trips and researches destinations obsessively.', 'Documents experiences through photos and journals.', 'Seeks out diverse foods, events, and communities.']
        )
        
        """Achievement-oriented personas for goal-driven matching"""
        
        # Builder Persona
        a1 = Persona(
            _alias='maker',
            _category='achievement',
            _title='Builder',
            _bio='I create tangible results. Whether coding projects, crafts, or engineering solutions, I love bringing ideas to life. My hands-on approach and practical mindset drive me to build things that work and matter.',
            _archetype=['Practical', 'Resourceful', 'Hands-on'],
            _personality_type=['Creator', 'Implementer'],
            _says=['Let me prototype that idea.', 'I built this from scratch.', 'How can we make this work?'],
            _thinks=['The best learning happens by doing.', 'Shipping is better than perfection.'],
            _feels=['Satisfied seeing projects come to completion.', 'Frustrated by endless planning without action.'],
            _does=['Jumps into implementation quickly.', 'Solves problems with creative workarounds.', 'Shares builds and creations with community.']
        )
        
        # Innovator Persona
        a2 = Persona(
            _alias='spark',
            _category='achievement',
            _title='Innovator',
            _bio='I see possibilities everywhere and challenge the status quo. Innovation drives me—finding better ways, asking "what if," and connecting unexpected ideas. I\'m energized by brainstorming and pushing boundaries.',
            _archetype=['Visionary', 'Bold', 'Unconventional'],
            _personality_type=['Ideator', 'Disruptor'],
            _says=['What if we tried this instead?', 'There has to be a better way.', 'Let\'s think outside the box.'],
            _thinks=['Innovation requires risk and experimentation.', 'Traditional approaches often miss opportunities.'],
            _feels=['Excited by novel ideas and emerging trends.', 'Constrained by rigid rules or conventional thinking.'],
            _does=['Researches cutting-edge technologies and methods.', 'Proposes creative solutions to old problems.', 'Experiments fearlessly, learning from failures.']
        )
        
        # Competitor Persona
        a3 = Persona(
            _alias='victor',
            _category='achievement',
            _title='Competitor',
            _bio='I\'m motivated by winning and being the best. Competition brings out my peak performance—I set ambitious goals, track rankings, and push myself to excel. Recognition and achievement fuel my drive.',
            _archetype=['Ambitious', 'Results-driven', 'Tenacious'],
            _personality_type=['Achiever', 'Champion'],
            _says=['I\'m going for first place.', 'Let\'s see who finishes first.', 'I don\'t settle for average.'],
            _thinks=['Competition reveals true potential.', 'Metrics and rankings show real progress.'],
            _feels=['Energized by challenges and high stakes.', 'Disappointed when effort doesn\'t yield top results.'],
            _does=['Enters competitions, hackathons, and contests.', 'Benchmarks performance against peers.', 'Celebrates wins and analyzes losses for improvement.']
        )
        
        # Mentor Persona
        a4 = Persona(
            _alias='sage',
            _category='achievement',
            _title='Mentor',
            _bio='I find purpose in helping others succeed. Sharing knowledge, guiding peers, and seeing others grow gives me deep satisfaction. My achievement is measured by the impact I have on my community.',
            _archetype=['Supportive', 'Wise', 'Patient'],
            _personality_type=['Guide', 'Nurturer'],
            _says=['Let me help you with that.', 'Have you considered this approach?', 'Your success is my success.'],
            _thinks=['Teaching reinforces my own understanding.', 'Lifting others elevates the whole community.'],
            _feels=['Fulfilled when helping someone overcome obstacles.', 'Proud seeing mentees achieve their goals.'],
            _does=['Offers tutoring and peer support regularly.', 'Creates guides and resources for others.', 'Listens actively and provides thoughtful feedback.']
        )
        
        """Fantasy superpower personas for aspirational matching"""
        
        # Speed Persona
        f1 = Persona(
            _alias='flash',
            _category='fantasy',
            _title='Speedster',
            _bio='If I had a superpower, it would be super speed—getting things done fast, responding instantly, and never wasting time. I value efficiency, quick thinking, and staying ahead of the curve.',
            _archetype=['Fast-paced', 'Responsive', 'Efficient'],
            _personality_type=['Executor', 'Quick-thinker'],
            _says=['Let\'s move quickly on this.', 'Time is precious.', 'I already finished that.'],
            _thinks=['Speed and momentum create success.', 'Waiting around wastes opportunity.'],
            _feels=['Energized by rapid progress and quick wins.', 'Impatient with slow processes or delays.'],
            _does=['Completes tasks ahead of deadlines.', 'Multitasks and context-switches rapidly.', 'Optimizes workflows for maximum efficiency.']
        )
        
        # Strength Persona
        f2 = Persona(
            _alias='titan',
            _category='fantasy',
            _title='Powerhouse',
            _bio='If I had a superpower, it would be super strength—the ability to tackle the hardest challenges, carry heavy loads, and power through obstacles. I value resilience, determination, and raw capability.',
            _archetype=['Resilient', 'Powerful', 'Unstoppable'],
            _personality_type=['Force', 'Perseverer'],
            _says=['I can handle the tough stuff.', 'Bring on the challenge.', 'I don\'t give up easily.'],
            _thinks=['Strength comes from persistence and grit.', 'The hardest problems are the most rewarding.'],
            _feels=['Confident tackling difficult tasks others avoid.', 'Energized by overcoming major obstacles.'],
            _does=['Volunteers for the most challenging assignments.', 'Pushes through setbacks with determination.', 'Supports teammates who need heavy lifting.']
        )
        
        # Intelligence Persona
        f3 = Persona(
            _alias='oracle',
            _category='fantasy',
            _title='Mastermind',
            _bio='If I had a superpower, it would be super intelligence—solving complex problems, seeing patterns others miss, and mastering any subject. I value knowledge, strategy, and intellectual excellence.',
            _archetype=['Analytical', 'Strategic', 'Intellectual'],
            _personality_type=['Thinker', 'Strategist'],
            _says=['Let me analyze this first.', 'I see a pattern here.', 'Knowledge is power.'],
            _thinks=['Deep understanding beats surface-level knowing.', 'Strategic thinking prevents future problems.'],
            _feels=['Excited by intellectual puzzles and complex systems.', 'Frustrated by illogical approaches or ignorance.'],
            _does=['Researches thoroughly before making decisions.', 'Develops sophisticated strategies and plans.', 'Masters new concepts quickly through intense study.']
        )
        
        # Flight Persona
        f4 = Persona(
            _alias='soar',
            _category='fantasy',
            _title='Visionary',
            _bio='If I had a superpower, it would be flight—seeing the big picture from above, rising above limitations, and reaching new heights. I value perspective, freedom, and boundless possibility.',
            _archetype=['Big-picture', 'Optimistic', 'Limitless'],
            _personality_type=['Dreamer', 'Inspirer'],
            _says=['Imagine the possibilities.', 'Let\'s aim higher.', 'The sky\'s not the limit.'],
            _thinks=['Perspective changes everything.', 'Limitations are often self-imposed.'],
            _feels=['Inspired by ambitious visions and bold goals.', 'Confined by narrow thinking or small dreams.'],
            _does=['Sets audacious goals that inspire others.', 'Sees connections across different domains.', 'Encourages teams to think beyond constraints.']
        )
        
        personas = [p1, p2, p3, p4, s1, s2, s3, s4, a1, a2, a3, a4, f1, f2, f3, f4]
        
        for persona in personas:
            try:
                persona.create()
                print(f"Created persona: {persona._title} ({persona._alias}) - {persona._category}")
            except IntegrityError:
                db.session.rollback()
                print(f"Persona already exists: {persona._alias}")
