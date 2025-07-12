import pandas as pd
import json
import time
import openai

# ✅ STEP 1: Set your API key (no OpenAI() object needed!)
openai.api_key = "abcde"  # 🔐 Replace with your actual key

# ✅ STEP 2: Load and clean dataset
df = pd.read_csv("dc-comics.csv").dropna(subset=['name', 'ALIGN', 'SEX', 'EYE', 'HAIR', 'ALIVE'])

samples = []

# ✅ STEP 3: Generate prompts and fetch stories
for index, r in df.iterrows():
    name = r['name'].strip()
    prompt = (f"Write a 500-word story about {name}, a {r['ALIGN'].lower()} {r['SEX'].lower()} superhero "
              f"with {r['EYE'].lower()} eyes and {r['HAIR'].lower()} hair, currently "
              f"{'alive' if 'Living' in r['ALIVE'] else 'not alive'}. Focus only on {name}, "
              "showcasing their origin, powers, and a major mission.")

    print(f"[{index+1}/{len(df)}] Generating story for: {name}")

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.9
        )
        story = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error for {name}: {e}")
        story = f"{name} stands as a legend in the DC universe..."

    samples.append({
        "name": name,
        "prompt": prompt,
        "story": story
    })

    time.sleep(2)  # 🕒 To respect OpenAI's rate limit

# ✅ STEP 4: Save as JSONL
with open("dc_train.jsonl", "w", encoding="utf-8") as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

print("✅ All stories generated and saved to dc_train.jsonl")
