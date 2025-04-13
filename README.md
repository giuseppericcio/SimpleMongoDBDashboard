# 🩺 MedicalAssistantGPT

Welcome to **MedicalAssistantGPT**, a simple yet powerful Streamlit dashboard that leverages **MongoDB**, **Streamlit**, and **OpenAI** to help users explore medical symptom-disorder relationships. This repository is part of the *Big Data Engineering* course for the academic year **2024–2025** 🎓.

## ✨ Features

- 📊 Interactive dashboard built with **Streamlit**
- 🧠 Uses **OpenAI GPT** to generate simple medical explanations
- 🗃️ Data storage and querying powered by **MongoDB Atlas**
- 🔄 Easy CSV data import via `load_data.py`
- 🔍 Symptom-based disorder filtering
- 📋 Real-time relation type stats

---

## 📁 Project Structure

```
.
├── .streamlit/
│   └── secrets.toml         # Stores API keys (OpenAI)
├── .gitignore
├── dashboard.py             # Streamlit app for interactive exploration
├── LICENSE
├── load_data.py             # Script to load CSV data into MongoDB Atlas
├── README.md
├── relations.csv            # Dataset: [source, relationType, destination]
└── requirements.txt         # Python dependencies
```

---

## 🚀 Getting Started

### 1. 🧪 Install Dependencies

Make sure you are using **Python 3.8+**. Then install all required libraries:

```bash
pip install -r requirements.txt
```

---

### 2. ☁️ Set Up MongoDB Atlas

1. Create a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account.
2. Create a **new cluster** and **database** named `healthcare`.
3. Inside the `healthcare` database, create a **collection** named `relations`.
4. Whitelist your IP and get your connection string.
5. Update the MongoDB connection string inside `dashboard.py` and `load_data.py`:

```python
client = MongoClient("your-mongodb-connection-string")
```

---

### 3. 🔐 Set Up OpenAI API Key

In the file `.streamlit/secrets.toml`, store your OpenAI key like this:

```toml
[openai]
api_key = "your-openai-api-key"
```

> 🔒 *This file is ignored by Git. Don’t commit your secrets!*

---

### 4. 📥 Load the CSV into MongoDB

Use the `load_data.py` script to populate the `relations` collection:

```bash
python load_data.py
```

---

### 5. 🖥️ Run the Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Then visit [http://localhost:8501](http://localhost:8501) in your browser 🚀

---

## 🧠 How It Works

- The dashboard lets users select **two or more symptoms** from the sidebar.
- It queries **MongoDB** to find disorders that match **all selected symptoms**.
- Then, it uses **GPT** to explain those disorders in simple terms—perfect for educational and demo purposes!

---

## 📚 Example Use Case

Select:
- Symptom A: *Fever*
- Symptom B: *Cough*

➡️ The app identifies disorders like **Influenza** associated with both symptoms and provides a plain-language description and potential treatments.

---

## 🧾 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙌 Acknowledgments

Made with ❤️ for students of **Big Data Engineering 2024–25**  
Instructors: *Antonio Romano, Giuseppe Riccio, Vincenzo Moscato* 👨‍🏫