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
        "audio": "E26-T05-32-34.mp3",
        "transcript": [
            "W: Hello, Tariq. (32) Could you do me a favor?",
            "M: Sure—what is it?",
            "W: I'm meeting with the Gerhard Group at ten A.M. for the product pitch, and (32) I need copies of your market analysis report made for each representative.",
            "M: Aren't you at the office right now?",
            "W: Actually, I came in early today, but (33) I couldn't get the copy machine to work.",
            "M: Seriously? (33) We bought it last month!",
            "W: I'm afraid so.",
            "M: (34) I just got off the train. I'll stop at Business Express on McAllister Street and take care of it on my way to the office."
        ],
        "questions": [
            {
                "id": 32,
                "question": "What does the woman ask the man to do for her?",
                "choices": {
                    "A": "Greet a client in the lobby",
                    "B": "Present a product pitch",
                    "C": "Organize some binders",
                    "D": "Make some photocopies"
                },
                "answer": "D"
            },
            {
                "id": 33,
                "question": "What does the man say about some equipment?",
                "choices": {
                    "A": "It is operating smoothly.",
                    "B": "It was purchased recently.",
                    "C": "It needs to be plugged in.",
                    "D": "It has not yet been updated."
                },
                "answer": "B"
            },
            {
                "id": 34,
                "question": "Where is the man?",
                "choices": {
                    "A": "At the office",
                    "B": "At a train station",
                    "C": "At a store",
                    "D": "At a client's headquarters"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "35-37",
        "audio": "E26-T05-35-37.mp3",
        "transcript": [
            "W: Delton Van Lines. How can I help you?",
            "M: Hello. I'm the office manager at Woodsom Insurance Company. (35) We are relocating to a new office in June and would like to book your services.",
            "W: Certainly! But before we reserve a date for the move, (36) we'll need to come to your current location and estimate the cost of moving your furniture and equipment.",
            "M: We have a staff meeting tomorrow morning, so no one's available to show you around then. But tomorrow afternoon works.",
            "W: Perfect! (36) Our representative can be there at two. (37) I'll just need to know where you're located."
        ],
        "questions": [
            {
                "id": 35,
                "question": "Where does the woman most likely work?",
                "choices": {
                    "A": "At a furniture store",
                    "B": "At a moving company",
                    "C": "At a post office",
                    "D": "At an office supply store"
                },
                "answer": "B"
            },
            {
                "id": 36,
                "question": "Why will a representative visit the man's company tomorrow?",
                "choices": {
                    "A": "To provide an estimate",
                    "B": "To sign a contract",
                    "C": "To give a presentation",
                    "D": "To place an order"
                },
                "answer": "A"
            },
            {
                "id": 37,
                "question": "What information will the man most likely provide next?",
                "choices": {
                    "A": "A company's operating hours",
                    "B": "An account number",
                    "C": "A street address",
                    "D": "A telephone number"
                },
                "answer": "A"
            }
        ]
    },
    {
        "q_num": "38-40",
        "audio": "E26-T05-38-40.mp3",
        "transcript": [
            "M: Doctor MacMillan, (38) I'm calling from the human resources department. I'm in charge of your onboarding, and I wanted to confirm your start date. It's the first of April, right?",
            "W: Right. That's when (39) I'll be joining the scientific research team. And as you probably know, I'm still finishing up a research paper with my current institution.",
            "M: Yes, the director did tell me that. (40) Your contract includes time for you to finish up your previous commitments. I can send it to you this afternoon."
        ],
        "questions": [
            {
                "id": 38,
                "question": "What department does the man work in?",
                "choices": {
                    "A": "Legal",
                    "B": "Accounting",
                    "C": "Human resources",
                    "D": "Public relations"
                },
                "answer": "C"
            },
            {
                "id": 39,
                "question": "What kind of work has the woman been hired to do?",
                "choices": {
                    "A": "Scientific research",
                    "B": "Book editing",
                    "C": "Office management",
                    "D": "Legal advising"
                },
                "answer": "A"
            },
            {
                "id": 40,
                "question": "What will the man send the woman this afternoon?",
                "choices": {
                    "A": "A password",
                    "B": "A travel reimbursement",
                    "C": "A security badge",
                    "D": "A contract"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "41-43",
        "audio": "E26-T05-41-43.mp3",
        "transcript": [
            "W1: (41) We've been getting a lot of online orders for our chocolate candies lately. I'm glad to see the increase in orders, but I'm worried about meeting the demands. Are we going to be able to fill and ship all these orders?",
            "M: (42) I think we should hire a few more people to work in the mornings. They could help with packaging and shipping. What do you think, Rebecca?",
            "W2: I agree. (43) I also think that we should ask if our delivery service can pick up our packages twice a day instead of just once a day—maybe every morning and afternoon. I'll call them today."
        ],
        "questions": [
            {
                "id": 41,
                "question": "What recently happened at the business?",
                "choices": {
                    "A": "Its monthly rent increased.",
                    "B": "It received many orders.",
                    "C": "It was featured in a magazine.",
                    "D": "It passed an inspection."
                },
                "answer": "B"
            },
            {
                "id": 42,
                "question": "According to the man, what will help the business?",
                "choices": {
                    "A": "Purchasing updated equipment",
                    "B": "Offering different products",
                    "C": "Extending store hours",
                    "D": "Hiring more employees"
                },
                "answer": "A"
            },
            {
                "id": 43,
                "question": "Who does Rebecca say she will call today?",
                "choices": {
                    "A": "A packaging designer",
                    "B": "An Internet service provider",
                    "C": "A delivery service",
                    "D": "A bank"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "44-46",
        "audio": "E26-T05-44-46.mp3",
        "transcript": [
            "W: I spoke to the Mancini brothers. They just shipped our leather order—the hazelnut color. But it'll take a while to arrive. We don't have enough in stock to complete (44) the ten sofa orders that we've received the past few days.",
            "M: (45) What about the local leather supplier that brought us some samples last week? We could ask them whether they have enough for ten sofas.",
            "W: To be honest, (46) I wasn't very impressed with the quality of their leather. I'd rather wait. I'll reach out to the customers about the delay."
        ],
        "questions": [
            {
                "id": 44,
                "question": "What do the speakers manufacture?",
                "choices": {
                    "A": "Shoes",
                    "B": "Luggage",
                    "C": "Furniture",
                    "D": "Sports equipment"
                },
                "answer": "C"
            },
            {
                "id": 45,
                "question": "Who does the man suggest contacting?",
                "choices": {
                    "A": "A leather supplier",
                    "B": "A delivery driver",
                    "C": "An interior designer",
                    "D": "A machine technician"
                },
                "answer": "A"
            },
            {
                "id": 46,
                "question": "Why is the woman opposed to making a change?",
                "choices": {
                    "A": "She has contracts with clients.",
                    "B": "She is concerned about quality.",
                    "C": "Overhead expenses will increase.",
                    "D": "A license will expire soon."
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "47-49",
        "audio": "E26-T05-47-49.mp3",
        "transcript": [
            "W: Thanks for coming in, Marcos. (47) I just got the results from the consulting firm we hired. They have some ideas about how we can increase sales of our denim blue jeans.",
            "M: I hope so. What does our target audience want?",
            "W: Well, (48) they think it's time we updated our brand with new styles or colors.",
            "M: You know, it takes a lot of effort to develop and launch new styles.",
            "W: Yes. But, if we don't do it, another company will.",
            "M: You're right. (49) I'll ask Junko to come up with some new designs for us to consider."
        ],
        "questions": [
            {
                "id": 47,
                "question": "What are the speakers meeting to discuss?",
                "choices": {
                    "A": "Safety regulations",
                    "B": "Equipment upgrades",
                    "C": "Budget cuts",
                    "D": "Consultant recommendations"
                },
                "answer": "D"
            },
            {
                "id": 48,
                "question": "What does the man mean when he says, \"it takes a lot of effort to develop and launch new styles\"?",
                "choices": {
                    "A": "He is excited about a challenge.",
                    "B": "He is surprised at a competitor's choices.",
                    "C": "He is doubtful about a suggestion.",
                    "D": "He thinks more employees should be hired."
                },
                "answer": "C"
            },
            {
                "id": 49,
                "question": "Who most likely is Junko?",
                "choices": {
                    "A": "A focus group leader",
                    "B": "A clothing designer",
                    "C": "A sales associate",
                    "D": "An accountant"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "50-52",
        "audio": "E26-T05-50-52.mp3",
        "transcript": [
            "M: Hi, Gabriela. Thanks for agreeing to give me the highlights of the budget discussion from the monthly meeting. (50) I'm back from vacation and still catching up.",
            "W: Sure. Here's a copy of the report. Everyone on our organization's board at Tennis United agreed to the fee increase for (51) the tennis camp for young players.",
            "M: Good. And why do we have T-shirts listed as an expense item?",
            "W: Although the next tournament's in the fall, (52) the T-shirts were ordered very early. That way we received half off the price, since the supplier wanted to get rid of his summer inventory."
        ],
        "questions": [
            {
                "id": 50,
                "question": "Why did the man miss a meeting?",
                "choices": {
                    "A": "He was stuck in traffic.",
                    "B": "He had a medical appointment.",
                    "C": "He was speaking with a client.",
                    "D": "He was away on vacation."
                },
                "answer": "D"
            },
            {
                "id": 51,
                "question": "Which sport does the speakers' organization promote?",
                "choices": {
                    "A": "Tennis",
                    "B": "Volleyball",
                    "C": "Swimming",
                    "D": "Gymnastics"
                },
                "answer": "A"
            },
            {
                "id": 52,
                "question": "Why were T-shirts ordered early?",
                "choices": {
                    "A": "To avoid potential delays",
                    "B": "To get free delivery",
                    "C": "To receive a discount",
                    "D": "To meet heavy demand"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "53-55",
        "audio": "E26-T05-53-55.mp3",
        "transcript": [
            "W: The first item on today's meeting agenda is (53) our bid to renovate the Morrisville Bridge. Do we have an update on that yet?",
            "M1: Yes—unfortunately we didn't get the contract.",
            "M2: Yes, the only explanation given was that (54) another construction company submitted a proposal with a shorter timeline.",
            "W: So, what do we know about this competitor? Have they worked on other local projects?",
            "M1: The only thing I heard was their name—CDQ Construction Company.",
            "W: Well, I'd like to know more about them. (55) Can you two do some research before our next meeting?"
        ],
        "questions": [
            {
                "id": 53,
                "question": "What industry do the speakers most likely work in?",
                "choices": {
                    "A": "Energy",
                    "B": "Finance",
                    "C": "Construction",
                    "D": "Manufacturing"
                },
                "answer": "C"
            },
            {
                "id": 54,
                "question": "What is the reason a company did not get a contract?",
                "choices": {
                    "A": "Some costs were too high.",
                    "B": "A facility failed an inspection.",
                    "C": "Some paperwork was submitted late.",
                    "D": "A competitor can complete a project faster."
                },
                "answer": "D"
            },
            {
                "id": 55,
                "question": "What does the woman ask the men to do?",
                "choices": {
                    "A": "Visit a facility",
                    "B": "Conduct some research",
                    "C": "Rewrite a proposal",
                    "D": "Contact some vendors"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "56-58",
        "audio": "E26-T05-56-58.mp3",
        "transcript": [
            "W: (56) Did you see that the results of last month's employee survey have been compiled? All the staff feedback is available.",
            "M: Yes, and I just finished reviewing the comments.",
            "W: You know, I noticed one recurring complaint. The size of the break room is too small. (57) Perhaps we could enlarge the break room by having the wall taken down between it and the meeting room next door.",
            "M: Well, we do have money available in the budget.",
            "W: Then could you reach out to your contact at the construction company?",
            "M: (58) I can't do it this afternoon, since I need to see a dentist, but I will definitely make the call."
        ],
        "questions": [
            {
                "id": 56,
                "question": "What did the company do last month?",
                "choices": {
                    "A": "It opened a second location.",
                    "B": "It merged with another business.",
                    "C": "It launched a new product.",
                    "D": "It conducted an employee survey."
                },
                "answer": "D"
            },
            {
                "id": 57,
                "question": "Why does the man say, \"we do have money available in the budget\"?",
                "choices": {
                    "A": "To request another budget analysis",
                    "B": "To suggest hiring additional employees",
                    "C": "To agree with a proposed renovation",
                    "D": "To recommend an increase in advertising"
                },
                "answer": "C"
            },
            {
                "id": 58,
                "question": "What does the man say he has to do this afternoon?",
                "choices": {
                    "A": "Have his car repaired",
                    "B": "Give a presentation",
                    "C": "Go to a dentist appointment",
                    "D": "Attend a reception"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "59-61",
        "audio": "E26-T05-59-61.mp3",
        "transcript": [
            "W: (59) Thanks for calling Hang's Metal Recycling Company. How can I help you?",
            "M: Hi. I'm with Shannak Construction Company. We've got a lot of brass metal scrap from a recent remodeling job. Are you currently buying metal scrap?",
            "W: Yes, we are. We currently pay two dollars a pound.",
            "M: Oh, (60) there's another recycling center that pays two dollars and twenty-five cents a pound. Would you be willing to match their price?",
            "W: Yes, we have a price-match guarantee.",
            "M: Great. (61) I'll bring the metal to you this afternoon, then."
        ],
        "questions": [
            {
                "id": 59,
                "question": "Where does the woman work?",
                "choices": {
                    "A": "At a recycling company",
                    "B": "At an appliance store",
                    "C": "At a manufacturing company",
                    "D": "At an architectural firm"
                },
                "answer": "A"
            },
            {
                "id": 60,
                "question": "What does the man ask the woman to do?",
                "choices": {
                    "A": "Revise a contract",
                    "B": "Match a competitor's offer",
                    "C": "Refund a delivery fee",
                    "D": "Sign in at a security desk"
                },
                "answer": "B"
            },
            {
                "id": 61,
                "question": "What does the man say he will do this afternoon?",
                "choices": {
                    "A": "Conduct an inspection",
                    "B": "Sign a document",
                    "C": "Deliver some materials",
                    "D": "Update a Web site"
                },
                "answer": "C"
            }
        ]
    },
    {
        "q_num": "62-64",
        "audio": "E26-T05-62-64.mp3",
        "graphic": "data/graphics/ets26_t05_q62_64.png",
        "transcript": [
            "W: Hi. I just got off the phone with management. They're not happy. The construction of the train tunnel isn't progressing fast enough.",
            "M: Yeah, I'm not surprised. (62) The drilling is done now. The thing is, we can't start installing the support columns until we have all the materials for the concrete.",
            "W: When are the materials going to get here?",
            "M: A week, maybe two.",
            "W: (63) Let's see if the shipment can be expedited. Can you do that?",
            "M: Sure. I'll call the supplier to ask about getting it here sooner.",
            "W: In the meantime, (64) I'm going to write an e-mail to management to explain how we're attempting to resolve the situation."
        ],
        "questions": [
            {
                "id": 62,
                "question": "Look at the graphic. Which project phase was just completed?",
                "choices": {
                    "A": "Phase 1",
                    "B": "Phase 2",
                    "C": "Phase 3",
                    "D": "Phase 4"
                },
                "answer": "B"
            },
            {
                "id": 63,
                "question": "What does the woman ask the man to do?",
                "choices": {
                    "A": "Request an earlier delivery date",
                    "B": "Consult with a safety inspector",
                    "C": "Post some construction plans",
                    "D": "Forward an invoice"
                },
                "answer": "A"
            },
            {
                "id": 64,
                "question": "What does the woman intend to do next?",
                "choices": {
                    "A": "Review some data",
                    "B": "Move a vehicle",
                    "C": "Increase the size of a crew",
                    "D": "Contact the management team"
                },
                "answer": "D"
            }
        ]
    },
    {
        "q_num": "65-67",
        "audio": "E26-T05-65-67.mp3",
        "graphic": "data/graphics/ets26_t05_q65_67.png",
        "transcript": [
            "M: The city just posted its new parking rates, and we need to talk about how they'll affect (65) our restaurant's food delivery service. I'm worried we'll lose money because we'll need to pay more for parking while the delivery driver takes the food to customers.",
            "W: Wow. (66) Parking in our main delivery area is up to fifteen dollars an hour? That is a problem. But offering free delivery attracts a lot of business. (67) What else can we do to lower expenses?",
            "M: (67) We could start using bicycle delivery whenever possible. That should help.",
            "W: Good idea. I'll talk to our drivers to see who's willing to switch to bicycle deliveries for customers nearby. Some people really like the exercise."
        ],
        "questions": [
            {
                "id": 65,
                "question": "What type of business do the speakers work for?",
                "choices": {
                    "A": "A restaurant",
                    "B": "A law firm",
                    "C": "An office-supply store",
                    "D": "A flower shop"
                },
                "answer": "A"
            },
            {
                "id": 66,
                "question": "Look at the graphic. In which area of the city does the business make most of its deliveries?",
                "choices": {
                    "A": "The waterfront district",
                    "B": "The historic district",
                    "C": "The residential district",
                    "D": "The downtown district"
                },
                "answer": "D"
            },
            {
                "id": 67,
                "question": "How does the man propose lowering business expenses?",
                "choices": {
                    "A": "By reducing packaging waste",
                    "B": "By introducing bicycle delivery",
                    "C": "By switching to a new supplier",
                    "D": "By moving to a smaller building"
                },
                "answer": "B"
            }
        ]
    },
    {
        "q_num": "68-70",
        "audio": "E26-T05-68-70.mp3",
        "graphic": "data/graphics/ets26_t05_q68_70.png",
        "transcript": [
            "M: When customers walk into Southern Regional Bank, I want them to feel confident about entrusting their money to us. As I mentioned the last time we met, I'm hoping (68) your interior design firm can give our lobby a more polished, professional look.",
            "W: Our proposal does just that. Here—take a look. The cover page includes a summary of the renovations.",
            "M: Hmm. (69) Do you really think we need skylights? That would be a big expense.",
            "W: There aren't many windows in your lobby, so it's the best way to bring more natural light into the room. Besides, our proposed renovations would actually come in under budget. (70) If you turn to page four, you'll see the cost breakdown."
        ],
        "questions": [
            {
                "id": 68,
                "question": "Who most likely is the woman?",
                "choices": {
                    "A": "A hotel manager",
                    "B": "An interior designer",
                    "C": "A construction worker",
                    "D": "A real estate agent"
                },
                "answer": "B"
            },
            {
                "id": 69,
                "question": "Look at the graphic. Which step does the man ask about?",
                "choices": {
                    "A": "Step 1",
                    "B": "Step 2",
                    "C": "Step 3",
                    "D": "Step 4"
                },
                "answer": "A"
            },
            {
                "id": 70,
                "question": "What will the man most likely do next?",
                "choices": {
                    "A": "Send a contract",
                    "B": "Go to the lobby",
                    "C": "Look at some photographs",
                    "D": "Review a cost estimate"
                },
                "answer": "B"
            }
        ]
    }
]

print("Processing and translating ETS 2026 Test 5 Part 3...")

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
            "slide_index": 4000 + q["id"],  # Test 5 slide indices starting at 4000 + ID
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

# Retain existing entries, and only filter out any previous duplicate 'ets_test_05'
db = [s for s in db if s.get("id") != "ets_test_05"]

# Create and add ets_test_05
new_section = {
    "id": "ets_test_05",
    "title": "ETS 2026 - TEST 05",
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

print("SUCCESS: ETS 2026 Test 5 successfully compiled and written to database!")
