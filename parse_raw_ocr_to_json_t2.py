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
        "audio": "E26-T02-32-34.mp3",
        "transcript": [
            "W: (32) How were your deliveries?",
            "M: Not bad, except at that new residential building on South Street. I had to call them on my phone to come pick up their food. At first, (33) I tried to call on the building intercom, but it's still broken.",
            "W: You're not the first to say that. Last week, a customer called to complain that their food was cold by the time they found it.",
            "M: Maybe we just can't make deliveries there until the landlord fixes the intercom system.",
            "W: (34) I'm going to update the instructions on our mobile app telling customers to meet us at the building's front door. Let's see if that helps."
        ],
        "questions": [
            {
                "id": 32,
                "question": "What kind of work does the man do?",
                "choices": {
                    "A": "He is a tour guide.",
                    "B": "He is a landlord.",
                    "C": "He repairs appliances.",
                    "D": "He delivers food."
                },
                "answer": "D"
            },
            {
                "id": 33,
                "question": "What has caused problems for the speakers' business?",
                "choices": {
                    "A": "Road construction",
                    "B": "Cold weather",
                    "C": "An expired permit",
                    "D": "A broken intercom"
                },
                "answer": "D"
            },
            {
                "id": 34,
                "question": "What will the woman update on a mobile application?",
                "choices": {
                    "A": "Instructions",
                    "B": "Prices",
                    "C": "Photographs",
                    "D": "Hours of operation"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "35-37",
        "audio": "E26-T02-35-37.mp3",
        "transcript": [
            "W: We're getting close to the time of year when (35) we need to begin planning our Theater in the Park series for the summer. We have lots of decisions to make about shows, dates, and performers.",
            "M: You're right. I'll set up a meeting for this month. You know, I had an idea. (36) Why don't we invite community residents to volunteer to help with building sets, painting, and setting up the stage?",
            "W: We could, but I don't know if we'll be able to use volunteers this year. (37) We'll need approval to start that kind of program. It'll take time. Let's check into that for next year."
        ],
        "questions": [
            {
                "id": 35,
                "question": "What industry do the speakers most likely work in?",
                "choices": {
                    "A": "Fitness",
                    "B": "Entertainment",
                    "C": "Landscaping",
                    "D": "Travel"
                },
                "answer": "B"
            },
            {
                "id": 36,
                "question": "What does the man suggest?",
                "choices": {
                    "A": "Providing online access to videos",
                    "B": "Creating volunteer opportunities",
                    "C": "Offering free transportation",
                    "D": "Adding additional time slots"
                },
                "answer": "B"
            },
            {
                "id": 37,
                "question": "Why do the speakers need to wait?",
                "choices": {
                    "A": "Promotional items have not been ordered.",
                    "B": "A facility is not available.",
                    "C": "A budget is too small.",
                    "D": "A program has not been approved."
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "38-40",
        "audio": "E26-T02-38-40.mp3",
        "transcript": [
            "M: Back to our podcast with special guest Kimberly Stuart, (38) who's currently advising our city on business development projects. Before the break, we promised to address the decline of shopping downtown.",
            "W: Yes—and it's been the worst at (39) the kind of stores that sell unique items like antiques and jewelry. These items have always been purchased at brick-and-mortar stores but are now being purchased mostly online.",
            "M: So, do those stores have a future?",
            "W: I think they do, (40) especially if we make a point of organizing live community activities downtown, such as concerts or festivals. When people walk around town, they are likely to browse at stores—and make purchases."
        ],
        "questions": [
            {
                "id": 38,
                "question": "Who is the woman?",
                "choices": {
                    "A": "A store owner",
                    "B": "A television celebrity",
                    "C": "A business consultant",
                    "D": "An event sponsor"
                },
                "answer": "C"
            },
            {
                "id": 39,
                "question": "What does the woman say about online shopping?",
                "choices": {
                    "A": "It is cheaper than buying in person.",
                    "B": "It makes shopping a social experience.",
                    "C": "It is reducing traffic problems in the city.",
                    "D": "It is affecting specialty shops."
                },
                "answer": "D"
            },
            {
                "id": 40,
                "question": "What does the woman suggest doing?",
                "choices": {
                    "A": "Offering clearance sales",
                    "B": "Holding live events",
                    "C": "Meeting with store owners",
                    "D": "Retraining store staff"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "41-43",
        "audio": "E26-T02-41-43.mp3",
        "transcript": [
            "M: (41) Our company has seen a huge spike in sales ever since it launched the rebate program for customers. With the rebate, customers get money back. And they're telling their friends, increasing our sales.",
            "W: Yes. The rebate's been great for our company (42) because now more homeowners have an incentive to install solar panels on their properties, since they're rewarded for the electricity their solar panels produce. But our technicians can't keep up with the high demand.",
            "M: You're right. (43) I'm planning to hire more technicians. I've already received some résumés from potential candidates."
        ],
        "questions": [
            {
                "id": 41,
                "question": "Why have a company's sales increased?",
                "choices": {
                    "A": "A rebate program was started.",
                    "B": "A competitor went out of business.",
                    "C": "A celebrity endorsed the company.",
                    "D": "A product won an award."
                },
                "answer": "A"
            },
            {
                "id": 42,
                "question": "What industry do the speakers most likely work in?",
                "choices": {
                    "A": "Banking",
                    "B": "Telecommunications",
                    "C": "Solar energy",
                    "D": "Music"
                },
                "answer": "C"
            },
            {
                "id": 43,
                "question": "What does the man say he is planning to do?",
                "choices": {
                    "A": "Hire new employees",
                    "B": "Provide additional training",
                    "C": "Upgrade some equipment",
                    "D": "Open another location"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "44-46",
        "audio": "E26-T02-44-46.mp3",
        "transcript": [
            "M: Fernanda, I was just looking at the company calendar, and (44) I noticed that the national electronics trade show is coming up soon.",
            "W: Oh, that's right! It'll be a great opportunity for us to showcase (45) the product that we've been developing—our new robotic vacuum cleaner.",
            "M: We'll need to decide who we want to send to represent our company at the trade show.",
            "W: Well, I know just the right person—Kavi. (46) Kavi does a good job of clearly explaining highly technical concepts in a way that everyone can understand."
        ],
        "questions": [
            {
                "id": 44,
                "question": "What upcoming event are the speakers discussing?",
                "choices": {
                    "A": "A trade show",
                    "B": "A client meeting",
                    "C": "An awards ceremony",
                    "D": "A press conference"
                },
                "answer": "A"
            },
            {
                "id": 45,
                "question": "What product has the speakers' company recently developed?",
                "choices": {
                    "A": "A video game",
                    "B": "A mobile phone",
                    "C": "A lawn mower",
                    "D": "A vacuum cleaner"
                },
                "answer": "D"
            },
            {
                "id": 46,
                "question": "Why does the woman recommend Kavi?",
                "choices": {
                    "A": "He is a good communicator.",
                    "B": "He enjoys traveling.",
                    "C": "He leads a product development team.",
                    "D": "He lives near the event venue."
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "47-49",
        "audio": "E26-T02-47-49.mp3",
        "transcript": [
            "M: Dr. Fuentes, sorry to interrupt. Do you have a minute?",
            "W: Yes. (47) My nine o'clock dental cleaning patient just canceled.",
            "M: (48) I know you're looking for a new receptionist. I'd like to recommend someone for the position.",
            "W: Oh. Who do you have in mind?",
            "M: Well, a former colleague of mine has just moved back to town. Her name's Kelly Graham, and she has several years of experience.",
            "W: OK. (49) Could you tell Kelly to send me her résumé? I'd be happy to look it over."
        ],
        "questions": [
            {
                "id": 47,
                "question": "Where do the speakers most likely work?",
                "choices": {
                    "A": "At a publishing house",
                    "B": "At a dental clinic",
                    "C": "At a financial firm",
                    "D": "At a real estate agency"
                },
                "answer": "B"
            },
            {
                "id": 48,
                "question": "What does the man tell the woman about?",
                "choices": {
                    "A": "A new product",
                    "B": "A schedule change",
                    "C": "A policy update",
                    "D": "A job candidate"
                },
                "answer": "D"
            },
            {
                "id": 49,
                "question": "Why will the man most likely contact Kelly Graham?",
                "choices": {
                    "A": "To plan an office celebration",
                    "B": "To arrange a training session",
                    "C": "To request a document",
                    "D": "To order some supplies"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "50-52",
        "audio": "E26-T02-50-52.mp3",
        "transcript": [
            "M1: Ms. Gao? I'm Hector, and this is my colleague Sergey. Thanks for meeting with us.",
            "W: It's a pleasure to meet you both. How can I help you?",
            "M2: (50) We're making some training videos for our client, FiveStar Industries.",
            "M1: (51) We found your advertisement in a trade publication. We need someone to choose appropriate filming sites at FiveStar's factories, and it said you have lots of experience scouting for industrial locations.",
            "W: Sure. (52) I'd want to start by touring their factories. Can you schedule a time for me to do that next week?",
            "M2: Yes, I'll call them today to arrange it."
        ],
        "questions": [
            {
                "id": 50,
                "question": "What industry do the men work in?",
                "choices": {
                    "A": "Travel",
                    "B": "Manufacturing",
                    "C": "Video production",
                    "D": "Construction"
                },
                "answer": "C"
            },
            {
                "id": 51,
                "question": "How did the men learn about the woman?",
                "choices": {
                    "A": "From her Web site",
                    "B": "From a trade publication",
                    "C": "From a colleague",
                    "D": "From a recruitment agency"
                },
                "answer": "B"
            },
            {
                "id": 52,
                "question": "What does the woman want to do next week?",
                "choices": {
                    "A": "Attend an orientation session",
                    "B": "Visit some facilities",
                    "C": "Interview some applicants",
                    "D": "Finalize a contract"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "53-55",
        "audio": "E26-T02-53-55.mp3",
        "transcript": [
            "M: (53) Our engineering firm has been asked to cut the corporate travel budget by twenty percent, but it won't be easy. The engineering consultants have to travel to meet with clients.",
            "W: Right, and they often travel on short notice. Flight arrangements made at the last minute are expensive, especially for nonstop flights. (54) It would be cheaper if they took connecting flights.",
            "M: Yes, but that can take a lot of time.",
            "W: True. (55) Maybe we can make up for the cost of the flights by economizing on hotels. Let's look into that."
        ],
        "questions": [
            {
                "id": 53,
                "question": "What type of business do the speakers work for?",
                "choices": {
                    "A": "A law firm",
                    "B": "An advertising agency",
                    "C": "An engineering firm",
                    "D": "An event-planning company"
                },
                "answer": "C"
            },
            {
                "id": 54,
                "question": "Why does the man say, \"that can take a lot of time\"?",
                "choices": {
                    "A": "To reject a suggestion",
                    "B": "To express sympathy",
                    "C": "To request additional pay",
                    "D": "To offer assistance"
                },
                "answer": "A"
            },
            {
                "id": 55,
                "question": "What does the woman suggest?",
                "choices": {
                    "A": "Contacting some former clients",
                    "B": "Making reservations early",
                    "C": "Staying at affordable hotels",
                    "D": "Consulting with an expert"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "56-58",
        "audio": "E26-T02-56-58.mp3",
        "transcript": [
            "M1: Thanks for meeting with us, Ms. Azuma. This is Scott Ajibade, one of our senior project managers.",
            "M2: I admire your work, Ms. Azuma.",
            "W: Thank you. I was surprised by your invitation. I typically design jewelry, but (56) your company's known for making computers and mobile phones.",
            "M1: Scott's team is currently working on a smartwatch. But there's a lot of competition, as you know.",
            "M2: (57) We're hoping you can create a fresh design that will help our product stand out.",
            "W: (58) Do you already have an idea of what the watch should look like, or are we starting from scratch?",
            "M2: (58) I have some preliminary sketches we can look at, but none of them seem quite right."
        ],
        "questions": [
            {
                "id": 56,
                "question": "What industry do the men most likely work in?",
                "choices": {
                    "A": "Fashion",
                    "B": "Cosmetics",
                    "C": "Advertising",
                    "D": "Technology"
                },
                "answer": "D"
            },
            {
                "id": 57,
                "question": "Why did the men request a meeting?",
                "choices": {
                    "A": "To negotiate a merger",
                    "B": "To ask for funding",
                    "C": "To discuss a product design",
                    "D": "To suggest a marketing strategy"
                },
                "answer": "C"
            },
            {
                "id": 58,
                "question": "What will the speakers most likely do next?",
                "choices": {
                    "A": "Set a release date",
                    "B": "Sign a contract",
                    "C": "Collect customer feedback",
                    "D": "Review some drawings"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "59-61",
        "audio": "E26-T02-59-61.mp3",
        "transcript": [
            "W: Hi. I'd like to purchase some new carpeting. It's for the waiting room at (59) my hair salon.",
            "M: We have many different styles. (60) Are you looking for something specific?",
            "W: (60) Well, we get a lot of customers walking through, and our current carpeting is a light color.",
            "M: No matter what color you get, all our carpets are durable and can take high amounts of foot traffic. For businesses like yours, I recommend placing a protective mat near the door.",
            "W: That's a good idea.",
            "M: Also, (61) I offer free cleaning services for a year for all purchases."
        ],
        "questions": [
            {
                "id": 59,
                "question": "What type of business does the woman work in?",
                "choices": {
                    "A": "A hair salon",
                    "B": "A real estate agency",
                    "C": "An interior design firm",
                    "D": "A car rental company"
                },
                "answer": "A"
            },
            {
                "id": 60,
                "question": "Why does the woman say, \"our current carpeting is a light color\"?",
                "choices": {
                    "A": "To suggest an expense was not justified",
                    "B": "To express surprise about a decision",
                    "C": "To describe a problem with an order",
                    "D": "To indicate the need to make a change"
                },
                "answer": "D"
            },
            {
                "id": 61,
                "question": "What does the man's business offer?",
                "choices": {
                    "A": "A bulk discount",
                    "B": "Same-day delivery",
                    "C": "Free cleaning services",
                    "D": "Monthly inspections"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "62-64",
        "audio": "E26-T02-62-64.mp3",
        "graphic": "data/graphics/ets26_t02_q62_64.png",
        "transcript": [
            "M: I really need this coffee break. My morning meeting with my client was really challenging.",
            "W: What were you discussing?",
            "M: The project schedule. (62) They asked us to provide the prototype design to them three weeks earlier than originally planned.",
            "W: Well. Then today's cup is my treat. Which one would you like?",
            "M: That's so nice of you! (63) I'll go with the White Cloud Coffee. I like a little milk in mine.",
            "W: Good choice. So, I have some news to share with you. Did you hear about David?",
            "M: No, what's going on?",
            "W: Apparently, (64) he's planning to retire next month."
        ],
        "questions": [
            {
                "id": 62,
                "question": "<strong>PRACTICE 11 (GRAPHIC)</strong><br>What did the man's client request?",
                "choices": {
                    "A": "A large shipment",
                    "B": "A shortened timeline",
                    "C": "A change in design",
                    "D": "A more expensive material"
                },
                "answer": "B"
            },
            {
                "id": 63,
                "question": "Look at the graphic. How much does the man's coffee cost?",
                "choices": {
                    "A": "$2.00",
                    "B": "$3.25",
                    "C": "$3.75",
                    "D": "$4.25"
                },
                "answer": "C"
            },
            {
                "id": 64,
                "question": "What does the woman say about David?",
                "choices": {
                    "A": "He is retiring.",
                    "B": "He is organizing a party.",
                    "C": "He is on vacation.",
                    "D": "He accepted another position."
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "65-67",
        "audio": "E26-T02-65-67.mp3",
        "graphic": "data/graphics/ets26_t02_q65_67.png",
        "transcript": [
            "M: This is Bradley from Windows Galore. How can I help you?",
            "W: Hello! (65) I'd like to have screens added to my windows at home. I was wondering if you would be available to stop by and take a look. (66) I live at 42 West Third Street, by the way.",
            "M: OK—that's not far. Let me see. I could come any morning this week.",
            "W: How about in the afternoon?",
            "M: Hmm. (67) I could reschedule my Tuesday afternoon appointment. I'll check and get back to you—I have your number now. And your name is?",
            "W: Hoffman—Claudia Hoffman. Thank you. Talk to you soon."
        ],
        "questions": [
            {
                "id": 65,
                "question": "<strong>PRACTICE 12 (GRAPHIC)</strong><br>What does the man most likely do?",
                "choices": {
                    "A": "Install windows",
                    "B": "Repair roofs",
                    "C": "Remove trees",
                    "D": "Plant gardens"
                },
                "answer": "A"
            },
            {
                "id": 66,
                "question": "What does the woman provide?",
                "choices": {
                    "A": "A floor layout",
                    "B": "An address",
                    "C": "A form of payment",
                    "D": "Proof of insurance"
                },
                "answer": "B"
            },
            {
                "id": 67,
                "question": "Look at the graphic. Which appointment will the man try to reschedule?",
                "choices": {
                    "A": "The inspector's visit",
                    "B": "The bank loan meeting",
                    "C": "The dental cleaning",
                    "D": "The café project"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "68-70",
        "audio": "E26-T02-68-70.mp3",
        "graphic": "data/graphics/ets26_t02_q68_70.png",
        "transcript": [
            "M: Ms. Kwon, (68) thank you for sending me to the upcoming robotics conference. I didn't expect an opportunity like this so soon after being hired here.",
            "W: (69) It's important for you to be familiar with current robot designs. There are always new trends and technologies coming out, and I want you to stay ahead of developments in our industry.",
            "M: I agree. Plus, it'll give me the chance to introduce myself to potential clients.",
            "W: Oh, about that: here's a handout I provide to all new hires. It includes some helpful tips—especially this one. (70) Do you have your business cards yet?",
            "M: Hmm. I haven't received them, but I'll call the printer today for an update."
        ],
        "questions": [
            {
                "id": 68,
                "question": "<strong>PRACTICE 13 (GRAPHIC)</strong><br>What industry do the speakers most likely work in?",
                "choices": {
                    "A": "Legal",
                    "B": "Construction",
                    "C": "Agriculture",
                    "D": "Robotics"
                },
                "answer": "D"
            },
            {
                "id": 69,
                "question": "Why does the woman want the man to attend a conference?",
                "choices": {
                    "A": "To learn more about the latest industry trends",
                    "B": "To accept a reward on behalf of the company",
                    "C": "To host a panel discussion",
                    "D": "To screen job candidates"
                },
                "answer": "A"
            },
            {
                "id": 70,
                "question": "Look at the graphic. Which tip does the woman point out?",
                "choices": {
                    "A": "Tip 1",
                    "B": "Tip 2",
                    "C": "Tip 3",
                    "D": "Tip 4"
                },
                "answer": "D"
            }
        ]
    }
]

print("Processing and translating ETS 2026 Test 2 Part 3...")

processed_practice_sets = []

for s_idx, r_set in enumerate(raw_sets):
    print(f"Translating set {s_idx + 1}/13 (Questions {r_set['q_num']})...")
    
    # Translate Transcript
    vi_transcript = [translate_text(line) for line in r_set["transcript"]]
    
    # Process Questions
    processed_questions = []
    for q in r_set["questions"]:
        # Clean up the question text (remove PRACTICE and Question headers if any)
        q_clean = q["question"]
        q_clean = re.sub(r"<strong>PRACTICE\s*\d+\s*(?:\(GRAPHIC\))?</strong><br>", "", q_clean, flags=re.IGNORECASE)
        q_clean = re.sub(r"<strong>Question\s*\d+[\.:]</strong>\s*", "", q_clean, flags=re.IGNORECASE)
        q_clean = q_clean.strip()
        
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
            # Fallback
            en_key_line = r_set["transcript"][0]
            vi_key_line = vi_transcript[0]
            
        explanation = generate_explanation(ans_letter, vi_choices[ans_letter], en_key_line, vi_key_line)
        
        processed_questions.append({
            "id": q["id"],
            "slide_index": 3000 + q["id"],
            "question": q["question"],  # Keep the original raw_sets question format (with PRACTICE header if present)
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

# Retain existing entries, and only filter out any previous duplicate 'ets_test_02'
db = [s for s in db if s.get("id") != "ets_test_02"]

# Create and add ets_test_02
new_section = {
    "id": "ets_test_02",
    "title": "ETS 2026 - TEST 02",
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

print("SUCCESS: ETS 2026 Test 2 successfully compiled and written to database!")
