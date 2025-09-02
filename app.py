import streamlit as st
import openai

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Profile Tuner", page_icon=":briefcase:")

# --- AUTHENTICATION ---
# This is the secure way to get your API key for a deployed app
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("API Key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()

# --- HELPER FUNCTION (THE AI BRAIN) ---
def tune_profile(summary, job_desc):
    """
    This function takes the user's summary and a job description,
    sends it to the OpenAI API, and returns the AI's response.
    """
    prompt = f"""
    Act as an expert career coach and LinkedIn strategist. A user has provided their current LinkedIn summary and a job description for a role they want to apply for. Your tasks are:

    1.  Analyze the job description to identify the top 5-7 most important skills, qualifications, and keywords.
    2.  Rewrite the user's summary to be approximately 150-200 words. The new summary must skillfully weave in the identified skills and keywords, highlighting the user's strengths in relation to the role. It must be written in a confident, professional, and compelling first-person tone.
    3.  After the summary, generate 3 alternative LinkedIn headlines (each under 220 characters) that are optimized for this specific job.

    Here is the user's current summary:
    "{summary}"

    Here is the job description:
    "{job_desc}"

    Format your response clearly with "### New Summary:" and "### Headline Suggestions:" headings.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- MAIN APP UI ---
st.title("🚀 AI LinkedIn Profile Tuner")
st.write("Paste your summary and a job description to get an AI-powered profile makeover!")

with st.form("profile_form"):
    current_summary = st.text_area("Your Current LinkedIn Summary:", height=150, placeholder="e.g., Experienced project manager...")
    job_description = st.text_area("Job Description You're Applying To:", height=300, placeholder="e.g., The ideal candidate will have...")
    
    submitted = st.form_submit_button("Tune My Profile!")

    if submitted:
        if not current_summary.strip() or not job_description.strip():
            st.warning("Please fill out both text fields.", icon="⚠️")
        else:
            with st.spinner('I am working on your profile, "give me a min"...'):
                tuned_profile = tune_profile(current_summary, job_description)
                st.success("Success! Here is your tuned profile:")
                st.markdown(tuned_profile)