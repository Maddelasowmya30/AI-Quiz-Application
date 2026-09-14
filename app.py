
import streamlit as st

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Quiz Application",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------------
# Application Title
# -----------------------------------

st.title("🧠 AI Quiz Application")
st.write("Test your Python knowledge and improve your learning!")

st.info(
    "This application uses Python logic to calculate your score "
    "and generate personalized learning feedback."
)

# -----------------------------------
# Quiz Questions
# -----------------------------------

questions = [
    {
        "question": "Which language is used to create this application?",
        "options": ["Java", "Python", "C++", "HTML"],
        "answer": "Python",
        "topic": "Python Basics",
        "explanation": "Python is used to build this application with Streamlit."
    },
    {
        "question": "Which data type stores multiple values in an ordered collection?",
        "options": ["List", "Integer", "Boolean", "Float"],
        "answer": "List",
        "topic": "Lists",
        "explanation": "A list stores multiple values in an ordered and changeable collection."
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "define", "def", "fun"],
        "answer": "def",
        "topic": "Functions",
        "explanation": "The def keyword is used to define a function in Python."
    },
    {
        "question": "Which loop is commonly used to iterate through a list?",
        "options": ["repeat", "for", "iterate", "loop"],
        "answer": "for",
        "topic": "Loops",
        "explanation": "A for loop can visit each item in a list."
    },
    {
        "question": "Which symbol is used to write a single-line comment in Python?",
        "options": ["//", "/*", "#", "<!--"],
        "answer": "#",
        "topic": "Python Basics",
        "explanation": "The # symbol starts a single-line comment in Python."
    },
    {
        "question": "Which collection stores data as key-value pairs?",
        "options": ["Tuple", "List", "Dictionary", "Set"],
        "answer": "Dictionary",
        "topic": "Dictionaries",
        "explanation": "A dictionary stores values using unique keys."
    },
    {
        "question": "Which statement is used to make a decision in Python?",
        "options": ["if", "select", "choose", "check"],
        "answer": "if",
        "topic": "Conditions",
        "explanation": "The if statement executes code when a condition is true."
    },
    {
        "question": "Which function displays output in Python?",
        "options": ["show()", "display()", "print()", "output()"],
        "answer": "print()",
        "topic": "Python Basics",
        "explanation": "The print() function displays information on the screen."
    }
]

# -----------------------------------
# Session State Initialization
# -----------------------------------

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

# -----------------------------------
# Reset Quiz Function
# -----------------------------------

def reset_quiz():
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_finished = False

# -----------------------------------
# AI-Style Feedback Function
# -----------------------------------

def generate_feedback(score, total, topic_scores):
    percentage = (score / total) * 100

    if percentage == 100:
        level = "Excellent"
        message = (
            "Outstanding performance! You have answered every "
            "question correctly."
        )
        advice = "You are ready to explore advanced Python concepts."

    elif percentage >= 75:
        level = "Very Good"
        message = (
            "Great work! You have a strong understanding "
            "of the basic concepts."
        )
        advice = "Practice more coding problems to improve further."

    elif percentage >= 50:
        level = "Good Progress"
        message = (
            "You are making progress. Review the topics "
            "where you made mistakes."
        )
        advice = "Revise the basics and practice small programs daily."

    else:
        level = "Keep Learning"
        message = (
            "Do not worry! Every mistake is an opportunity "
            "to learn something new."
        )
        advice = "Start with Python basics, then practice simple exercises."

    weak_topics = []

    for topic, result in topic_scores.items():
        if result["wrong"] > 0:
            weak_topics.append(topic)

    return level, message, advice, weak_topics

# -----------------------------------
# Quiz Result Function
# -----------------------------------

def calculate_results():
    score = 0
    topic_scores = {}

    for index, question in enumerate(questions):
        topic = question["topic"]
        selected_answer = st.session_state.user_answers.get(index)

        if topic not in topic_scores:
            topic_scores[topic] = {
                "correct": 0,
                "wrong": 0
            }

        if selected_answer == question["answer"]:
            score += 1
            topic_scores[topic]["correct"] += 1
        else:
            topic_scores[topic]["wrong"] += 1

    return score, topic_scores

# -----------------------------------
# Display Quiz
# -----------------------------------

if not st.session_state.quiz_finished:

    total_questions = len(questions)
    question_number = st.session_state.current_question

    progress = question_number / total_questions

    st.progress(progress)

    st.write(
        f"Question {question_number + 1} "
        f"of {total_questions}"
    )

    current = questions[question_number]

    st.subheader(current["question"])

    selected_option = st.radio(
        "Choose your answer:",
        current["options"],
        index=None,
        key=f"question_{question_number}"
    )

    st.caption(f"Topic: {current['topic']}")

    if question_number < total_questions - 1:

        if st.button("Next Question ➡️", type="primary"):

            if selected_option is None:
                st.warning("Please select an answer first.")

            else:
                st.session_state.user_answers[question_number] = selected_option
                st.session_state.current_question += 1
                st.rerun()

    else:

        if st.button("Submit Quiz 🎯", type="primary"):

            if selected_option is None:
                st.warning("Please select an answer first.")

            else:
                st.session_state.user_answers[question_number] = selected_option
                st.session_state.quiz_finished = True
                st.rerun()

# -----------------------------------
# Display Final Results
# -----------------------------------

else:

    score, topic_scores = calculate_results()

    total = len(questions)
    percentage = (score / total) * 100

    st.balloons()

    st.header("🎉 Quiz Completed!")

    st.metric(
        label="Your Final Score",
        value=f"{score} / {total}"
    )

    st.write(f"### Percentage: {percentage:.1f}%")

    if percentage >= 75:
        st.success("You performed very well!")
    elif percentage >= 50:
        st.info("Good effort! Keep practicing.")
    else:
        st.warning("Keep learning and try again!")

    # AI-style personalized feedback

    level, message, advice, weak_topics = generate_feedback(
        score, total, topic_scores
    )

    st.subheader("🤖 Personalized Learning Feedback")

    st.write(f"**Performance Level:** {level}")
    st.write(message)
    st.write(f"**Learning Advice:** {advice}")

    if weak_topics:
        st.write("### 📚 Topics to Revise")

        for topic in weak_topics:
            st.write(f"- {topic}")

    else:
        st.success("You answered all topics correctly!")

    # Topic-wise analysis

    st.subheader("📊 Topic-wise Performance")

    for topic, result in topic_scores.items():

        total_topic_questions = (
            result["correct"] + result["wrong"]
        )

        topic_percentage = (
            result["correct"] / total_topic_questions
        ) * 100

        st.write(f"**{topic}**")

        st.progress(topic_percentage / 100)

        st.write(
            f"Correct: {result['correct']} | "
            f"Wrong: {result['wrong']} | "
            f"Accuracy: {topic_percentage:.1f}%"
        )

    # Review answers

    st.subheader("📝 Review Your Answers")

    for index, question in enumerate(questions):

        selected = st.session_state.user_answers.get(index)
        correct = question["answer"]

        st.write(f"**{index + 1}. {question['question']}**")
        st.write(f"Your answer: {selected}")
        st.write(f"Correct answer: {correct}")

        if selected == correct:
            st.success("Correct answer ✅")
        else:
            st.error("Incorrect answer ❌")

        st.caption(question["explanation"])

        st.divider()

    if st.button("🔄 Restart Quiz", type="primary"):
        reset_quiz()
        st.rerun()