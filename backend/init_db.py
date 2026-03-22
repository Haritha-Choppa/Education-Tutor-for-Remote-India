from app import create_app, db
from app.models.lesson import Lesson, PracticeProblem
from app.models.quiz import Quiz, QuizQuestion

def add_sample_data():
    """Add/extend sample lessons and quizzes for testing (idempotent)."""

    created_counts = {
        'lessons': 0,
        'practice_problems': 0,
        'quizzes': 0,
        'questions': 0
    }

    def get_or_create_lesson(payload):
        lesson = Lesson.query.filter_by(title=payload['title']).first()
        if lesson:
            lesson.description = payload['description']
            lesson.subject = payload['subject']
            lesson.grade_level = payload['grade_level']
            lesson.content = payload['content']
            lesson.order = payload['order']
            db.session.commit()
            return lesson
        lesson = Lesson(**payload)
        db.session.add(lesson)
        db.session.commit()
        created_counts['lessons'] += 1
        return lesson

    def get_or_create_practice_problem(payload):
        existing = PracticeProblem.query.filter_by(
            lesson_id=payload['lesson_id'],
            question=payload['question']
        ).first()
        if existing:
            return
        db.session.add(PracticeProblem(**payload))
        db.session.commit()
        created_counts['practice_problems'] += 1

    def get_or_create_quiz(payload):
        quiz = Quiz.query.filter_by(
            lesson_id=payload['lesson_id'],
            title=payload['title']
        ).first()
        if quiz:
            return quiz
        quiz = Quiz(**payload)
        db.session.add(quiz)
        db.session.commit()
        created_counts['quizzes'] += 1
        return quiz

    def get_or_create_quiz_question(payload):
        existing = QuizQuestion.query.filter_by(
            quiz_id=payload['quiz_id'],
            order=payload['order']
        ).first()
        if existing:
            return
        db.session.add(QuizQuestion(**payload))
        db.session.commit()
        created_counts['questions'] += 1

    lessons_data = [
        {
            'title': 'Introduction to Algebra',
            'description': 'Learn the basics of algebraic expressions and equations',
            'subject': 'Mathematics',
            'grade_level': 'Grade 8',
            'content': 'Variables represent unknown numbers, and equations let us solve for them using inverse operations.',
            'order': 1
        },
        {
            'title': 'Algebraic Equations and Inequalities',
            'description': 'Solve one-step and two-step equations and inequalities',
            'subject': 'Mathematics',
            'grade_level': 'Grade 8',
            'content': 'Use balancing methods and inverse operations to solve equations and represent solutions on a number line.',
            'order': 2
        },
        {
            'title': 'Linear Algebra Session 1: Vectors and Scalars',
            'description': 'Understand vector notation, magnitude, and direction',
            'subject': 'Mathematics',
            'grade_level': 'Grade 10',
            'content': (
                'Scalars have magnitude only, while vectors have both magnitude and direction.\n\n'
                'Core ideas:\n'
                '1. Vector notation in 2D and 3D\n'
                '2. Magnitude using distance formula\n'
                '3. Unit vectors and direction\n\n'
                'Real-world examples include velocity, displacement, and force.'
            ),
            'order': 3
        },
        {
            'title': 'Linear Algebra Session 2: Vector Operations',
            'description': 'Practice vector addition, subtraction, and scalar multiplication',
            'subject': 'Mathematics',
            'grade_level': 'Grade 10',
            'content': 'Add vectors component-wise, subtract by adding inverse vectors, and scale vectors by multiplying each component.',
            'order': 4
        },
        {
            'title': 'Linear Algebra Session 3: Matrices Basics',
            'description': 'Read, classify, and operate on matrices',
            'subject': 'Mathematics',
            'grade_level': 'Grade 10',
            'content': (
                'Matrices are rectangular arrays used to represent systems and transformations.\n\n'
                'What to learn:\n'
                '1. Matrix dimensions and notation\n'
                '2. Matrix addition/subtraction rules\n'
                '3. Scalar multiplication and matrix multiplication\n\n'
                'Use matrix operations to organize and solve many equations at once.'
            ),
            'order': 5
        },
        {
            'title': 'Linear Algebra Session 4: Determinants and Inverse Matrices',
            'description': 'Compute determinants and find inverse matrices for 2x2 cases',
            'subject': 'Mathematics',
            'grade_level': 'Grade 10',
            'content': 'Determinants indicate invertibility. A non-zero determinant means a square matrix has an inverse.',
            'order': 6
        },
        {
            'title': 'Linear Algebra Session 5: Systems of Linear Equations',
            'description': 'Solve systems using substitution, elimination, and matrix methods',
            'subject': 'Mathematics',
            'grade_level': 'Grade 10',
            'content': (
                'A system of equations may have one, none, or infinitely many solutions.\n\n'
                'Methods covered:\n'
                '1. Substitution\n'
                '2. Elimination\n'
                '3. Row-reduction with augmented matrices\n\n'
                'Always check the final solution in original equations.'
            ),
            'order': 7
        },
        {
            'title': 'Linear Algebra Session 6: Eigenvalues and Eigenvectors',
            'description': 'Explore eigen concepts and geometric interpretation',
            'subject': 'Mathematics',
            'grade_level': 'Grade 11',
            'content': 'Eigenvectors keep their direction under a matrix transformation while eigenvalues scale their magnitude.',
            'order': 8
        },
        {
            'title': 'Linear Algebra Session 7: Orthogonality and Projections',
            'description': 'Learn dot product, orthogonal vectors, and projection',
            'subject': 'Mathematics',
            'grade_level': 'Grade 11',
            'content': 'Orthogonal vectors have zero dot product, and projections decompose vectors into useful components.',
            'order': 9
        },
        {
            'title': 'Photosynthesis',
            'description': 'Understand how plants convert sunlight into energy',
            'subject': 'Biology',
            'grade_level': 'Grade 9',
            'content': (
                'Photosynthesis is the process by which green plants produce food using sunlight.\n\n'
                'Detailed flow:\n'
                '1. Chlorophyll in chloroplasts absorbs sunlight\n'
                '2. Water is absorbed through roots and transported to leaves\n'
                '3. Carbon dioxide enters through stomata\n'
                '4. Light-dependent reactions produce ATP and NADPH\n'
                '5. Calvin cycle uses ATP, NADPH, and CO2 to build glucose\n'
                '6. Oxygen is released as a byproduct\n\n'
                'Overall equation:\n'
                '6CO2 + 6H2O + light energy -> C6H12O6 + 6O2\n\n'
                'Importance:\n'
                '- Provides food for plants and the food chain\n'
                '- Releases oxygen needed for respiration\n'
                '- Supports energy flow in ecosystems'
            ),
            'order': 10
        },
        {
            'title': 'Cellular Respiration',
            'description': 'Learn how cells release energy from glucose',
            'subject': 'Biology',
            'grade_level': 'Grade 9',
            'content': 'Cellular respiration breaks down glucose to produce ATP through glycolysis, Krebs cycle, and electron transport.',
            'order': 11
        },
        {
            'title': 'Introduction to Calculus',
            'description': 'Understand limits, derivatives, and rates of change',
            'subject': 'Mathematics',
            'grade_level': 'Grade 11',
            'content': (
                'Calculus studies change and accumulation.\n\n'
                'Topics in this lesson:\n'
                '1. Limits and continuity\n'
                '2. Derivative as instantaneous rate of change\n'
                '3. Basic differentiation rules\n\n'
                'Calculus helps model motion, growth, optimization, and area.'
            ),
            'order': 12
        },
        {
            'title': 'Newton Laws of Motion',
            'description': 'Master force, mass, acceleration, and equilibrium',
            'subject': 'Physics',
            'grade_level': 'Grade 10',
            'content': (
                'Newton Laws explain how forces affect motion.\n\n'
                'Law summary:\n'
                '1. First law: inertia\n'
                '2. Second law: F = ma\n'
                '3. Third law: action-reaction pairs\n\n'
                'Use free-body diagrams to identify forces before solving problems.'
            ),
            'order': 13
        },
        {
            'title': 'Atomic Structure and Periodic Trends',
            'description': 'Understand atoms, electron configuration, and periodic table patterns',
            'subject': 'Chemistry',
            'grade_level': 'Grade 10',
            'content': (
                'Chemistry starts with the structure of atoms and how elements are organized.\n\n'
                'Main points:\n'
                '1. Protons, neutrons, and electrons\n'
                '2. Atomic number, mass number, and isotopes\n'
                '3. Valence electrons and periodic trends\n\n'
                'Across a period, atomic radius generally decreases and ionization energy increases.'
            ),
            'order': 14
        },
        {
            'title': 'Chemical Bonding and Compounds',
            'description': 'Compare ionic and covalent bonding with real examples',
            'subject': 'Chemistry',
            'grade_level': 'Grade 10',
            'content': (
                'Atoms form bonds to reach more stable electron arrangements.\n\n'
                'Focus areas:\n'
                '1. Ionic bonding through electron transfer\n'
                '2. Covalent bonding through electron sharing\n'
                '3. Naming simple compounds\n\n'
                'Metal + nonmetal often forms ionic compounds, while nonmetal + nonmetal typically forms covalent compounds.'
            ),
            'order': 15
        },
        {
            'title': 'Grammar and Sentence Structure',
            'description': 'Build strong sentence patterns for clear writing',
            'subject': 'English',
            'grade_level': 'Grade 9',
            'content': (
                'Clear writing depends on strong sentence structure and grammar.\n\n'
                'This lesson covers:\n'
                '1. Subject-verb agreement\n'
                '2. Simple, compound, and complex sentences\n'
                '3. Common punctuation rules\n\n'
                'Use commas to separate clauses carefully, and always check agreement between subject and verb.'
            ),
            'order': 16
        },
        {
            'title': 'English Communication for Workplace',
            'description': 'Write emails, reports, and presentations professionally',
            'subject': 'English',
            'grade_level': 'Professional',
            'content': (
                'Professional English helps in meetings, reports, and client communication.\n\n'
                'Skills in this lesson:\n'
                '1. Writing concise emails with clear subject lines\n'
                '2. Structuring reports with objective, analysis, and recommendation\n'
                '3. Using professional tone and active voice\n\n'
                'Clear communication improves teamwork, delivery quality, and career growth.'
            ),
            'order': 17
        },
        {
            'title': 'Organic Chemistry Fundamentals',
            'description': 'Learn hydrocarbons, functional groups, and basic reactions',
            'subject': 'Chemistry',
            'grade_level': 'Undergraduate',
            'content': (
                'Organic chemistry focuses on carbon-containing compounds and their reactions.\n\n'
                'Core topics:\n'
                '1. Bonding in carbon compounds\n'
                '2. Functional groups: alcohols, aldehydes, ketones, acids, amines\n'
                '3. Isomerism and nomenclature\n'
                '4. Reaction types: substitution, addition, elimination\n\n'
                'Understanding functional groups helps predict properties and reaction behavior.'
            ),
            'order': 18
        },
        {
            'title': 'Chemical Kinetics and Equilibrium',
            'description': 'Study reaction rates, equilibrium constants, and Le Chatelier principle',
            'subject': 'Chemistry',
            'grade_level': 'Undergraduate',
            'content': (
                'Chemical kinetics explains how fast reactions happen, while equilibrium explains extent.\n\n'
                'Concepts covered:\n'
                '1. Rate laws and reaction order\n'
                '2. Activation energy and catalysts\n'
                '3. Dynamic equilibrium and equilibrium constant (K)\n'
                '4. Le Chatelier principle under stress changes\n\n'
                'These ideas are widely used in industrial process optimization.'
            ),
            'order': 19
        },
        {
            'title': 'Engineering Mechanics: Statics',
            'description': 'Analyze forces, moments, and equilibrium in structures',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Statics is the study of bodies at rest under force systems.\n\n'
                'Topics:\n'
                '1. Free-body diagrams\n'
                '2. Force resolution in 2D and 3D\n'
                '3. Moments and couples\n'
                '4. Equilibrium equations for beams and frames\n\n'
                'Statics is foundational for civil, mechanical, and structural design.'
            ),
            'order': 20
        },
        {
            'title': 'Electrical Engineering: Circuit Analysis',
            'description': 'Use Ohm law, Kirchhoff laws, and network theorems',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Circuit analysis helps compute voltage, current, and power in electrical networks.\n\n'
                'You will learn:\n'
                '1. Ohm law and power formulas\n'
                '2. Kirchhoff current and voltage laws\n'
                '3. Series-parallel simplification\n'
                '4. Thevenin and Norton equivalents\n\n'
                'These methods are critical in electronics, power systems, and control engineering.'
            ),
            'order': 21
        },
        {
            'title': 'Engineering Drawing and CAD Basics',
            'description': 'Interpret technical drawings and basic CAD workflow',
            'subject': 'Engineering',
            'grade_level': 'Professional',
            'content': (
                'Engineering drawings communicate design intent with precision.\n\n'
                'Lesson coverage:\n'
                '1. Orthographic and isometric projections\n'
                '2. Dimensioning and tolerancing basics\n'
                '3. Sectional views and symbols\n'
                '4. Intro to CAD sketch and constraints\n\n'
                'Drawing literacy is essential for manufacturing, QA, and design collaboration.'
            ),
            'order': 22
        },
        {
            'title': 'Thermodynamics for Engineers',
            'description': 'Apply first and second law concepts to engineering systems',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Thermodynamics studies energy, heat, and work in engineering systems.\n\n'
                'Main ideas:\n'
                '1. System, surroundings, and properties\n'
                '2. First law: energy conservation\n'
                '3. Second law: entropy and direction of processes\n'
                '4. Basic cycles: Otto, Diesel, and Rankine\n\n'
                'Thermodynamics is used in engines, power plants, HVAC, and refrigeration design.'
            ),
            'order': 23
        },
        {
            'title': 'Fluid Mechanics Essentials',
            'description': 'Understand flow behavior, pressure, and continuity principles',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Fluid mechanics explains how liquids and gases behave under forces.\n\n'
                'Topics:\n'
                '1. Fluid properties and pressure\n'
                '2. Continuity and Bernoulli equation\n'
                '3. Laminar vs turbulent flow\n'
                '4. Pipe losses and pump power\n\n'
                'Applications include pipelines, water supply, aerodynamics, and process plants.'
            ),
            'order': 24
        },
        {
            'title': 'Strength of Materials',
            'description': 'Analyze stress, strain, bending, and torsion in components',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Strength of materials evaluates how components deform and fail under load.\n\n'
                'Lesson includes:\n'
                '1. Stress-strain relationships\n'
                '2. Young modulus and elastic behavior\n'
                '3. Bending stress in beams\n'
                '4. Torsion in shafts and factor of safety\n\n'
                'This is critical for safe structural and machine design.'
            ),
            'order': 25
        },
        {
            'title': 'Manufacturing Processes and CNC',
            'description': 'Learn casting, machining, welding, and CNC basics',
            'subject': 'Engineering',
            'grade_level': 'Professional',
            'content': (
                'Manufacturing converts design into physical products with quality and precision.\n\n'
                'Covered processes:\n'
                '1. Casting and forming\n'
                '2. Machining operations\n'
                '3. Welding and joining methods\n'
                '4. CNC workflow and toolpath basics\n\n'
                'Process selection depends on material, tolerance, cost, and production volume.'
            ),
            'order': 26
        },
        {
            'title': 'Control Systems Fundamentals',
            'description': 'Model and analyze open-loop and closed-loop systems',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Control systems maintain desired output despite disturbances.\n\n'
                'This lesson covers:\n'
                '1. Transfer functions and block diagrams\n'
                '2. Feedback and stability concepts\n'
                '3. Time response characteristics\n'
                '4. Basic PID control intuition\n\n'
                'Control engineering is used in robotics, automation, vehicles, and process industries.'
            ),
            'order': 27
        },
        {
            'title': 'Digital Logic and Microprocessors',
            'description': 'Study logic gates, combinational circuits, and processor basics',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Digital systems are built from binary logic and sequential operations.\n\n'
                'Core modules:\n'
                '1. Number systems and Boolean algebra\n'
                '2. Logic gates and truth tables\n'
                '3. Flip-flops, counters, and registers\n'
                '4. Microprocessor architecture and instruction cycle\n\n'
                'These concepts form the foundation of embedded and computer hardware design.'
            ),
            'order': 28
        },
        {
            'title': 'Signals and Systems for Engineers',
            'description': 'Understand signal types, system response, and transforms',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Signals and systems provide tools for analyzing dynamic behavior.\n\n'
                'You will learn:\n'
                '1. Continuous and discrete signals\n'
                '2. LTI systems and convolution\n'
                '3. Frequency domain intuition\n'
                '4. Laplace/Fourier transform basics\n\n'
                'Used in communications, controls, audio processing, and instrumentation.'
            ),
            'order': 29
        },
        {
            'title': 'Embedded Systems and IoT',
            'description': 'Build sensor-based systems with microcontrollers and connectivity',
            'subject': 'Engineering',
            'grade_level': 'Professional',
            'content': (
                'Embedded systems combine hardware and software for dedicated functions.\n\n'
                'Key parts:\n'
                '1. Microcontroller peripherals (GPIO, ADC, UART)\n'
                '2. Sensor interfacing and data acquisition\n'
                '3. Communication protocols (I2C, SPI, MQTT)\n'
                '4. IoT architecture and cloud dashboard basics\n\n'
                'Embedded IoT solutions are central to smart homes, industry 4.0, and healthcare devices.'
            ),
            'order': 30
        },
        {
            'title': 'Computer Engineering: Data Structures and Algorithms',
            'description': 'Use efficient data structures and algorithmic strategies',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Efficient software depends on choosing the right data structure and algorithm.\n\n'
                'Topics included:\n'
                '1. Arrays, linked lists, stacks, queues, trees, graphs\n'
                '2. Sorting and searching techniques\n'
                '3. Time and space complexity (Big-O)\n'
                '4. Recursion, greedy, and dynamic programming basics\n\n'
                'These fundamentals support software engineering, AI, and systems programming.'
            ),
            'order': 31
        },
        {
            'title': 'Civil Engineering: Surveying and Estimation',
            'description': 'Learn field surveying methods and quantity estimation basics',
            'subject': 'Engineering',
            'grade_level': 'Professional',
            'content': (
                'Surveying maps terrain and site geometry for planning and construction.\n\n'
                'Lesson structure:\n'
                '1. Chain, compass, and leveling methods\n'
                '2. Bearings, reduced levels, and contouring\n'
                '3. Basic quantity take-off and BOQ concepts\n'
                '4. Intro to cost estimation and rate analysis\n\n'
                'These skills are used in road works, buildings, and infrastructure projects.'
            ),
            'order': 32
        },
        {
            'title': 'Renewable Energy Systems',
            'description': 'Understand solar, wind, storage, and hybrid system design principles',
            'subject': 'Engineering',
            'grade_level': 'Undergraduate',
            'content': (
                'Renewable systems are essential for sustainable energy transition.\n\n'
                'In this topic:\n'
                '1. Solar PV components and sizing basics\n'
                '2. Wind energy conversion overview\n'
                '3. Batteries and energy storage fundamentals\n'
                '4. Hybrid systems and grid integration concepts\n\n'
                'Engineers use these principles in clean power planning and smart-grid deployment.'
            ),
            'order': 33
        },
        {
            'title': 'Electromagnetism and Waves',
            'description': 'Understand electric fields, magnetic fields, and wave behavior',
            'subject': 'Physics',
            'grade_level': 'Grade 11',
            'content': (
                'Electromagnetism links electricity and magnetism through field interactions.\n\n'
                'Key ideas:\n'
                '1. Electric field and potential\n'
                '2. Magnetic field around moving charges\n'
                '3. Electromagnetic induction\n'
                '4. Nature of electromagnetic waves\n\n'
                'Applications include motors, generators, communication systems, and sensors.'
            ),
            'order': 34
        },
        {
            'title': 'Modern Physics and Semiconductors',
            'description': 'Explore atoms, quantum ideas, and semiconductor basics',
            'subject': 'Physics',
            'grade_level': 'Undergraduate',
            'content': (
                'Modern physics explains microscopic phenomena beyond classical mechanics.\n\n'
                'This lesson includes:\n'
                '1. Atomic models and quantization\n'
                '2. Photoelectric effect and wave-particle duality\n'
                '3. Basic quantum concepts\n'
                '4. Semiconductor materials and p-n junction behavior\n\n'
                'These concepts drive electronics, lasers, and modern computing devices.'
            ),
            'order': 35
        },
        {
            'title': 'Heat Transfer and Thermal Physics',
            'description': 'Learn conduction, convection, and radiation in real systems',
            'subject': 'Physics',
            'grade_level': 'Undergraduate',
            'content': (
                'Thermal physics studies heat movement and temperature behavior.\n\n'
                'Concepts covered:\n'
                '1. Temperature scales and thermal equilibrium\n'
                '2. Conduction through solids\n'
                '3. Convection in fluids\n'
                '4. Radiation and emissivity\n\n'
                'Heat transfer principles are used in cooling systems, HVAC, and energy devices.'
            ),
            'order': 36
        },
        {
            'title': 'Analytical Chemistry and Instrumentation',
            'description': 'Study concentration measurement and common laboratory instruments',
            'subject': 'Chemistry',
            'grade_level': 'Undergraduate',
            'content': (
                'Analytical chemistry quantifies substances in complex samples.\n\n'
                'Main areas:\n'
                '1. Titration and volumetric analysis\n'
                '2. pH, buffers, and indicators\n'
                '3. Spectroscopy basics (UV-Vis)\n'
                '4. Chromatography overview\n\n'
                'Accurate analysis is essential in pharma, food quality, environment, and industry.'
            ),
            'order': 37
        },
        {
            'title': 'Electrochemistry and Corrosion',
            'description': 'Understand redox reactions, cells, and corrosion prevention',
            'subject': 'Chemistry',
            'grade_level': 'Undergraduate',
            'content': (
                'Electrochemistry connects chemical reactions with electrical energy transfer.\n\n'
                'Lesson highlights:\n'
                '1. Oxidation and reduction balancing\n'
                '2. Galvanic and electrolytic cells\n'
                '3. Electrode potentials and Nernst intuition\n'
                '4. Corrosion mechanisms and protection methods\n\n'
                'Used in batteries, electroplating, corrosion engineering, and energy storage.'
            ),
            'order': 38
        },
        {
            'title': 'Environmental Chemistry and Sustainability',
            'description': 'Learn pollution chemistry and sustainable process thinking',
            'subject': 'Chemistry',
            'grade_level': 'Professional',
            'content': (
                'Environmental chemistry studies chemical processes in air, water, and soil.\n\n'
                'Topics:\n'
                '1. Water quality and treatment chemistry\n'
                '2. Air pollutants and atmospheric reactions\n'
                '3. Waste management and green chemistry ideas\n'
                '4. Sustainability metrics in chemical processes\n\n'
                'This supports cleaner technologies and responsible industrial practice.'
            ),
            'order': 39
        },
        {
            'title': 'Academic Writing and Research Skills',
            'description': 'Write reports, essays, and references clearly and correctly',
            'subject': 'English',
            'grade_level': 'Undergraduate',
            'content': (
                'Academic writing requires clarity, structure, and evidence-based argumentation.\n\n'
                'This lesson covers:\n'
                '1. Essay and report structure\n'
                '2. Thesis statements and paragraph coherence\n'
                '3. Citation and referencing basics\n'
                '4. Editing for concision and formal tone\n\n'
                'Strong writing improves performance in projects, exams, and publications.'
            ),
            'order': 40
        },
        {
            'title': 'Spoken English and Presentation Skills',
            'description': 'Improve fluency, pronunciation, and public speaking confidence',
            'subject': 'English',
            'grade_level': 'Professional',
            'content': (
                'Spoken English and presentation skills are critical for interviews and workplace impact.\n\n'
                'Skill modules:\n'
                '1. Pronunciation and stress patterns\n'
                '2. Structuring a short presentation\n'
                '3. Voice control and body language\n'
                '4. Handling questions effectively\n\n'
                'Regular practice improves confidence and communication effectiveness.'
            ),
            'order': 41
        },
        {
            'title': 'Genetics and Heredity',
            'description': 'Understand genes, inheritance patterns, and DNA basics',
            'subject': 'Biology',
            'grade_level': 'Grade 11',
            'content': (
                'Genetics explains how traits are inherited across generations.\n\n'
                'You will study:\n'
                '1. DNA, genes, and chromosomes\n'
                '2. Mendelian inheritance patterns\n'
                '3. Dominant and recessive traits\n'
                '4. Basic genetic variation concepts\n\n'
                'Genetics is essential for medicine, agriculture, and biotechnology.'
            ),
            'order': 42
        },
        {
            'title': 'Human Physiology and Homeostasis',
            'description': 'Learn organ-system coordination and internal balance',
            'subject': 'Biology',
            'grade_level': 'Undergraduate',
            'content': (
                'Physiology studies how body systems function and interact.\n\n'
                'Main topics:\n'
                '1. Nervous and endocrine coordination\n'
                '2. Cardiovascular and respiratory essentials\n'
                '3. Digestive and excretory functions\n'
                '4. Homeostasis and feedback control\n\n'
                'Understanding physiology supports health science and biomedical learning.'
            ),
            'order': 43
        }
    ]

    lessons = {item['title']: get_or_create_lesson(item) for item in lessons_data}

    practice_problems = [
        {
            'lesson_id': lessons['Introduction to Algebra'].id,
            'question': 'What is the value of x in the equation: 2x + 5 = 13?',
            'question_type': 'numeric',
            'correct_answer': '4',
            'explanation': '2x + 5 = 13; 2x = 8; x = 4',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Introduction to Algebra'].id,
            'question': 'Solve 4x - 9 = 7. What is x?',
            'question_type': 'numeric',
            'correct_answer': '4',
            'explanation': '4x - 9 = 7; 4x = 16; x = 4',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 1: Vectors and Scalars'].id,
            'question': 'Is (3, 4) a vector or a scalar?',
            'question_type': 'short_answer',
            'correct_answer': 'vector',
            'explanation': '(3, 4) has magnitude and direction, so it is a vector.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 1: Vectors and Scalars'].id,
            'question': 'Find the magnitude of vector (6, 8).',
            'question_type': 'short_answer',
            'correct_answer': '10',
            'explanation': 'sqrt(6^2 + 8^2) = sqrt(100) = 10',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 2: Vector Operations'].id,
            'question': 'Add vectors (2, -1) and (5, 3).',
            'question_type': 'short_answer',
            'correct_answer': '(7,2)',
            'explanation': 'Add each component: (2+5, -1+3) = (7,2)',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 3: Matrices Basics'].id,
            'question': 'How many rows and columns are in a 2x3 matrix?',
            'question_type': 'short_answer',
            'correct_answer': '2 rows and 3 columns',
            'explanation': 'The first number is rows and the second is columns.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 3: Matrices Basics'].id,
            'question': 'Can a 2x2 matrix be added to a 2x3 matrix?',
            'question_type': 'true_false',
            'correct_answer': 'False',
            'explanation': 'Matrix addition requires same dimensions.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Linear Algebra Session 5: Systems of Linear Equations'].id,
            'question': 'Solve quickly: x + y = 10 and x - y = 2. What is y?',
            'question_type': 'short_answer',
            'correct_answer': '4',
            'explanation': 'Add equations: 2x = 12 so x = 6, then y = 4.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Introduction to Calculus'].id,
            'question': 'What is the derivative of x^3?',
            'question_type': 'short_answer',
            'correct_answer': '3x^2',
            'explanation': 'Power rule: d/dx x^n = n*x^(n-1)',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Newton Laws of Motion'].id,
            'question': 'If mass is 2 kg and acceleration is 3 m/s^2, what is the net force?',
            'question_type': 'short_answer',
            'correct_answer': '6 N',
            'explanation': 'F = ma = 2 * 3 = 6 N',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Photosynthesis'].id,
            'question': 'What is the primary role of chlorophyll in photosynthesis?',
            'question_type': 'multiple_choice',
            'options': [
                'Absorbs light energy',
                'Produces ATP',
                'Breaks down glucose',
                'Transports water'
            ],
            'correct_answer': 'Absorbs light energy',
            'explanation': 'Chlorophyll absorbs light energy to drive photosynthesis.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Photosynthesis'].id,
            'question': 'Which gas is taken in by plants during photosynthesis?',
            'question_type': 'short_answer',
            'correct_answer': 'Carbon dioxide',
            'explanation': 'Plants absorb carbon dioxide and release oxygen.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Photosynthesis'].id,
            'question': 'Name the pigment that captures light energy during photosynthesis.',
            'question_type': 'short_answer',
            'correct_answer': 'Chlorophyll',
            'explanation': 'Chlorophyll captures light energy in chloroplasts.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Photosynthesis'].id,
            'question': 'Which stage directly fixes carbon dioxide into sugars?',
            'question_type': 'multiple_choice',
            'options': ['Calvin cycle', 'Light-independent photolysis', 'Electron transport chain only', 'Transpiration'],
            'correct_answer': 'Calvin cycle',
            'explanation': 'Carbon fixation occurs in the Calvin cycle.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Atomic Structure and Periodic Trends'].id,
            'question': 'Which particle determines the atomic number of an element?',
            'question_type': 'short_answer',
            'correct_answer': 'Protons',
            'explanation': 'Atomic number equals the number of protons in the nucleus.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Atomic Structure and Periodic Trends'].id,
            'question': 'As you move left to right in a period, does atomic radius generally increase?',
            'question_type': 'true_false',
            'correct_answer': 'False',
            'explanation': 'Atomic radius generally decreases across a period.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Chemical Bonding and Compounds'].id,
            'question': 'Sodium chloride (NaCl) is primarily which type of bond?',
            'question_type': 'multiple_choice',
            'options': ['Ionic', 'Covalent', 'Metallic', 'Hydrogen'],
            'correct_answer': 'Ionic',
            'explanation': 'Na transfers an electron to Cl, forming ions.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Chemical Bonding and Compounds'].id,
            'question': 'In covalent bonding, atoms share electrons.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Sharing electrons is the basis of covalent bonds.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Grammar and Sentence Structure'].id,
            'question': 'Choose the correct sentence: "The list of items are on the desk" or "The list of items is on the desk".',
            'question_type': 'short_answer',
            'correct_answer': 'The list of items is on the desk',
            'explanation': 'The subject is "list" (singular), so the verb is "is".',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Grammar and Sentence Structure'].id,
            'question': 'A sentence with one independent clause and one dependent clause is called?',
            'question_type': 'multiple_choice',
            'options': ['Simple sentence', 'Compound sentence', 'Complex sentence', 'Fragment'],
            'correct_answer': 'Complex sentence',
            'explanation': 'A complex sentence contains one independent and one or more dependent clauses.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['English Communication for Workplace'].id,
            'question': 'Which email closing is most professional?',
            'question_type': 'multiple_choice',
            'options': ['Bye', 'Thanks and regards', 'See ya', 'Later'],
            'correct_answer': 'Thanks and regards',
            'explanation': 'Professional sign-offs maintain formal tone.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Organic Chemistry Fundamentals'].id,
            'question': 'Which functional group is present in ethanol?',
            'question_type': 'short_answer',
            'correct_answer': 'Alcohol',
            'explanation': 'Ethanol contains the hydroxyl (-OH) group, classifying it as an alcohol.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Chemical Kinetics and Equilibrium'].id,
            'question': 'A catalyst increases reaction rate by lowering activation energy.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Catalysts provide an alternative pathway with lower activation energy.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Engineering Mechanics: Statics'].id,
            'question': 'For a 2D body in equilibrium, the sum of moments about any point should be?',
            'question_type': 'short_answer',
            'correct_answer': 'Zero',
            'explanation': 'Equilibrium requires both force and moment sums to be zero.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Electrical Engineering: Circuit Analysis'].id,
            'question': 'If V = 12V and R = 4 ohms, what is current I?',
            'question_type': 'short_answer',
            'correct_answer': '3 A',
            'explanation': 'Ohm law: I = V/R = 12/4 = 3 A.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Engineering Drawing and CAD Basics'].id,
            'question': 'Orthographic projection usually shows how many principal views?',
            'question_type': 'multiple_choice',
            'options': ['1', '2', '3', '6'],
            'correct_answer': '3',
            'explanation': 'Front, top, and side views are the standard principal views.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Thermodynamics for Engineers'].id,
            'question': 'What does the first law of thermodynamics represent?',
            'question_type': 'short_answer',
            'correct_answer': 'Conservation of energy',
            'explanation': 'Energy cannot be created or destroyed, only transformed.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Fluid Mechanics Essentials'].id,
            'question': 'Bernoulli principle primarily relates pressure, velocity, and elevation in flowing fluid.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Bernoulli equation links pressure head, velocity head, and elevation head.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Strength of Materials'].id,
            'question': 'Stress is force divided by?',
            'question_type': 'short_answer',
            'correct_answer': 'Area',
            'explanation': 'Normal stress = force / cross-sectional area.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Manufacturing Processes and CNC'].id,
            'question': 'CNC stands for?',
            'question_type': 'short_answer',
            'correct_answer': 'Computer Numerical Control',
            'explanation': 'CNC machines execute programmed tool motions automatically.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Control Systems Fundamentals'].id,
            'question': 'Feedback in control systems helps reduce error between desired and actual output.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Feedback compares output with setpoint to correct deviations.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Digital Logic and Microprocessors'].id,
            'question': 'How many possible output combinations exist for 3 binary inputs?',
            'question_type': 'short_answer',
            'correct_answer': '8',
            'explanation': '2^3 = 8 combinations.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Signals and Systems for Engineers'].id,
            'question': 'Convolution is used to compute output of an LTI system.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Output equals input convolved with impulse response for LTI systems.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Embedded Systems and IoT'].id,
            'question': 'Name one common protocol used for IoT messaging.',
            'question_type': 'short_answer',
            'correct_answer': 'MQTT',
            'explanation': 'MQTT is a lightweight publish-subscribe protocol for IoT.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Computer Engineering: Data Structures and Algorithms'].id,
            'question': 'Which data structure uses FIFO order?',
            'question_type': 'multiple_choice',
            'options': ['Stack', 'Queue', 'Tree', 'Heap'],
            'correct_answer': 'Queue',
            'explanation': 'Queue follows First-In-First-Out order.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Civil Engineering: Surveying and Estimation'].id,
            'question': 'A BOQ in civil projects expands to?',
            'question_type': 'short_answer',
            'correct_answer': 'Bill of Quantities',
            'explanation': 'BOQ lists measured quantities for project estimation.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Renewable Energy Systems'].id,
            'question': 'Solar PV panels convert sunlight directly into?',
            'question_type': 'short_answer',
            'correct_answer': 'Electrical energy',
            'explanation': 'Photovoltaic effect produces electrical energy from light.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Electromagnetism and Waves'].id,
            'question': 'A changing magnetic field can induce an electric current.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'This is electromagnetic induction.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Modern Physics and Semiconductors'].id,
            'question': 'What type of semiconductor is formed by adding pentavalent impurities?',
            'question_type': 'short_answer',
            'correct_answer': 'n-type',
            'explanation': 'Pentavalent doping adds extra electrons and forms n-type material.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Heat Transfer and Thermal Physics'].id,
            'question': 'Which mode of heat transfer does not require a material medium?',
            'question_type': 'multiple_choice',
            'options': ['Conduction', 'Convection', 'Radiation', 'Diffusion'],
            'correct_answer': 'Radiation',
            'explanation': 'Radiation transfers heat through electromagnetic waves.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Analytical Chemistry and Instrumentation'].id,
            'question': 'Titration is commonly used to determine?',
            'question_type': 'short_answer',
            'correct_answer': 'Concentration',
            'explanation': 'Titration quantifies concentration of analyte solutions.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Electrochemistry and Corrosion'].id,
            'question': 'Corrosion of iron is an oxidation process.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Iron loses electrons during rust formation.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Environmental Chemistry and Sustainability'].id,
            'question': 'Which approach reduces hazardous substance generation at source?',
            'question_type': 'short_answer',
            'correct_answer': 'Green chemistry',
            'explanation': 'Green chemistry emphasizes safer reagents and low-waste pathways.',
            'difficulty': 'medium'
        },
        {
            'lesson_id': lessons['Academic Writing and Research Skills'].id,
            'question': 'A clear thesis statement usually appears in which part of an essay?',
            'question_type': 'multiple_choice',
            'options': ['Introduction', 'References', 'Appendix', 'Title page'],
            'correct_answer': 'Introduction',
            'explanation': 'Thesis statement sets the central argument early.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Spoken English and Presentation Skills'].id,
            'question': 'Maintaining eye contact improves audience engagement.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Eye contact helps build connection and confidence.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Genetics and Heredity'].id,
            'question': 'What molecule stores hereditary information?',
            'question_type': 'short_answer',
            'correct_answer': 'DNA',
            'explanation': 'DNA carries genetic instructions in living organisms.',
            'difficulty': 'easy'
        },
        {
            'lesson_id': lessons['Human Physiology and Homeostasis'].id,
            'question': 'Homeostasis means maintaining a stable internal environment.',
            'question_type': 'true_false',
            'correct_answer': 'True',
            'explanation': 'Body systems regulate variables to keep internal balance.',
            'difficulty': 'easy'
        }
    ]

    for problem in practice_problems:
        get_or_create_practice_problem(problem)

    quizzes_data = [
        {
            'lesson_title': 'Introduction to Algebra',
            'payload': {
                'title': 'Algebra Basics Quiz',
                'description': 'Test your understanding of basic algebraic concepts',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Solve for x: 3x - 7 = 5',
                    'question_type': 'short_answer',
                    'correct_answer': '4',
                    'explanation': '3x = 12, so x = 4',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'What is the commutative property of addition?',
                    'question_type': 'multiple_choice',
                    'options': ['a + b = b + a', 'a + (b + c) = (a + b) + c', 'a(b + c) = ab + ac', 'None of the above'],
                    'correct_answer': 'a + b = b + a',
                    'explanation': 'Order does not matter in addition.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Is 5 + 3 = 3 + 5 true?',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'This is commutative addition.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 1: Vectors and Scalars',
            'payload': {
                'title': 'Linear Algebra Session 1 Quiz',
                'description': 'Check your understanding of vectors and scalars',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Which of the following is a scalar?',
                    'question_type': 'multiple_choice',
                    'options': ['Velocity', 'Displacement', 'Temperature', 'Force'],
                    'correct_answer': 'Temperature',
                    'explanation': 'Temperature has magnitude only and no direction.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Find the magnitude of vector (3, 4).',
                    'question_type': 'short_answer',
                    'correct_answer': '5',
                    'explanation': 'sqrt(3^2 + 4^2) = 5.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'A vector has both magnitude and direction.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'This is the definition of a vector.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 2: Vector Operations',
            'payload': {
                'title': 'Linear Algebra Session 2 Quiz',
                'description': 'Practice vector operations',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Add vectors (1,2) and (3,4).',
                    'question_type': 'short_answer',
                    'correct_answer': '(4,6)',
                    'explanation': 'Add corresponding components.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'If v=(2,-1), what is 3v?',
                    'question_type': 'short_answer',
                    'correct_answer': '(6,-3)',
                    'explanation': 'Multiply each component by 3.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Vector subtraction can be done by adding the opposite vector.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'u - v = u + (-v).',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 3: Matrices Basics',
            'payload': {
                'title': 'Linear Algebra Session 3 Quiz',
                'description': 'Matrix dimensions and basic operations',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'What is the dimension of a matrix with 2 rows and 3 columns?',
                    'question_type': 'short_answer',
                    'correct_answer': '2x3',
                    'explanation': 'Dimension is rows x columns.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Can matrices of size 2x2 and 2x3 be added?',
                    'question_type': 'true_false',
                    'correct_answer': 'False',
                    'explanation': 'Matrix addition requires equal dimensions.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which is required for matrix multiplication A(mxn) * B(p x q)?',
                    'question_type': 'multiple_choice',
                    'options': ['m = p', 'n = p', 'm = q', 'n = q'],
                    'correct_answer': 'n = p',
                    'explanation': 'Inner dimensions must match.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 5: Systems of Linear Equations',
            'payload': {
                'title': 'Linear Systems Quiz',
                'description': 'Test methods for solving linear systems',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'How many solutions can a linear system have?',
                    'question_type': 'multiple_choice',
                    'options': ['Only one', 'One or two only', 'One, none, or infinitely many', 'Always infinitely many'],
                    'correct_answer': 'One, none, or infinitely many',
                    'explanation': 'Depends on line/plane intersections.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Elimination method combines equations to remove a variable.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'That is the core idea of elimination.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Solve: x + y = 5 and x - y = 1. What is x?',
                    'question_type': 'short_answer',
                    'correct_answer': '3',
                    'explanation': 'Adding equations gives 2x = 6, so x = 3.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 6: Eigenvalues and Eigenvectors',
            'payload': {
                'title': 'Eigenvalues and Eigenvectors Quiz',
                'description': 'Understand eigen concepts and matrix action',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'An eigenvector changes only in magnitude under a linear transformation.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Direction remains the same (up to sign), while scale changes by eigenvalue.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'If Av = 3v, what is the eigenvalue?',
                    'question_type': 'short_answer',
                    'correct_answer': '3',
                    'explanation': 'The scalar multiplying v is the eigenvalue.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'How many distinct eigenvalues can a 2x2 matrix have at most?',
                    'question_type': 'short_answer',
                    'correct_answer': '2',
                    'explanation': 'A 2x2 characteristic polynomial has degree 2.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Linear Algebra Session 7: Orthogonality and Projections',
            'payload': {
                'title': 'Orthogonality and Projections Quiz',
                'description': 'Dot products, right angles, and vector projection',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'What is the dot product of orthogonal vectors?',
                    'question_type': 'short_answer',
                    'correct_answer': '0',
                    'explanation': 'Orthogonal vectors are perpendicular, giving dot product zero.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Projection finds the component of one vector along another.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Projection extracts aligned component.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'If u . v = 0, then u and v are?',
                    'question_type': 'multiple_choice',
                    'options': ['Parallel', 'Orthogonal', 'Equal', 'Dependent'],
                    'correct_answer': 'Orthogonal',
                    'explanation': 'Zero dot product indicates orthogonality.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Photosynthesis',
            'payload': {
                'title': 'Photosynthesis Quiz',
                'description': 'Test your knowledge of the photosynthetic process',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'In which part of the chloroplast do light-dependent reactions occur?',
                    'question_type': 'multiple_choice',
                    'options': ['Thylakoid membrane', 'Stroma', 'Nucleus', 'Ribosome'],
                    'correct_answer': 'Thylakoid membrane',
                    'explanation': 'Light-dependent reactions occur in thylakoids.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'What gas is released during photosynthesis?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Oxygen',
                    'explanation': 'Oxygen is released when water is split.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Is carbon dioxide required for photosynthesis?',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'CO2 is one of the main reactants.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Cellular Respiration',
            'payload': {
                'title': 'Cellular Respiration Quiz',
                'description': 'Check your understanding of ATP production',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'What is the main energy currency of the cell?',
                    'question_type': 'short_answer',
                    'correct_answer': 'ATP',
                    'explanation': 'ATP stores and transfers energy in cells.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Cellular respiration primarily occurs in the mitochondria.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Mitochondria are the main site of respiration in eukaryotic cells.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which process comes first in cellular respiration?',
                    'question_type': 'multiple_choice',
                    'options': ['Electron transport chain', 'Krebs cycle', 'Glycolysis', 'Fermentation'],
                    'correct_answer': 'Glycolysis',
                    'explanation': 'Glycolysis is the first stage and occurs in the cytoplasm.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Introduction to Calculus',
            'payload': {
                'title': 'Introduction to Calculus Quiz',
                'description': 'Check limits and derivative basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'What does the derivative represent?',
                    'question_type': 'multiple_choice',
                    'options': ['Area under curve', 'Average value', 'Instantaneous rate of change', 'Maximum value'],
                    'correct_answer': 'Instantaneous rate of change',
                    'explanation': 'Derivative gives instant slope/rate.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'The limit process is foundational for derivatives.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Derivative is defined by a limit.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'What is d/dx of x^2?',
                    'question_type': 'short_answer',
                    'correct_answer': '2x',
                    'explanation': 'Power rule: d/dx x^n = n*x^(n-1).',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Newton Laws of Motion',
            'payload': {
                'title': 'Newton Laws Quiz',
                'description': 'Practice force and motion concepts',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Newton second law is commonly written as?',
                    'question_type': 'short_answer',
                    'correct_answer': 'F=ma',
                    'explanation': 'Net force equals mass times acceleration.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Every action has an equal and opposite reaction belongs to which law?',
                    'question_type': 'multiple_choice',
                    'options': ['First law', 'Second law', 'Third law', 'Law of gravitation'],
                    'correct_answer': 'Third law',
                    'explanation': 'This is Newton third law.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'An object at rest remains at rest unless acted on by a net force.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'This is Newton first law (inertia).',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Engineering Mechanics: Statics',
            'payload': {
                'title': 'Engineering Mechanics Quiz',
                'description': 'Forces, moments, and equilibrium basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'For equilibrium in 2D, which condition is required?',
                    'question_type': 'multiple_choice',
                    'options': ['Only sum of Fx = 0', 'Only sum of moments = 0', 'Sum of forces and moments = 0', 'No force acts'],
                    'correct_answer': 'Sum of forces and moments = 0',
                    'explanation': 'Equilibrium needs force balance in x,y and moment balance.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'A free-body diagram should include all external forces.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'FBD accuracy is essential for solving statics problems.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Moment is force multiplied by?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Perpendicular distance',
                    'explanation': 'M = F x d_perpendicular.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Electrical Engineering: Circuit Analysis',
            'payload': {
                'title': 'Circuit Analysis Quiz',
                'description': 'Ohm law and Kirchhoff law practice',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Kirchhoff current law applies at?',
                    'question_type': 'multiple_choice',
                    'options': ['Loops', 'Nodes', 'Only sources', 'Transformers only'],
                    'correct_answer': 'Nodes',
                    'explanation': 'KCL states algebraic sum of currents at a node is zero.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'If R doubles at constant V, current halves.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'I = V/R, so increasing R reduces I.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Power in a resistor can be computed as?',
                    'question_type': 'multiple_choice',
                    'options': ['P = VI', 'P = V/I', 'P = I/V', 'P = R/I'],
                    'correct_answer': 'P = VI',
                    'explanation': 'Electrical power is voltage multiplied by current.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Engineering Drawing and CAD Basics',
            'payload': {
                'title': 'Engineering Drawing and CAD Quiz',
                'description': 'Projection, dimensions, and CAD fundamentals',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Which view is commonly paired with front view in orthographic projection?',
                    'question_type': 'multiple_choice',
                    'options': ['Random view', 'Top view', 'Perspective only', 'No additional view'],
                    'correct_answer': 'Top view',
                    'explanation': 'Front-top-side are principal orthographic views.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Dimensioning communicates size and location in drawings.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Dimensions define geometric requirements.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'CAD is mainly used to?',
                    'question_type': 'multiple_choice',
                    'options': ['Draw and modify designs digitally', 'Only print drawings', 'Do accounting', 'Browse files'],
                    'correct_answer': 'Draw and modify designs digitally',
                    'explanation': 'CAD supports drafting, modeling, and revisions.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Thermodynamics for Engineers',
            'payload': {
                'title': 'Thermodynamics Quiz',
                'description': 'Energy conservation and entropy basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'The first law of thermodynamics is about?',
                    'question_type': 'multiple_choice',
                    'options': ['Entropy increase only', 'Conservation of energy', 'Gas law only', 'Momentum transfer'],
                    'correct_answer': 'Conservation of energy',
                    'explanation': 'Energy is conserved in thermodynamic processes.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Entropy is associated with disorder and irreversibility.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Second law introduces entropy trends.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one practical application of thermodynamics.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Power plant',
                    'explanation': 'Thermodynamics is central to power generation, HVAC, and engines.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Fluid Mechanics Essentials',
            'payload': {
                'title': 'Fluid Mechanics Quiz',
                'description': 'Flow equations and pressure behavior',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Bernoulli equation assumes ideal flow and energy conservation along streamline.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Bernoulli is derived from mechanical energy conservation.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Continuity equation is based on conservation of?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Mass',
                    'explanation': 'Mass flow rate is conserved in steady incompressible flow.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which factor generally increases pipe head loss?',
                    'question_type': 'multiple_choice',
                    'options': ['Lower velocity', 'Shorter pipe', 'Higher roughness', 'Bigger diameter'],
                    'correct_answer': 'Higher roughness',
                    'explanation': 'Rougher pipe walls increase friction losses.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Strength of Materials',
            'payload': {
                'title': 'Strength of Materials Quiz',
                'description': 'Stress, strain, and beam response fundamentals',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Stress is measured in units of?',
                    'question_type': 'multiple_choice',
                    'options': ['N', 'Pa', 'J', 'm/s'],
                    'correct_answer': 'Pa',
                    'explanation': 'Pascal is N/m^2, the SI unit of stress.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Young modulus is ratio of stress to strain in elastic region.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'E = stress/strain within elastic limit.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one loading mode besides tension/compression.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Bending',
                    'explanation': 'Common modes include bending, shear, and torsion.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Manufacturing Processes and CNC',
            'payload': {
                'title': 'Manufacturing and CNC Quiz',
                'description': 'Production methods and CNC fundamentals',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'CNC machines are controlled by?',
                    'question_type': 'multiple_choice',
                    'options': ['Manual lever only', 'Programmed numerical commands', 'Hydraulic only', 'Random motion'],
                    'correct_answer': 'Programmed numerical commands',
                    'explanation': 'CNC executes programmed coordinates and feeds.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Welding is a permanent joining process.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Welding creates metallurgical bond between parts.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one subtractive manufacturing process.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Milling',
                    'explanation': 'Machining operations like milling remove material.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Control Systems Fundamentals',
            'payload': {
                'title': 'Control Systems Quiz',
                'description': 'Feedback, stability, and time response',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Closed-loop systems use feedback to regulate output.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Feedback compares output to reference signal.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'PID stands for?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Proportional Integral Derivative',
                    'explanation': 'PID controller has three correction terms.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which is a common stability indicator in frequency domain?',
                    'question_type': 'multiple_choice',
                    'options': ['Profit margin', 'Phase margin', 'Voltage rating', 'Data rate'],
                    'correct_answer': 'Phase margin',
                    'explanation': 'Gain and phase margins indicate robustness.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Digital Logic and Microprocessors',
            'payload': {
                'title': 'Digital Logic and Microprocessors Quiz',
                'description': 'Boolean logic and processor basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'How many input combinations does a 2-input logic gate have?',
                    'question_type': 'short_answer',
                    'correct_answer': '4',
                    'explanation': '2^2 combinations for two binary inputs.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'A flip-flop is used as a memory element.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Flip-flops store binary state in sequential circuits.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which operation does ALU primarily perform?',
                    'question_type': 'multiple_choice',
                    'options': ['Mechanical rotation', 'Arithmetic and logic operations', 'Wireless charging', 'Data printing'],
                    'correct_answer': 'Arithmetic and logic operations',
                    'explanation': 'ALU executes core math and logic instructions.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Signals and Systems for Engineers',
            'payload': {
                'title': 'Signals and Systems Quiz',
                'description': 'Signal representation and system behavior',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'An LTI system is linear and time-invariant.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'LTI assumptions simplify analysis and design.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Convolution in time domain corresponds to what in frequency domain?',
                    'question_type': 'multiple_choice',
                    'options': ['Addition', 'Multiplication', 'Division', 'Differentiation only'],
                    'correct_answer': 'Multiplication',
                    'explanation': 'Convolution-multiplication duality is fundamental.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one transform commonly used in signals and systems.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Fourier transform',
                    'explanation': 'Fourier and Laplace transforms are widely used.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Embedded Systems and IoT',
            'payload': {
                'title': 'Embedded Systems and IoT Quiz',
                'description': 'Microcontrollers, sensors, and connectivity',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Which interface is commonly used for short-range sensor communication?',
                    'question_type': 'multiple_choice',
                    'options': ['I2C', 'HDMI', 'VGA', 'PCIe'],
                    'correct_answer': 'I2C',
                    'explanation': 'I2C is common for connecting sensors/peripherals.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'MQTT follows publish-subscribe model.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'MQTT brokers route published messages to subscribers.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'What does ADC stand for in microcontrollers?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Analog to Digital Converter',
                    'explanation': 'ADC converts analog sensor signals into digital values.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Computer Engineering: Data Structures and Algorithms',
            'payload': {
                'title': 'DSA for Engineers Quiz',
                'description': 'Efficiency and algorithm basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Big-O notation describes?',
                    'question_type': 'multiple_choice',
                    'options': ['Hardware size', 'Algorithmic complexity growth', 'Only memory address', 'Programming language'],
                    'correct_answer': 'Algorithmic complexity growth',
                    'explanation': 'Big-O captures scaling behavior with input size.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Binary search requires sorted data.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Binary search relies on sorted order to halve search space.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Which structure follows LIFO?',
                    'question_type': 'short_answer',
                    'correct_answer': 'Stack',
                    'explanation': 'Stack uses last-in-first-out discipline.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Civil Engineering: Surveying and Estimation',
            'payload': {
                'title': 'Surveying and Estimation Quiz',
                'description': 'Survey methods and project quantity basics',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 12
            },
            'questions': [
                {
                    'question_text': 'Which instrument is commonly used for leveling work?',
                    'question_type': 'multiple_choice',
                    'options': ['Theodolite/level', 'Oscilloscope', 'Micrometer only', 'Multimeter'],
                    'correct_answer': 'Theodolite/level',
                    'explanation': 'Levels/theodolites are key field instruments for surveying.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'BOQ helps estimate project cost by listing quantities.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'BOQ forms basis for rate and cost calculations.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one surveying output used in planning.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Contour map',
                    'explanation': 'Contour maps represent terrain elevation and slope.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        },
        {
            'lesson_title': 'Renewable Energy Systems',
            'payload': {
                'title': 'Renewable Energy Systems Quiz',
                'description': 'Solar, wind, storage, and integration concepts',
                'total_questions': 3,
                'passing_score': 70.0,
                'time_limit': 15
            },
            'questions': [
                {
                    'question_text': 'Solar PV converts sunlight into?',
                    'question_type': 'multiple_choice',
                    'options': ['Heat only', 'Electrical energy', 'Mechanical torque directly', 'Nuclear energy'],
                    'correct_answer': 'Electrical energy',
                    'explanation': 'Photovoltaic cells generate electrical output from light.',
                    'points': 1.0,
                    'order': 1
                },
                {
                    'question_text': 'Battery systems can smooth renewable intermittency.',
                    'question_type': 'true_false',
                    'correct_answer': 'True',
                    'explanation': 'Storage balances generation-demand mismatch.',
                    'points': 1.0,
                    'order': 2
                },
                {
                    'question_text': 'Name one renewable source besides solar.',
                    'question_type': 'short_answer',
                    'correct_answer': 'Wind',
                    'explanation': 'Common sources include wind, hydro, biomass, and geothermal.',
                    'points': 1.0,
                    'order': 3
                }
            ]
        }
    ]

    for quiz_data in quizzes_data:
        lesson = lessons[quiz_data['lesson_title']]
        quiz_payload = dict(quiz_data['payload'])
        quiz_payload['lesson_id'] = lesson.id
        quiz = get_or_create_quiz(quiz_payload)

        for question in quiz_data['questions']:
            question_payload = dict(question)
            question_payload['quiz_id'] = quiz.id
            get_or_create_quiz_question(question_payload)

    print(
        "Sample data sync complete: "
        f"lessons +{created_counts['lessons']}, "
        f"practice_problems +{created_counts['practice_problems']}, "
        f"quizzes +{created_counts['quizzes']}, "
        f"questions +{created_counts['questions']}"
    )

def init_db():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Keep seeding idempotent so new curriculum content can be appended safely.
        add_sample_data()

if __name__ == '__main__':
    init_db()
