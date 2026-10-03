"""All writing tasks used in the Writing Task lessons (topic 50) - ONE version of each, used everywhere.

Shape checked against the real English writing tasks (Summer 2020-2025): 140-200 words, 2-3 paragraphs:
  1. the current situation and how it works (facts, sometimes the purpose),
  2. the change / proposal with concrete details (numbers, who, how),
  3. the sides' reasons (often two per side), sometimes a named kind of authority,
then the question in bold, ending "Give reasons for your answer."
Question types seen: yes/no ("Are you in favor of ...?", "should ...?"), "which of the two methods is preferable?",
"should X be a right or a privilege?". All tasks here are ORIGINAL (the camera and tax tasks are the teacher's own
running examples). No real NITE task is copied.
"""
from writing_assets import prompt_box, EXAMPLE_PROMPT, EXAMPLE_QUESTION

T = {}


def task(key, title, paras, q):
    T[key] = dict(title=title, paras=paras, q=q)


# ------------------------------------------------------------------ the teacher's running examples
task('camera', 'Face-recognition cameras', [
    "In recent years, officials in the security services have been promoting a bill to set up a national network "
    "of face-recognition cameras in public spaces. Today's technology can identify people and objects in real time "
    "with a high degree of certainty, so it would be possible to identify any person, vehicle or other object caught "
    "on camera, provided that their image already exists in the database.",
    "According to the bill, this information would help to fight criminal and security offences that harm the "
    "population: suspicious activity could be identified before an offence is committed, illegal activity could be "
    "stopped while it is taking place, and offenders could be caught after the event.",
    "Supporters of the bill claim that such a system would reduce, and even completely eliminate, criminal and "
    "security incidents in the monitored areas. Opponents believe that it would seriously harm privacy, and that it "
    "is unthinkable for the security services to be able to follow our every step.",
], 'In your opinion, should the security services be allowed to install face-recognition cameras in public '
   'spaces? Give reasons for your answer.')

task('tax', 'Reduced tax for large companies', [
    "In most countries, companies pay a fixed percentage of their profits as tax, and this money funds public "
    "services such as schools, hospitals and roads. Because many countries compete to attract large international "
    "companies, which build factories and employ thousands of workers, some governments offer these companies a "
    "reduced rate of tax - in some cases less than half of the ordinary rate - for ten years or more.",
    "Supporters of this policy argue that without the tax benefit, large companies would simply open their "
    "factories in another country, and the jobs, the investment and the tax they do pay would be lost. Opponents "
    "argue that it is unfair for the richest firms to pay a lower rate than small businesses, and that the "
    "missing income is eventually paid for by ordinary citizens, through higher taxes or poorer public services.",
], 'In your opinion, should the state charge large companies a reduced rate of tax? Give reasons for your answer.')

# ------------------------------------------------------------------ examples inside the lessons
# 'fourday' is the opening essay (vr50-a-baseline) and its retake (workshop 19) ONLY - never a worked example in a
# lesson, so that the before/after comparison stays fair. Lessons use 'lights' instead (original task).
task('fourday', 'A four-day school week', EXAMPLE_PROMPT, EXAMPLE_QUESTION)

task('lights', 'Street lights at night', [
    "In most towns, street lights stay on from dusk until dawn, and street lighting is one of the largest items on "
    "a town's electricity bill. Modern street lamps can be switched on and off remotely, street by street.",
    "In recent years, several towns have begun to switch off the lights in residential streets between 1 a.m. and "
    "5 a.m., when few people are outside. Main roads, junctions and pedestrian crossings stay lit all night, and "
    "the towns report that they save about a third of their lighting costs.",
    "Supporters argue that the money saved can fund other local services, and that darker nights save energy and "
    "help residents sleep. Opponents argue that people who come home late, such as night-shift workers, will "
    "feel unsafe in dark streets, and that unlit pavements may lead to more burglaries and to falls among "
    "elderly residents.",
], 'In your opinion, should towns switch off the lights in residential streets in the middle of the night? Give '
   'reasons for your answer.')

task('bus', 'Free local buses', [
    "In most cities, passengers on local buses pay a fare for each trip or buy a monthly pass. The fares cover part "
    "of the cost of the service, and the city pays the rest from its budget.",
    "Recently, several cities have abolished bus fares altogether, so that anyone can board any local bus free of "
    "charge. To cover the lost income, these cities have raised local taxes slightly and cut other spending.",
    "Supporters of free buses argue that they encourage people to leave their cars at home, which reduces traffic "
    "jams and air pollution, and that they help residents on low incomes reach work, study and medical services. "
    "Opponents argue that people who can afford the fare will now travel at the expense of all taxpayers, and that "
    "the money would be better spent on more frequent and more reliable buses.",
], 'In your opinion, should cities make local buses free of charge? Give reasons for your answer.')

task('bus2', 'Free public transport: advantages and disadvantages', T['bus']['paras'],
     'In your opinion, what are the advantages and disadvantages of free public transport, for the city\'s '
     'residents and for the city itself? Give reasons for your answer.')

task('phones', 'Phones at school', [
    "Most secondary-school students carry a smartphone. Until recently, schools usually allowed students to keep "
    "their phones, provided that they were switched off during lessons.",
    "In the past few years, a growing number of schools have introduced a stricter rule: students hand in their "
    "phones to the school office when they arrive in the morning and get them back only when they leave. Some "
    "education ministries are considering making this rule compulsory in all schools.",
    "Supporters of the rule argue that it improves concentration in class and reduces online bullying during school "
    "hours, and that breaks are spent talking and playing instead of looking at screens. Opponents argue that it "
    "cuts students off from their parents in an emergency, and that it prevents teachers from using the phone as a "
    "learning tool.",
], 'In your opinion, should schools collect students\' phones for the whole school day? Give reasons for your '
   'answer.')

# ------------------------------------------------------------------ workshop tasks (carried through the lessons)
task('social', 'A minimum age for social networks', [
    "Social networks allow users to share photos, videos and messages with friends and with the public. Most "
    "networks officially require users to be at least 13 years old, but in practice they do not check a user's "
    "age, and many younger children open accounts by entering a false date of birth.",
    "Several countries are now considering a law that would raise the minimum age to 16 and require the networks "
    "to verify every new user's age, for example by means of an identity document or a parent's approval. "
    "Networks that fail to do so would be fined.",
    "Supporters of the law argue that young teenagers are especially vulnerable to online bullying and to "
    "comparing themselves with others, and that this harms their mental health. Opponents argue that the law would "
    "force every user to hand over personal documents, and that teenagers who are cut off from the networks their "
    "friends use would simply find ways around the ban.",
], 'In your opinion, should the minimum age for opening an account on a social network be raised to 16? Give '
   'reasons for your answer.')

task('organ', 'Organ donation: two methods', [
    "Thousands of patients wait for an organ transplant every year, and many of them die before a suitable organ "
    "is found. In some countries, a person becomes an organ donor only if he or she has signed a donor card; "
    "without such a card, the organs are not used after death unless the family agrees.",
    "Other countries use the opposite method: every adult is considered a donor after death, unless he or she has "
    "registered a refusal in advance. In these countries, the rate of organ donation is usually higher.",
    "Supporters of the second method argue that most people are in favor of donation but never get round to "
    "signing a card, so the second method simply reflects their real wishes and saves lives. Opponents argue that "
    "a decision about a person's body must be made actively by that person, and that the silence of someone who "
    "was never informed cannot be considered consent.",
], 'In your opinion, which of the two methods of organ donation is preferable? Give reasons for your answer.')

task('exams', 'Final exams or school projects', [
    "In many countries, students finish secondary school by sitting national written exams. All students in the "
    "country answer the same questions on the same day, and the results play an important part in admission to "
    "universities.",
    "Some education experts propose replacing most of these exams with projects carried out at school during the "
    "last two years: research papers, experiments and presentations, assessed by the students' own teachers and "
    "checked by a sample of external examiners.",
    "Supporters of the proposal argue that one day of exams measures mainly memory and the ability to cope with "
    "pressure, while projects develop the skills needed in higher education and at work. Opponents argue that "
    "grades given by students' own teachers are less reliable and easier to influence, and that universities "
    "would lose a fair way of comparing students from different schools.",
], 'In your opinion, should national written exams be replaced by school-based projects? Give reasons for your '
   'answer.')

task('grades', 'Paying students for grades', [
    "Schools in low-income neighborhoods often have lower achievement and higher dropout rates than schools in "
    "wealthier areas. Many programs have tried to close this gap, for example by adding lessons or smaller classes.",
    "Recently, a number of local authorities have tried a different approach: students in these schools receive a "
    "small sum of money for every improvement in their grades and for full attendance during the term. The money "
    "is paid into a savings account that the student can use after finishing school.",
    "Supporters of the program argue that it gives students an immediate reason to invest in their studies, and "
    "that the savings help them continue to higher education. Opponents argue that paying for grades teaches "
    "students to learn only for a reward, and that when the payments stop, their motivation will be lower than "
    "before.",
], 'In your opinion, should students be paid for improving their grades? Give reasons for your answer.')

task('voting', 'Compulsory voting', [
    "In most democratic countries, voting in elections is a right but not a duty, and in many of them fewer than "
    "two-thirds of the citizens who are entitled to vote actually do so. Turnout is usually lowest among young "
    "people and among citizens with low incomes.",
    "A small number of countries have made voting compulsory: citizens who do not vote without a valid reason must "
    "pay a modest fine. In these countries, turnout is usually above 90 percent.",
    "Supporters of compulsory voting argue that when almost everyone votes, the government represents the whole "
    "population and not only the groups that tend to vote. Opponents argue that the freedom not to vote is part of "
    "democracy, and that forcing uninterested citizens to vote adds random votes rather than considered ones.",
], 'In your opinion, should voting in national elections be compulsory? Give reasons for your answer.')

# ------------------------------------------------------------------ practice tasks (the practice section)
task('carfree', 'Car-free city centres', [
    "In most cities, private cars may enter every street, and the city centre is where traffic jams and air "
    "pollution are usually worst. Several European cities have closed the streets of their historic centres to "
    "private cars; only residents, buses, taxis, delivery vans at set hours and emergency vehicles may enter. Parking garages are built at the edge of the centre, and free shuttle buses take visitors inside.",
    "Supporters argue that the closure makes the centre quieter, cleaner and safer, and that pedestrians and "
    "cyclists return to streets that were once full of cars. Opponents, many of them shop owners, argue that "
    "customers who come from outside the city by car will go to shopping centres on the outskirts instead, and "
    "that elderly and disabled people will find the centre harder to reach.",
], 'In your opinion, should city centres be closed to private cars? Give reasons for your answer.')

task('volunteer', 'Compulsory volunteering', [
    "Many young people volunteer during their school years - in hospitals, youth movements, or with elderly people "
    "who live alone. In most schools, however, volunteering is a personal choice.",
    "Some education systems have made community service compulsory: every student must complete sixty hours of "
    "volunteering in the last three years of secondary school in order to receive a school-leaving certificate. "
    "Schools help students find a placement, and the organizations report the hours to the school.",
    "Supporters argue that the requirement exposes young people to parts of society they would otherwise never "
    "meet, and that many of them continue to volunteer afterwards. Opponents argue that volunteering which is forced "
    "is no longer volunteering, and that students who serve only to collect hours may do the work badly and harm "
    "the people they are supposed to help.",
], 'In your opinion, should community service be a requirement for completing secondary school? Give reasons '
   'for your answer.')

task('sugar', 'A tax on sweetened drinks', [
    "Sweetened drinks, such as cola and many fruit drinks, contain large amounts of sugar, and doctors link them to "
    "obesity, diabetes and tooth decay, especially among children.",
    "Several countries have introduced a special tax on these drinks, which raises their price by about 20 percent. "
    "In some of them, the money collected is used to fund sports facilities and healthy meals in schools. After the "
    "tax was introduced, sales of sweetened drinks fell, and some manufacturers reduced the amount of sugar in their "
    "products.",
    "Supporters argue that the tax protects public health and reduces the future costs of treating diseases. "
    "Opponents argue that the state should not decide what adults eat and drink, and that such a tax falls "
    "hardest on families with low incomes, who spend a larger share of their money on food and drink.",
], 'In your opinion, should the state impose a special tax on sweetened drinks? Give reasons for your answer.')

task('er', 'A fee for non-urgent emergency visits', [
    "Hospital emergency rooms treat anyone who arrives, at any hour, free of charge. In recent years, emergency rooms "
    "in many cities have become overcrowded, and patients sometimes wait many hours to be seen. Doctors estimate that "
    "a large share of the visitors have conditions that could be treated at a local clinic.",
    "In response, some health systems have introduced a fee for patients who come to the emergency room without a "
    "referral and are found not to need urgent care. The fee is not charged to children, to patients who are "
    "admitted to the hospital, or to those who arrive by ambulance.",
    "Supporters argue that the fee directs patients to the right service and shortens waiting times for those who "
    "really need emergency care. Opponents argue that patients cannot always judge how serious their condition is, "
    "and that the fear of paying may lead some of them to stay at home when they should not.",
], 'In your opinion, should hospitals charge a fee for non-urgent visits to the emergency room? Give reasons for '
   'your answer.')

task('homework', 'Homework in primary school', [
    "In most primary schools, children receive homework several times a week - exercises in arithmetic, reading and "
    "writing that are meant to practise what was learned in class. Parents are often expected to help and to check "
    "that the work is done.",
    "Some schools have recently abolished homework in the first six grades. Instead, the school day includes a "
    "supervised practice hour, and parents are asked only to read with their children at home.",
    "Supporters of the change argue that homework widens the gap between children whose parents can help them and "
    "children whose parents cannot, and that young children need free time to play and rest. Opponents argue that "
    "homework teaches children responsibility and independent work, and that it lets parents see what their "
    "children are learning.",
], 'In your opinion, should homework be abolished in primary schools? Give reasons for your answer.')

task('rentals', 'Short-term tourist rentals', [
    "Online platforms allow people to rent out their apartments to tourists for a few nights at a time. In popular "
    "cities, many apartments that were once rented to local residents for years are now rented to tourists "
    "throughout the year, because this brings the owners a higher income.",
    "Several cities have therefore limited short-term rentals: an owner may rent out an apartment to tourists for "
    "no more than 90 nights a year, unless it is the owner's own home and he or she lives in it.",
    "Supporters of the limit argue that it returns apartments to the long-term rental market, lowers rents for "
    "residents and keeps neighborhoods from turning into hotels. Opponents argue that owners should be free to "
    "decide how to use their property, and that tourists who stay in apartments spend money in local shops and "
    "restaurants rather than in large hotel chains.",
], 'In your opinion, should cities limit the number of nights an apartment may be rented to tourists? Give '
   'reasons for your answer.')

task('sport', 'Public money for professional sport', [
    "Professional sports teams are usually owned by private investors, who earn money from ticket sales, "
    "broadcasting rights and sponsors. Nevertheless, many cities also support their local teams with public money, "
    "for example by building stadiums or covering part of the teams' expenses. In some cities, this support amounts "
    "to several percent of the annual sports budget.",
    "Supporters of this support argue that a successful local team brings visitors and income to the city, gives "
    "young people role models, and creates a sense of pride and belonging among residents. Opponents argue that "
    "the money should be spent on sports facilities that all residents can use, such as swimming pools and sports "
    "fields in neighborhoods, and that private businesses should not be funded by taxpayers.",
], 'In your opinion, should cities fund professional sports teams with public money? Give reasons for your answer.')

task('retire', 'A fixed retirement age', [
    "In many countries, employees must retire at a fixed age, usually between 62 and 67, and then receive a "
    "pension. Life expectancy has risen considerably, and many people at this age are healthy and want to continue "
    "working.",
    "Some countries have abolished the fixed retirement age. Employees may continue working for as long as they "
    "wish, and an employer may end their employment only for the same reasons that apply to any other worker.",
    "Supporters argue that forcing people to stop working because of their age is discrimination, and that the "
    "economy benefits from their experience. Opponents argue that without a fixed age, older employees will stay in "
    "senior positions longer, so that fewer jobs and promotions will be available to young people, and that "
    "employers will find it harder to plan ahead.",
], 'In your opinion, is a fixed retirement age preferable to allowing employees to continue working as long as '
   'they wish? Give reasons for your answer.')

# ------------------------------------------------------------------ the teacher's own examples (their wording, verbatim)
task('smoking', 'Anti-smoking laws', [
    "In recent years, laws have significantly restricted the areas where smoking is allowed in public. Today, "
    "smoking is prohibited in places like cafés, restaurants, bus stations, and more, and the number of designated "
    "smoking areas has been reduced. Enforcement has also increased, and violators—including business owners who "
    "allow smoking on their premises—face heavy fines.",
    "Supporters of the legislation argue that it protects the health of non-smokers and is therefore morally "
    "justified. On the other hand, critics claim the laws discriminate unfairly against smokers.",
], 'What is your opinion? Are anti-smoking laws justified? Explain your answer.')

task('taxvote', 'Voting rights and taxes', [
    "A bill proposes to deny voting rights to people who don't pay taxes. Supporters say that in a democracy, "
    "rights come with duties, so those who don't pay taxes shouldn't vote. They believe this would encourage tax "
    "payment and benefit the economy and democracy.",
    "Opponents argue voting is a basic right that shouldn't be restricted, and limiting it could harm democracy. "
    "They also say low voter turnout means the bill won't effectively increase tax compliance.",
], 'What do you think? Should non-taxpayers be allowed to vote? Explain your view.')

WORKSHOP = ['social', 'organ', 'exams', 'grades', 'voting']
PRACTICE = ['carfree', 'volunteer', 'sugar', 'er', 'homework', 'rentals', 'sport', 'retire']


def words(key):
    t = T[key]
    return len(' '.join(t['paras']).split())


def box(key, w=1140, x=410, y=40):
    """The task in its frame, placed on the board."""
    t = T[key]
    return dict(prompt_box(t['paras'], t['q'], w=w), x=x, y=y)


def text(key):
    """Plain text of a task (for cards): paragraphs, then the question."""
    t = T[key]
    return '\n'.join(t['paras']) + '\n' + t['q']


def split_task_slides(modules, top=110):
    """A full task box fills most of the board. On a slide where more items appear below the box, keep the box
    (and the lines spoken right after it) on its own slide, and move the rest to a second slide with the same
    title, shifted up."""
    for m in modules:
        out = []
        for sl in m['slides']:
            sc = sl.get('script', [])
            k = next((i for i, x in enumerate(sc) if isinstance(x, tuple) and x[0] == 'A' and x[2].get('k') == 'vis'
                      and x[2].get('w', 0) >= 1000 and x[2].get('h', 0) > 450), None)
            later = [x for x in sc[k + 1:] if isinstance(x, tuple) and x[0] == 'A'] if k is not None else []
            if not later:
                out.append(sl); continue
            box = sc[k][2]
            if all(box.get('y', 0) + box['h'] <= x[2].get('y', 0) <= 760 for x in later):
                out.append(sl); continue
            j = next(i for i in range(k + 1, len(sc)) if isinstance(sc[i], tuple) and sc[i][0] == 'A')
            first = dict(sl, script=sc[:j])
            ys = [x[2]['y'] for x in sc[j:] if isinstance(x, tuple) and x[0] == 'A' and 'y' in x[2]]
            dy = (min(ys) - top) if ys else 0
            rest = [(x[0], x[1], dict(x[2], y=x[2]['y'] - dy)) if isinstance(x, tuple) and x[0] == 'A' and 'y' in x[2]
                    else x for x in sc[j:]]
            out += [first, dict(sl, script=rest)]
        m['slides'] = out
    return modules
