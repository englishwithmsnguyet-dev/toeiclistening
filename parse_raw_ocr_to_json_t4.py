import json
import re
import urllib.request
import urllib.parse
import time
import os

CACHE_FILE = "/Users/nguyetpham/Documents/MINH NGUYỆT/TEACHING/TÀI LIỆU DẠY BẢN MỚI/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/translation_cache.json"
if not os.path.exists(CACHE_FILE):
    CACHE_FILE = "translation_cache.json"

db_path = "/Users/nguyetpham/Documents/MINH NGUYỆT/TEACHING/TÀI LIỆU DẠY BẢN MỚI/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part03_data.json"
js_path = "/Users/nguyetpham/Documents/MINH NGUYỆT/TEACHING/TÀI LIỆU DẠY BẢN MỚI/TOEIC 2026/BÀI GIẢNG/toeic_listening_web/data/part03_data.js"

# Load translation cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)
    except:
        translation_cache = {}
else:
    translation_cache = {}

def save_cache():
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save translation cache: {e}")

def translate_text(text, target_lang="vi"):
    text = text.strip()
    if not text:
        return ""
    cache_key = f"{target_lang}:{text}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]
    
    prefix = ""
    prefix_match = re.match(r"^([A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*)(.*)", text, re.DOTALL)
    if prefix_match:
        prefix = prefix_match.group(1)
        text_to_translate = prefix_match.group(2)
    else:
        text_to_translate = text

    clean_text = re.sub(r"<[^>]+>", "", text_to_translate).strip()
    if not clean_text:
        return text

    for attempt in range(3):
        try:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(clean_text)
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                translated = "".join([part[0] for part in result[0] if part[0]])
                final_val = prefix + translated
                translation_cache[cache_key] = final_val
                save_cache()
                return final_val
        except Exception as e:
            time.sleep(1)
    return text

def clean_html(text):
    return re.sub(r"<[^>]+>", "", text).strip()

def generate_explanation(correct_letter, vi_choice_text, en_key_line, vi_key_line):
    en_clean = clean_html(en_key_line)
    en_clean_no_speaker = re.sub(r"^[A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*", "", en_clean).strip()
    en_clean_no_num = re.sub(r"\(\d+\)\s*", "", en_clean_no_speaker).strip()

    vi_clean = clean_html(vi_key_line)
    vi_clean_no_speaker = re.sub(r"^[A-Za-z0-9]+[-A-Za-z0-9]*\s*:\s*", "", vi_clean).strip()
    vi_clean_no_num = re.sub(r"\(\d+\)\s*", "", vi_clean_no_speaker).strip()

    # Uses high-contrast royal blue #3b82f6 (var(--color-blue)) for explanation box
    return (
        f"<strong style='color: var(--success);'>ĐÁP ÁN ĐÚNG LÀ {correct_letter}</strong> (<em>{vi_choice_text}</em>).<br>"
        f"<div style='margin-top: 8px; border-left: 3px solid #3b82f6; padding-left: 10px; background: rgba(59, 130, 246, 0.02); padding-top: 4px; padding-bottom: 4px;'>"
        f"<strong>Từ khóa trong bài nghe:</strong><br>"
        f"<span style='color: var(--text-main); font-weight: 500;'>\"{en_clean_no_num}\"</span><br>"
        f"<span style='color: var(--text-muted); font-size: 0.9rem;'>→ \"{vi_clean_no_num}\"</span>"
        f"</div>"
    )

raw_sets = [
    {
        "q_num": "32-34",
        "audio": "E26-T04-32-34.mp3",
        "transcript": [
            "W: Good morning. (32) Thanks for coming to tour this apartment building.",
            "M: I'm glad I could visit in person. (33) I've always wanted to live in this neighborhood—it's so beautiful. This building is brand-new, isn't it?",
            "W: Yes. In fact, you'd be among the very first tenants if you decide to move here. Before you look at some apartments, (34) would you please sign your name here in our guest book?",
            "M: Oh, of course."
        ],
        "questions": [
            {
                "id": 32,
                "question": "Who most likely is the woman?",
                "choices": {
                    "A": "A landscape architect",
                    "B": "An interior designer",
                    "C": "A real estate agent",
                    "D": "A building inspector"
                },
                "answer": "C"
            },
            {
                "id": 33,
                "question": "What is the man looking forward to?",
                "choices": {
                    "A": "Living in a particular area",
                    "B": "Walking to work",
                    "C": "Going on vacation",
                    "D": "Saving money for a house"
                },
                "answer": "A"
            },
            {
                "id": 34,
                "question": "What does the woman ask for?",
                "choices": {
                    "A": "Some references",
                    "B": "Some identification",
                    "C": "A signature",
                    "D": "A payment"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "35-37",
        "audio": "E26-T04-35-37.mp3",
        "transcript": [
            "W: Chen, I hope all is going well on your first day. (35) I saw you have some scheduled seafood deliveries across the bay in the Morgan District. Why haven't you left yet?",
            "M: I wasn't going to head over to that particular area for another hour. Do the restaurants in the Morgan District want their deliveries earlier than scheduled?",
            "W: No, but (36) I'm concerned about Bay Bridge traffic. It's routinely congested with vehicles. So you should always add at least an extra hour to your trip out there.",
            "M: Thanks for the tip. (37) I'll also check traffic webcams on the highway agency's Web site."
        ],
        "questions": [
            {
                "id": 35,
                "question": "What most likely is the man's job?",
                "choices": {
                    "A": "Boat crew member",
                    "B": "Restaurant owner",
                    "C": "Seafood inspector",
                    "D": "Delivery truck driver"
                },
                "answer": "D"
            },
            {
                "id": 36,
                "question": "Why is the woman concerned?",
                "choices": {
                    "A": "A road has been temporarily closed.",
                    "B": "A permit has expired.",
                    "C": "Traffic may cause a delay.",
                    "D": "Some supplies are no longer available."
                },
                "answer": "C"
            },
            {
                "id": 37,
                "question": "What does the man say he will check?",
                "choices": {
                    "A": "Some webcams",
                    "B": "A list of ingredients",
                    "C": "An address",
                    "D": "Some maps"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "38-40",
        "audio": "E26-T04-38-40.mp3",
        "transcript": [
            "M: This morning I got an e-mail from (38) Pelicon, a local producer of beauty products. They're interested in purchasing lanolin from us to use in their new line of all-natural makeup.",
            "W: I'm not sure about that. We're a fairly small farm, and we already sell lanolin to another local business. (39) I'm worried that we don't produce enough lanolin to meet the demand of another client. I don't want to expand and take on more wool production.",
            "M: But (40) our contract with the business we currently supply lanolin to has almost expired—there's no guarantee it will be renewed. I think you should at least read Pelicon's proposal.",
            "W: Sure. Can you forward me the e-mail?"
        ],
        "questions": [
            {
                "id": 38,
                "question": "According to the man, what does Pelicon produce?",
                "choices": {
                    "A": "Household cleaners",
                    "B": "Cosmetics",
                    "C": "Industrial textiles",
                    "D": "Pharmaceuticals"
                },
                "answer": "B"
            },
            {
                "id": 39,
                "question": "What does the woman say she is concerned about?",
                "choices": {
                    "A": "Hiring skilled workers",
                    "B": "Securing a bank loan",
                    "C": "Finding transportation",
                    "D": "Making enough product"
                },
                "answer": "D"
            },
            {
                "id": 40,
                "question": "Why does the man recommend reading an e-mail?",
                "choices": {
                    "A": "To consider a business proposal",
                    "B": "To prepare for a client meeting",
                    "C": "To view some construction plans",
                    "D": "To learn the details of a complaint"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "41-43",
        "audio": "E26-T04-41-43.mp3",
        "transcript": [
            "M: Nisreen? This is Lewis. (41) I heard you're going to be working for our company overseas, in the New Zealand office. What a great opportunity!",
            "W: Yes, thank you. I start next month, and I'm really excited.",
            "M: I'm calling to touch base with you about some of our vendor contracts. (42) It's time to renew the contracts, and I wanted to ask you to take care of that before you left.",
            "W: No problem. I know where those files are located on our shared computer drive. (43) I'll just need the password to access them."
        ],
        "questions": [
            {
                "id": 41,
                "question": "What will the woman do next month?",
                "choices": {
                    "A": "Reorganize a department",
                    "B": "Attend a conference",
                    "C": "Relocate to an overseas office",
                    "D": "Take a vacation"
                },
                "answer": "C"
            },
            {
                "id": 42,
                "question": "What does the man want the woman to do?",
                "choices": {
                    "A": "Help with some contracts",
                    "B": "Prepare a project timeline",
                    "C": "Update some software",
                    "D": "Call a sales representative"
                },
                "answer": "A"
            },
            {
                "id": 43,
                "question": "What does the woman ask the man for?",
                "choices": {
                    "A": "Some employee names",
                    "B": "Some credit card information",
                    "C": "A file password",
                    "D": "A telephone number"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "44-46",
        "audio": "E26-T04-44-46.mp3",
        "transcript": [
            "W: Hi. (44) This is Giovanni Marino's agent. I'm calling to reschedule his planned appearance on the Sunday Morning Show.",
            "M: Right. We have him booked to appear on the show in July to promote (45) his new movie.",
            "W: Unfortunately, (45) the movie he's acting in is behind schedule, and he'll now be on location through the end of August.",
            "M: Hmm, I see. Let me look at our guest calendar. I have a slot I'm looking to fill on September fourteenth—would that work?",
            "W: Yes, that would be great, thanks.",
            "M: All right. (46) I'll update the contract with the new date and e-mail it to you."
        ],
        "questions": [
            {
                "id": 44,
                "question": "Why is the woman calling?",
                "choices": {
                    "A": "To negotiate a payment",
                    "B": "To reschedule an appearance",
                    "C": "To book a venue",
                    "D": "To ask about security"
                },
                "answer": "A"
            },
            {
                "id": 45,
                "question": "Who most likely is Giovanni Marino?",
                "choices": {
                    "A": "An actor",
                    "B": "A politician",
                    "C": "A writer",
                    "D": "A photographer"
                },
                "answer": "C"
            },
            {
                "id": 46,
                "question": "What will the man send in an e-mail?",
                "choices": {
                    "A": "A revised contract",
                    "B": "A reimbursement form",
                    "C": "An invitation to a video conference",
                    "D": "Directions to a location"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "47-49",
        "audio": "E26-T04-47-49.mp3",
        "transcript": [
            "M1: Hello, Usha. Hi, Pablo.",
            "W: Hey, Konstantin. (47) We're talking about our thoughts on the new company policy for remote workers. On the days I have to come into the office, I always worry about finding an appropriate workstation.",
            "M2: Yeah, I don't like the unpredictability either. Why can't we just sign up for our workstation sometime in advance? What do you think about it?",
            "M1: These are good points. (48) Let's all go to the director to discuss this with her.",
            "M2: (48) I believe she's in her office, so now's a good time.",
            "W: Oh, I can't go now. (49) I have a report to finalize by noon."
        ],
        "questions": [
            {
                "id": 47,
                "question": "What are the speakers discussing?",
                "choices": {
                    "A": "A conference schedule",
                    "B": "A company policy",
                    "C": "A catering menu",
                    "D": "A supply order"
                },
                "answer": "B"
            },
            {
                "id": 48,
                "question": "What do the men want to do?",
                "choices": {
                    "A": "Rent a car",
                    "B": "Go to a restaurant",
                    "C": "Speak with a manager",
                    "D": "Change some flight reservations"
                },
                "answer": "C"
            },
            {
                "id": 49,
                "question": "What does the woman say she needs to do now?",
                "choices": {
                    "A": "Work on a report",
                    "B": "Meet with a client",
                    "C": "Print some materials",
                    "D": "Check her e-mails"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "50-52",
        "audio": "E26-T04-50-52.mp3",
        "transcript": [
            "W: OK, Mr. Jebreen. (50) Here's your new library card. Remember that you can borrow books, CDs, and DVDs from our collection with it.",
            "M: Thank you. I read somewhere that people can also borrow digital items.",
            "W: Yes! (51) We offer the Cloud-Camel application. All you have to do is download the app and use the information on your card to set up an account.",
            "M: That's great. (52) I go on a business trip every month, so having easy access to online content will be convenient."
        ],
        "questions": [
            {
                "id": 50,
                "question": "Who most likely is the woman?",
                "choices": {
                    "A": "A journalist",
                    "B": "A librarian",
                    "C": "A musician",
                    "D": "A software developer"
                },
                "answer": "C"
            },
            {
                "id": 51,
                "question": "What does the woman recommend that the man do?",
                "choices": {
                    "A": "Consult a manual",
                    "B": "Sign up for a class",
                    "C": "Listen to some music",
                    "D": "Use a particular mobile app"
                },
                "answer": "D"
            },
            {
                "id": 52,
                "question": "What does the man say happens each month?",
                "choices": {
                    "A": "He publishes a blog post.",
                    "B": "He meets with a social group.",
                    "C": "He travels for work.",
                    "D": "He volunteers for a community event."
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "53-55",
        "audio": "E26-T04-53-55.mp3",
        "transcript": [
            "W: (53) Have you reviewed the data from the workplace survey? You really should. It looks like most staff feel positive about the direction that the company is going in. (54) But almost 40 percent feel like their individual contributions aren't being recognized.",
            "M: Well, the company's certainly had other priorities. I wonder how the management team's going to respond.",
            "W: (55) I've suggested many times that they give out awards every quarter for exceptional performance. Maybe now they'll finally start doing it."
        ],
        "questions": [
            {
                "id": 53,
                "question": "What does the woman want the man to look at?",
                "choices": {
                    "A": "A marketing plan",
                    "B": "A conference calendar",
                    "C": "Schedule changes",
                    "D": "Survey results"
                },
                "answer": "D"
            },
            {
                "id": 54,
                "question": "What does the man imply when he says, \"the company's certainly had other priorities\"?",
                "choices": {
                    "A": "His workload has decreased.",
                    "B": "He is not responsible for some results.",
                    "C": "Some criticism is accurate.",
                    "D": "Some decisions led to a successful outcome."
                },
                "answer": "A"
            },
            {
                "id": 55,
                "question": "What has the woman suggested in the past?",
                "choices": {
                    "A": "Rewarding staff performance",
                    "B": "Extending business hours",
                    "C": "Encouraging professional development",
                    "D": "Organizing team-building events"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "56-58",
        "audio": "E26-T04-56-58.mp3",
        "transcript": [
            "W1: (56) Oliver, have you finished the maintenance check on the small airplane that came in this morning? The owner's hoping to fly it this weekend.",
            "M: I finished checking it earlier this morning. It needs a new fuel injection pump, so I've asked Camille to order one. Oh, here she comes. Camille, will the new pump arrive today?",
            "W2: (57) Unfortunately, no. The manufacturer said there'll be a delay, and it won't arrive until Monday.",
            "W1: I better let the customer know. (58) She was planning to fly the plane to Toronto this weekend for a friend's wedding. She'll need to find another way to get there."
        ],
        "questions": [
            {
                "id": 56,
                "question": "What did the man perform a maintenance check on?",
                "choices": {
                    "A": "A motorcycle",
                    "B": "A car",
                    "C": "A bus",
                    "D": "An airplane"
                },
                "answer": "C"
            },
            {
                "id": 57,
                "question": "What news does Camille share?",
                "choices": {
                    "A": "A delivery will be delayed.",
                    "B": "An expense will increase.",
                    "C": "A staff member is unavailable.",
                    "D": "A rainstorm is predicted."
                },
                "answer": "D"
            },
            {
                "id": 58,
                "question": "Why is the customer traveling to Toronto?",
                "choices": {
                    "A": "To participate in a competition",
                    "B": "To present at a conference",
                    "C": "To attend a wedding",
                    "D": "To sign a contract"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "59-61",
        "audio": "E26-T04-59-61.mp3",
        "transcript": [
            "M: (59) Hello, you've reached the customer service line for Quality Internet Service. How can I help you?",
            "W: I'm Mona Shannak, and my account number's PK62H5. I'd like to close my account on June thirtieth.",
            "M: Oh, have you been experiencing issues with the service?",
            "W: (60) Actually, my company has asked me to relocate to Spain.",
            "M: That's exciting! I'll take care of your request for you then.",
            "W: Thank you—I appreciate that.",
            "M: When I'm done updating your records, (61) would you be willing to stay on the phone line to take a survey about your experience as a customer?",
            "W: Certainly."
        ],
        "questions": [
            {
                "id": 59,
                "question": "What type of business does the man work for?",
                "choices": {
                    "A": "An electric company",
                    "B": "An Internet provider",
                    "C": "A landscaping service",
                    "D": "A water supplier"
                },
                "answer": "A"
            },
            {
                "id": 60,
                "question": "What does the woman imply when she says, \"my company has asked me to relocate to Spain\"?",
                "choices": {
                    "A": "She enjoys traveling for business.",
                    "B": "She was surprised by a job transfer.",
                    "C": "She has no complaints about a service.",
                    "D": "She would like paperwork sent to a different address."
                },
                "answer": "D"
            },
            {
                "id": 61,
                "question": "What does the woman agree to do?",
                "choices": {
                    "A": "Pay a bill",
                    "B": "Read a policy",
                    "C": "Return a call",
                    "D": "Complete a survey"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "62-64",
        "audio": "E26-T04-62-64.mp3",
        "graphic": "data/graphics/ets26_t04_q62_64.png",
        "transcript": [
            "M: Hi, Ms. Rossi. (62) I understand you're concerned about a charge that appears on the statement for your business account.",
            "W: Yes, (63) I have a question about the charge on May 3. I don't remember purchasing anything for that amount.",
            "M: Let me review your statement now. Hmm. It looks like that purchase was made abroad. So an international transaction fee was added to the purchase amount.",
            "W: Oh, yes—I was out of the country at that time. Thanks for clarifying. (64) Can you provide me with a list of all the bank fees for transactions made abroad?",
            "M: (64) Yes, of course. Here's a document that lists all the information."
        ],
        "questions": [
            {
                "id": 62,
                "question": "Where does the man most likely work?",
                "choices": {
                    "A": "At an airport",
                    "B": "At a bank",
                    "C": "At a real estate agency",
                    "D": "At a department store"
                },
                "answer": "B"
            },
            {
                "id": 63,
                "question": "Look at the graphic. Which amount does the woman ask about?",
                "choices": {
                    "A": "$203.00",
                    "B": "$350.00",
                    "C": "$75.50",
                    "D": "$83.15"
                },
                "answer": "A"
            },
            {
                "id": 64,
                "question": "What does the man give the woman?",
                "choices": {
                    "A": "An updated statement",
                    "B": "A list of fees",
                    "C": "A discount card",
                    "D": "A brochure"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "65-67",
        "audio": "E26-T04-65-67.mp3",
        "graphic": "data/graphics/ets26_t04_q65_67.png",
        "transcript": [
            "M: Magali, were you able to reserve the performing arts center for the piano concert?",
            "W: Yes. (65) I booked their main auditorium for that day. They're sending me the contract.",
            "M: (65) Thanks for doing that.",
            "W: No problem. Hopefully, it'll be as successful as last year.",
            "M: We sold 2,000 tickets last year, but we had three celebrity performers. (66) I'm worried we won't sell as many tickets this year.",
            "W: Well, Xinyu Gu is a very popular pianist. And she's staying after the concert to sign autographs. Which reminds me, where should we set up the table for that?",
            "M: Good question. Hmm. The café should be closed by then. (67) Let's set it up next to the café."
        ],
        "questions": [
            {
                "id": 65,
                "question": "What does the man thank the woman for doing?",
                "choices": {
                    "A": "Printing programs",
                    "B": "Setting up lighting",
                    "C": "Reserving a venue",
                    "D": "Paying a performer"
                },
                "answer": "C"
            },
            {
                "id": 66,
                "question": "What does the man say he is worried about?",
                "choices": {
                    "A": "Reviews from critics",
                    "B": "Ticket sales",
                    "C": "A performance schedule",
                    "D": "The cost of merchandise"
                },
                "answer": "B"
            },
            {
                "id": 67,
                "question": "Look at the graphic. Where will a table be set up?",
                "choices": {
                    "A": "At location 1",
                    "B": "At location 2",
                    "C": "At location 3",
                    "D": "At location 4"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "68-70",
        "audio": "E26-T04-68-70.mp3",
        "graphic": "data/graphics/ets26_t04_q68_70.png",
        "transcript": [
            "M: Welcome to the garden center. Can I help you?",
            "W: Hi. (68) I've started growing rose bushes, and I've heard they require special care. (68) Are there any products you can recommend?",
            "M: Yes! But first, I'd like to show you a great resource on our Web site. Have you seen our blog?",
            "W: No, I haven't.",
            "M: We have monthly posts on many gardening topics, and (69) there's a recent one about growing roses.",
            "W: (69) I'll check it out! Thanks so much.",
            "M: You're welcome. Now—(70) let me show you our fertilizers. They're in aisle six."
        ],
        "questions": [
            {
                "id": 68,
                "question": "Why is the woman at the garden center?",
                "choices": {
                    "A": "To enroll in a course",
                    "B": "To join a gardening club",
                    "C": "To buy some supplies",
                    "D": "To return a purchase"
                },
                "answer": "C"
            },
            {
                "id": 69,
                "question": "Look at the graphic. Which month's post will the woman most likely read?",
                "choices": {
                    "A": "May's post",
                    "B": "June's post",
                    "C": "July's post",
                    "D": "August's post"
                },
                "answer": "A"
            },
            {
                "id": 70,
                "question": "What kind of products will the man show to the woman?",
                "choices": {
                    "A": "Indoor plants",
                    "B": "Plant fertilizers",
                    "C": "Gardening tools",
                    "D": "Irrigation systems"
                },
                "answer": "B"
            }
        ]
    }
]

print("Processing and translating ETS 2026 Test 4 Part 3...")

processed_practice_sets = []

for s_idx, r_set in enumerate(raw_sets):
    print(f"Translating set {s_idx + 1}/13 (Questions {r_set['q_num']})...")
    
    # Translate Transcript
    vi_transcript = [translate_text(line) for line in r_set["transcript"]]
    
    # Process Questions
    processed_questions = []
    for q in r_set["questions"]:
        q_clean = q["question"].strip()
        
        # Translate question text
        vi_q_text = translate_text(q_clean)
        
        # Translate Choices
        vi_choices = {}
        for letter, choice_val in q["choices"].items():
            vi_choices[letter] = translate_text(choice_val)
        
        # Determine exact keywords line for explanation
        ans_letter = q["answer"]
        key_tag = f"({q['id']})"
        
        en_key_line = ""
        vi_key_line = ""
        for idx, line in enumerate(r_set["transcript"]):
            if key_tag in line:
                en_key_line = line
                if idx < len(vi_transcript):
                    vi_key_line = vi_transcript[idx]
                break
        
        if not en_key_line:
            en_key_line = r_set["transcript"][0]
            vi_key_line = vi_transcript[0]
            
        explanation = generate_explanation(ans_letter, vi_choices[ans_letter], en_key_line, vi_key_line)
        
        processed_questions.append({
            "id": q["id"],
            "slide_index": 3000 + q["id"],
            "question": q["question"],
            "choices": q["choices"],
            "answer": q["answer"],
            "vietnamese_question": vi_q_text,
            "vietnamese_choices": vi_choices,
            "explanation": explanation
        })
        
    p_set = {
        "set_index": s_idx + 1,
        "audio": r_set["audio"],
        "questions": processed_questions,
        "transcript": r_set["transcript"],
        "vietnamese_transcript": vi_transcript
    }
    
    if "graphic" in r_set:
        p_set["graphic"] = r_set["graphic"]
        
    processed_practice_sets.append(p_set)

# Load existing database
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

# Retain existing entries, and only filter out any previous duplicate 'ets_test_04'
db = [s for s in db if s.get("id") != "ets_test_04"]

# Create and add ets_test_04
new_section = {
    "id": "ets_test_04",
    "title": "ETS 2026 - TEST 04",
    "type": "test",
    "theory": [],
    "vocabulary": [],
    "practice_sets": processed_practice_sets
}

db.append(new_section)

# Save to JSON
with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

# Save back to JS data file
with open(js_path, "w", encoding="utf-8") as f:
    f.write("window.part03Data = ")
    json.dump(db, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print("SUCCESS: ETS 2026 Test 4 successfully compiled and written to database!")
