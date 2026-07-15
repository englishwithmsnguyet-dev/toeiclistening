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

    # Uses high-contrast royal blue #3b82f6 for explanation box
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
        "audio": "E26-T03-32-34.mp3",
        "transcript": [
            "M: Hi, Chef Ayaka. I was looking over this week's sales, and (32) I noticed that a lot of people ordered the beef stew special.",
            "W: Yeah. It's been very popular with patrons. In fact, I want to add it to the regular menu.",
            "M: Good idea. (33) Beef prices change frequently, though, so we might need to consider that when we set the price for the dish if we're going to offer it daily.",
            "W: OK. (34) I'll call our supplier too. We need to make sure they can get us enough beef each week."
        ],
        "questions": [
            {
                "id": 32,
                "question": "Where do the speakers most likely work?",
                "choices": {
                    "A": "At a shipping company",
                    "B": "At a restaurant",
                    "C": "At a gift shop",
                    "D": "At a farm"
                },
                "answer": "B"
            },
            {
                "id": 33,
                "question": "What does the man suggest considering?",
                "choices": {
                    "A": "An advertising strategy",
                    "B": "An online menu",
                    "C": "The price of an item",
                    "D": "The results of a survey"
                },
                "answer": "C"
            },
            {
                "id": 34,
                "question": "What does the woman say she will do?",
                "choices": {
                    "A": "Pay a deposit",
                    "B": "Contact a supplier",
                    "C": "Reschedule a delivery",
                    "D": "Arrange some merchandise"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "35-37",
        "audio": "E26-T03-35-37.mp3",
        "transcript": [
            "M1: Excuse me, (35) does train 1401 stop at the Lexington Street station?",
            "W: Yes. It's a twenty-minute ride.",
            "M2: Oh good, that gives us plenty of time to get to the party.",
            "W: The train leaves from platform twelve in three minutes.",
            "M2: Let's head over there now, Sergey. (36) I'm really looking forward to our company gala event tonight.",
            "M1: Me too. (37) Hey did you happen to bring an umbrella? I forgot mine. It might rain on our walk from the station.",
            "M2: I did! We can share it."
        ],
        "questions": [
            {
                "id": 35,
                "question": "Where is the conversation most likely taking place?",
                "choices": {
                    "A": "At a fitness center",
                    "B": "At a hotel",
                    "C": "At a train station",
                    "D": "At a corporate office"
                },
                "answer": "C"
            },
            {
                "id": 36,
                "question": "What type of event will the men attend this evening?",
                "choices": {
                    "A": "A company gala",
                    "B": "An opera",
                    "C": "A sports match",
                    "D": "A lecture"
                },
                "answer": "A"
            },
            {
                "id": 37,
                "question": "What did Sergey forget to bring?",
                "choices": {
                    "A": "Gloves",
                    "B": "Sunglasses",
                    "C": "A hat",
                    "D": "An umbrella"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "38-40",
        "audio": "E26-T03-38-40.mp3",
        "transcript": [
            "W: (38) I talked to Mr. Hoffman this morning, and he said he's decided to start a delivery service for our customers who have a difficult time picking up their prescriptions.",
            "M: That's a good idea. (39) I know a lot of people find it inconvenient to come in person to get their medications. But many of our customers buy other things while they're here.",
            "W: Oh, they'll be able to make other purchases too, to be delivered with their medicine. In fact, (40) I'm supposed to draft a job posting for delivery drivers. Could you help me do that?"
        ],
        "questions": [
            {
                "id": 38,
                "question": "What has Mr. Hoffman decided to do?",
                "choices": {
                    "A": "Extend store hours",
                    "B": "Start a delivery service",
                    "C": "Offer a rewards program",
                    "D": "Stop selling certain products"
                },
                "answer": "B"
            },
            {
                "id": 39,
                "question": "What business do the speakers most likely work for?",
                "choices": {
                    "A": "A bakery",
                    "B": "A flower shop",
                    "C": "A grocery store",
                    "D": "A pharmacy"
                },
                "answer": "D"
            },
            {
                "id": 40,
                "question": "What does the woman ask the man to help her do?",
                "choices": {
                    "A": "Mail some packages",
                    "B": "Take inventory",
                    "C": "Create a job posting",
                    "D": "Help some customers"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "41-43",
        "audio": "E26-T03-41-43.mp3",
        "transcript": [
            "W: Marcel, I don't know if you reviewed the latest report. (41) Unfortunately, our sales are continuing to drop.",
            "M: Yes, competition is at an all-time high. More and more companies are selling clothing and gear for outdoor recreation.",
            "W: We need better ways to make our brand stand out.",
            "M: Well, (42) we could probably benefit from having more direct input from athletes who use our gear. I was thinking maybe we could hire a professional rock climber to consult with our designers.",
            "W: That's an interesting idea. Is there anyone you have in mind?",
            "M: (43) I'll e-mail you a list this afternoon."
        ],
        "questions": [
            {
                "id": 41,
                "question": "What problem does the woman mention?",
                "choices": {
                    "A": "A product is faulty.",
                    "B": "A company's sales are decreasing.",
                    "C": "Some materials are damaged.",
                    "D": "A sales department is understaffed."
                },
                "answer": "B"
            },
            {
                "id": 42,
                "question": "Where do the speakers most likely work?",
                "choices": {
                    "A": "At a publishing firm",
                    "B": "At a sporting goods company",
                    "C": "At a travel agency",
                    "D": "At a state park"
                },
                "answer": "B"
            },
            {
                "id": 43,
                "question": "What does the man say he will do this afternoon?",
                "choices": {
                    "A": "Sign a document",
                    "B": "Ship an order",
                    "C": "Review customer feedback",
                    "D": "Send a list"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "44-46",
        "audio": "E26-T03-44-46.mp3",
        "transcript": [
            "W: Hello. (44) I was featured in an article in your newspaper about five years ago. And now when I click on the link, nothing happens.",
            "M: Oh, the public links expire after three years, but (45) I can search for your article in our database. I just need keywords from the article to use in the search.",
            "W: It was about my internship at a dental office.",
            "M: OK. Let me check our archives.",
            "W: Thanks. I was still in college when the article came out, but (46) now I'm starting my own practice. And I'd like to hang the article on the wall.",
            "M: Oh! Congratulations."
        ],
        "questions": [
            {
                "id": 44,
                "question": "Why is the woman calling?",
                "choices": {
                    "A": "To verify some facts",
                    "B": "To confirm a deadline",
                    "C": "To inquire about an article",
                    "D": "To apply for a position"
                },
                "answer": "C"
            },
            {
                "id": 45,
                "question": "What does the man offer to do?",
                "choices": {
                    "A": "Search a database",
                    "B": "Renew a subscription",
                    "C": "Consult with colleagues",
                    "D": "Send an updated schedule"
                },
                "answer": "A"
            },
            {
                "id": 46,
                "question": "Why does the man congratulate the woman?",
                "choices": {
                    "A": "She appeared on television.",
                    "B": "She was nominated for an award.",
                    "C": "She is publishing a book.",
                    "D": "She is starting her own business."
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "47-49",
        "audio": "E26-T03-47-49.mp3",
        "transcript": [
            "W: Welcome to Scott's Supplies! Just so you know, (47) all our power tools and ladders are twenty percent off today. Is there something I can help you with?",
            "M: Yes. I came in last week to get some lumber for a home project I was working on, but (48) the boards I purchased are the wrong width. I was wondering if I could get a refund.",
            "W: Sure. Do you have the receipt?",
            "M: No, unfortunately. I must've lost it.",
            "W: Hmm, OK. (49) Let me find the manager."
        ],
        "questions": [
            {
                "id": 47,
                "question": "Where does the conversation most likely take place?",
                "choices": {
                    "A": "At a furniture store",
                    "B": "At an electronics store",
                    "C": "At a sporting goods store",
                    "D": "At a building supply store"
                },
                "answer": "D"
            },
            {
                "id": 48,
                "question": "Why does the man want a refund?",
                "choices": {
                    "A": "He found a less expensive option.",
                    "B": "He bought the wrong size.",
                    "C": "He does not like the color of an item.",
                    "D": "He noticed an item is damaged."
                },
                "answer": "B"
            },
            {
                "id": 49,
                "question": "What does the woman imply when she says, \"Let me find the manager\"?",
                "choices": {
                    "A": "She needs to attend to other customers.",
                    "B": "She does not have the authority to complete a request.",
                    "C": "A transaction was not processed correctly.",
                    "D": "A quality complaint needs to be documented."
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "50-52",
        "audio": "E26-T03-50-52.mp3",
        "transcript": [
            "W: Welcome back! (50) How were your lunch deliveries?",
            "M: All right, except one bag broke and the food container fell out right as I was walking up to a customer's door. The container was still sealed, and the customer accepted it, so it turned out OK in the end.",
            "W: Well, I'm glad everything worked out. By the way, take a look at my screen! (51) I got the new delivery software installed and running while you were gone.",
            "M: This looks great! I like how different areas can be grouped together so drivers can deliver more efficiently.",
            "W: Me too. (52) And since we've recently had such a significant increase in customers, this will be really useful."
        ],
        "questions": [
            {
                "id": 50,
                "question": "What most likely is the man's job?",
                "choices": {
                    "A": "Plumber",
                    "B": "Auto mechanic",
                    "C": "Food delivery person",
                    "D": "Computer technician"
                },
                "answer": "C"
            },
            {
                "id": 51,
                "question": "What did the woman do while the man was gone?",
                "choices": {
                    "A": "She created an advertisement.",
                    "B": "She finalized a contract.",
                    "C": "She addressed a customer complaint.",
                    "D": "She had new software installed."
                },
                "answer": "D"
            },
            {
                "id": 52,
                "question": "What does the woman say has recently changed?",
                "choices": {
                    "A": "Costs have been reduced.",
                    "B": "A competitor has opened a location nearby.",
                    "C": "The number of customers has increased.",
                    "D": "Safety regulations have been introduced."
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "53-55",
        "audio": "E26-T03-53-55.mp3",
        "transcript": [
            "M: Hi, Jin-Ah. I've got good news. (53) We signed a contract to create an ad campaign for a new client.",
            "W: That's great! Who is it?",
            "M: (54) It's HMD Incorporated, an organic snack company. They just developed a new line of snacks made entirely from vegetables. They want to market the snacks to sports teams as well as individuals.",
            "W: Well, that sounds exciting but hard to understand. I guess we'll need to learn more about the products first.",
            "M: Exactly. We'll have the client come in to give us nutritional information, and provide us with some samples. (55) I'll schedule a meeting with them soon."
        ],
        "questions": [
            {
                "id": 53,
                "question": "What type of company do the speakers work for?",
                "choices": {
                    "A": "An investment firm",
                    "B": "An advertising agency",
                    "C": "A staffing service",
                    "D": "A construction company"
                },
                "answer": "B"
            },
            {
                "id": 54,
                "question": "What has HMD Incorporated recently done?",
                "choices": {
                    "A": "It has built a new headquarters.",
                    "B": "It has donated to a charity.",
                    "C": "It has developed a new line of products.",
                    "D": "It has won an industry award."
                },
                "answer": "C"
            },
            {
                "id": 55,
                "question": "What does the man say he will do?",
                "choices": {
                    "A": "Update his team's goals",
                    "B": "Conduct some research",
                    "C": "Apply for a permit",
                    "D": "Arrange for a meeting"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "56-58",
        "audio": "E26-T03-56-58.mp3",
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
                "answer": "D"
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
                "answer": "A"
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
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "59-61",
        "audio": "E26-T03-59-61.mp3",
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
                "answer": "B"
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
                "answer": "C"
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
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "62-64",
        "audio": "E26-T03-62-64.mp3",
        "graphic": "data/graphics/ets26_t03_q62_64.png",
        "transcript": [
            "W: Marco, you'll be restocking the cleaning products this morning, right? While you're doing that, (62) could you also put the updated sale-price labels on the hand soap dispensers? They're on the shelf right above the laundry detergent.",
            "M: No problem—that shouldn't take long. What else can I help with?",
            "W: (63) Can you make room for our new international foods section at the front of the store?",
            "M: (64) Oh, did the shipment finally arrive? That snowstorm up north really affected delivery schedules."
        ],
        "questions": [
            {
                "id": 62,
                "question": "Look at the graphic. Which dollar amount will the man change?",
                "choices": {
                    "A": "$2.37",
                    "B": "$4.55",
                    "C": "$7.86",
                    "D": "$2.91"
                },
                "answer": "A"
            },
            {
                "id": 63,
                "question": "What will be added at the front of the store?",
                "choices": {
                    "A": "An additional checkout stand",
                    "B": "A holiday display",
                    "C": "A special food section",
                    "D": "A seating area"
                },
                "answer": "C"
            },
            {
                "id": 64,
                "question": "According to the man, why did a shipment arrive late?",
                "choices": {
                    "A": "He forgot to place an order.",
                    "B": "It was delivered to the wrong address.",
                    "C": "Some supplies were unavailable.",
                    "D": "Weather conditions were poor."
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "65-67",
        "audio": "E26-T03-65-67.mp3",
        "graphic": "data/graphics/ets26_t03_q65_67.png",
        "transcript": [
            "W: Thanks for calling Kwon Photography Studio.",
            "M: (65) Hello. I need to have a photo taken for a Canadian passport.",
            "W: OK. You can make an appointment Monday through Friday. (66) Just bring in a copy of the application so we can see the size requirements.",
            "M: I work nine to five every day at my current job. Do you have any openings after five P.M.?",
            "W: (67) No problem. We're open until six P.M. one day a week."
        ],
        "questions": [
            {
                "id": 65,
                "question": "What does the man say he needs to have done?",
                "choices": {
                    "A": "He needs to schedule a job interview.",
                    "B": "He needs to cancel a doctor's appointment.",
                    "C": "He needs to have his photograph taken.",
                    "D": "He needs to renew his driver's license."
                },
                "answer": "C"
            },
            {
                "id": 66,
                "question": "What does the woman ask the man to bring to an appointment?",
                "choices": {
                    "A": "An application form",
                    "B": "Some references",
                    "C": "A study guide",
                    "D": "A payment receipt"
                },
                "answer": "A"
            },
            {
                "id": 67,
                "question": "Look at the graphic. Which day will the man request an appointment for?",
                "choices": {
                    "A": "Monday",
                    "B": "Tuesday",
                    "C": "Wednesday",
                    "D": "Thursday"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "68-70",
        "audio": "E26-T03-68-70.mp3",
        "graphic": "data/graphics/ets26_t03_q68_70.png",
        "transcript": [
            "M: Hi, Marina. (68) Do you have receipts for your expenses from the dental hygienists' conference you attended last week?",
            "W: Yes, I have them. I was just going to scan them and send them to you by e-mail.",
            "M: Thanks very much. (69) Once I receive them, I'll process your request for reimbursement. Don't forget to fill out the travel expenses form and include it in your e-mail, too.",
            "W: (70) OK. Remind me, what should I use for the department code?",
            "M: Oh, sorry. I forgot to tell you. Use number 1009."
        ],
        "questions": [
            {
                "id": 68,
                "question": "What event did the woman attend last week?",
                "choices": {
                    "A": "A professional conference",
                    "B": "A training workshop",
                    "C": "A car auction",
                    "D": "A product demonstration"
                },
                "answer": "A"
            },
            {
                "id": 69,
                "question": "What will the man do with the documents the woman provides?",
                "choices": {
                    "A": "Process a request",
                    "B": "Postpone a reservation",
                    "C": "Make a schedule",
                    "D": "Finalize a report"
                },
                "answer": "A"
            },
            {
                "id": 70,
                "question": "Look at the graphic. Which section does the woman ask about?",
                "choices": {
                    "A": "Section 2",
                    "B": "Section 3",
                    "C": "Section 4",
                    "D": "Section 5"
                },
                "answer": "C"
            }
        ]
    }
]

print("Processing and translating ETS 2026 Test 3 Part 3...")

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

# Retain existing entries, and only filter out any previous duplicate 'ets_test_03'
db = [s for s in db if s.get("id") != "ets_test_03"]

# Create and add ets_test_03
new_section = {
    "id": "ets_test_03",
    "title": "ETS 2026 - TEST 03",
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

print("SUCCESS: ETS 2026 Test 3 successfully compiled and written to database!")
