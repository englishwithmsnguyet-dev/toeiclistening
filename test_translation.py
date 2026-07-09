import urllib.request
import urllib.parse
import json

def translate_text(text, target_lang='vi'):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_lang + "&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            translated = "".join([part[0] for part in result[0] if part[0]])
            return translated
    except Exception as e:
        return f"Error: {str(e)}"

print("Test Translation:", translate_text("What is the topic of the conversation?"))
