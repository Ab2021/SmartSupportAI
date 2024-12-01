import streamlit as st
from agents.ticket_classification import TicketClassificationAgent
from agents.knowledge_base import KnowledgeBaseAgent
from agents.content_generation import ContentGenerationAgent
from database.db import db

# Initialize agents
tca = TicketClassificationAgent()
kba = KnowledgeBaseAgent()
cga = ContentGenerationAgent()

st.title("AI Customer Support System")

# Sidebar for system statistics
st.sidebar.title("System Overview")
st.sidebar.metric("Active Agents", "3")
st.sidebar.metric("Knowledge Base Entries", "100+")

# Main ticket submission form
st.header("Submit Support Ticket")

with st.form("ticket_form"):
    title = st.text_input("Ticket Title")
    description = st.text_area("Ticket Description")
    submitted = st.form_submit_button("Submit Ticket")

if submitted and title and description:
    with st.spinner("Processing ticket..."):
        # Step 1: Classify ticket
        category, priority = tca.process(title, description)
        
        # Step 2: Search knowledge base
        kb_solution = kba.process(title, description)
        
        # Step 3: Generate response
        response = cga.process(title, description, kb_solution)
        
        # Save ticket to database
        ticket_id = db.save_ticket(title, description, category, priority)
        
        # Display results
        st.success(f"Ticket processed successfully! ID: {ticket_id}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Ticket Classification")
            st.write(f"Category: {category}")
            st.write(f"Priority: {priority}")
        
        with col2:
            st.subheader("Knowledge Base Match")
            if kb_solution:
                st.write(kb_solution)
            else:
                st.write("No direct knowledge base match found.")
        
        st.subheader("Generated Response")
        st.write(response)

# Display sample tickets (for demonstration)
st.header("Recent Tickets")
st.dataframe({
    "ID": [1, 2, 3],
    "Title": ["Login Issue", "Billing Question", "Feature Request"],
    "Category": ["Technical Issue", "Billing", "Feature Request"],
    "Priority": ["High", "Medium", "Low"]
})
