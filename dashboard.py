import streamlit as st

from bson.son import SON
from openai import OpenAI
from pymongo import MongoClient


if __name__ == "__main__":
    # ---- COLLEGAMENTO A MONGODB ----
    client = MongoClient('mongodb+srv://giuseppericcio:1234@cluster0.weahziy.mongodb.net/?retryWrites=true&w=majority')

    db = client.healthcare
    relations = db.relations

    # ---- CONFIGURAZIONE PAGINA ----
    st.set_page_config(page_title='MedicalAssistantGPT', page_icon='medical_symbol', layout='wide')
    st.title(':medical_symbol: MedicalAssistantGPT')

    # ---- IDENTIFICO LE RELAZIONI PRESENTI NEL DB ----
    @st.cache_data
    def countRelationType(_relations):
        relations_type = list(relations.aggregate([
        {"$group": {"_id" : "$relationType", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
        ]))

        return relations_type

    # ---- IDENTIFICO TUTTI I SINTOMI PRESENTI NEL DB ----
    @st.cache_data
    def get_symptoms(_relations):
        possibleSymptoms = list(relations.aggregate([
            {"$match": {"relationType": "symptom"}},
            {"$group": {"_id": None, "uniqueValues": {"$addToSet": "$destination"}}}
        ]))[0]['uniqueValues']
        
        return possibleSymptoms

    # ---- SIDEBAR ----
    possible_symptoms = get_symptoms(relations)
    st.session_state['selected_symptoms'] = st.sidebar.multiselect("Select at least two symptoms: ", possible_symptoms)
    selected_symptoms = st.session_state['selected_symptoms']

    # ---- MAIN PAGE ----
    relations_type = countRelationType(relations)
    st.subheader('🔗 Relation Types')
    st.dataframe(relations_type, use_container_width=True)

    # ---- IDENTIFICO I DISORDINI ASSOCIATI A QUEL SINTOMO ----
    if len(selected_symptoms) >= 2:
        related_disorders = list(relations.aggregate([
            {"$match": {"relationType": "symptom", "destination": 
                        {"$in": selected_symptoms } }},
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$match": {"count": {"$eq": len(selected_symptoms)}}}
        ]))

        related_disorders = [x['_id'] for x in related_disorders]
        st.subheader("🤒 Related disorders")
        st.dataframe(related_disorders, use_container_width=True)

        # ---- FORNISCO UNA SPIEGAZIONE SEMPLICE DELLA MALATTIA E DELLE SUE POSSIBILI CURE
        #      TRAMITE LE API DI OPENAI ----
        prompt = "As a medical assistant, your role is to provide easy-to-understand explanations " \
                "to patients about potential health conditions based on their reported symptoms. " \
                "You will be given a list of symptoms and a corresponding list of disorders that " \
                "are associated with these symptoms.\
        \
        The input is: \
        Symptoms = {} \
        Disorders = {} \
        \
        You will need to provide a clear and concise explanation of the reported potential disorders, " \
                "including their symptoms and possible treatments, to help the patient better understand " \
                "their condition. Your primary goal is to assist the patient in understanding their medical " \
                "condition and to ensure that they have the necessary knowledge to make informed decisions " \
                "about their healthcare. Therefore, you should communicate in a manner that is both " \
                "compassionate and informative.".format(selected_symptoms, related_disorders)

        client = OpenAI(
            # This is the default and can be omitted
            api_key=st.secrets.openai.api_key,
        )

        if len(related_disorders) != 0:
            st.subheader("🧠 Disorder explanation")
            message = {"role": "user", "content": prompt}
            st.session_state['completion'] = client.chat.completions.create(model="gpt-4o-mini", messages=[message], temperature=0)
            completion = st.session_state['completion']
            st.write(completion.choices[0].message.content)
