

import streamlit as st
import pandas as pd
import random
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("dc-comics.csv")
    return df.dropna(subset=['name', 'ALIGN', 'SEX', 'EYE', 'HAIR', 'ALIVE']).reset_index(drop=True)

df = load_data()
st.title("🦸 DC Character Story Generator ")


character = st.selectbox("Choose a DC Character:", df['name'])
data = df[df['name'] == character].iloc[0]


def generate_dc_story_prompt(name, align, sex, eye, hair, alive):
    status = 'alive' if 'Living' in alive else 'not alive'
    pronoun = "He" if sex.strip().lower() == "male" else "She"

    intro = (
        f"{name} is a {align.lower()} {sex.lower()} superhero known for their striking {eye.lower()} eyes and {hair.lower()} hair. "
        f"Currently, {name} is {status}. "
    )

    origin = random.choice([
        f"Born into a world of chaos, {name} discovered their purpose after a life-changing tragedy that shaped their destiny. ",
        f"Raised among the extraordinary, {name} always felt the call of duty echo in their soul. ",
        f"{name} wasn't born a hero — it was choice, sacrifice, and pain that forged their path. ",
        f"The journey began in shadows, but {name} rose with determination to stand for something greater. "
    ])

    powers = random.choice([
        f"{pronoun} possesses unmatched agility and strength, with skills that few can rival. ",
        f"Gifted with supernatural abilities, {name} uses them to uphold justice and peace. ",
        f"{pronoun} harnesses intelligence, tactical brilliance, and raw power to confront evil. ",
        f"Armed with unique powers, {name}'s combat style is both graceful and devastating. "
    ])

    mission = random.choice([
        f"One of {name}'s greatest missions was to dismantle a global threat, risking everything to save the innocent. ",
        f"When darkness engulfed the city, {name} stepped forward, fearless and unyielding. ",
        f"{name} once faced a powerful enemy who challenged not just strength, but the hero’s very morals. ",
        f"Even when betrayed by allies, {name} stood strong, proving that true heroes never fall. "
    ])

    legacy = random.choice([
        f"{name}'s story is far from over — each day is a new battle, a new chance to inspire. ",
        f"The legacy of {name} continues to inspire generations across the universe. ",
        f"No matter the odds, {name} rises, reminding the world of the power of hope and resilience. ",
        f"History will remember {name} not just as a warrior, but as a symbol of courage and justice. "
    ])

    return intro + origin + powers + mission + legacy


if st.button("Generate Story"):
    with st.spinner("Crafting your story..."):
        story = generate_dc_story_prompt(
            data['name'],
            data['ALIGN'],
            data['SEX'],
            data['EYE'],
            data['HAIR'],
            data['ALIVE']
        )
        st.subheader("📝 Story")
        st.write(story)

with st.expander("🔎 Character Metadata"):
    st.json(data.to_dict())


st.subheader("📊 Character Alignment Distribution")

align_count = df['ALIGN'].value_counts().reset_index()
align_count.columns = ['ALIGN', 'count']


align_chart = px.pie(
    align_count,
    names='ALIGN',
    values='count',
    title='Distribution of DC Character Alignments',
    color_discrete_sequence=px.colors.sequential.RdBu
)


st.plotly_chart(align_chart, use_container_width=True)
