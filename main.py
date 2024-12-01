import streamlit as st
import io
from datetime import datetime
from PIL import Image
from agents.ticket_classification import TicketClassificationAgent
from agents.priority_understanding import PriorityUnderstandingAgent
from agents.language_semantics import LanguageSemanticsAgent
from agents.knowledge_base import KnowledgeBaseAgent
from agents.content_generation import ContentGenerationAgent
from agents.intent_extraction import IntentExtractionAgent
from agents.solution_recommendation import SolutionRecommendationAgent
from agents.automated_resolution import AutomatedResolutionAgent
from database.db import db

# Initialize agents
tca = TicketClassificationAgent()
pua = PriorityUnderstandingAgent()
lsa = LanguageSemanticsAgent()
kba = KnowledgeBaseAgent()
cga = ContentGenerationAgent()
iea = IntentExtractionAgent()
ara = AutomatedResolutionAgent()
sra = SolutionRecommendationAgent()

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
        try:
            print("[DEBUG] Starting ticket processing pipeline...")
            
            # Step 1: Extract intent
            print("[DEBUG] Extracting ticket intent...")
            intent_info = iea.process(title, description)
            print(f"[DEBUG] Intent analysis: {intent_info}")

            # Step 2: Classify ticket
            print("[DEBUG] Classifying ticket...")
            category, initial_priority = tca.process(title, description)
            print(f"[DEBUG] Ticket classified as {category} with initial priority {initial_priority}")
            
            # Step 3: Analyze language semantics
            print("[DEBUG] Analyzing language semantics...")
            semantics = lsa.process(title, description)
            print(f"[DEBUG] Language analysis: {semantics}")
            
            # Step 3: Determine final priority and SLA
            print("[DEBUG] Determining priority and SLA...")
            priority_info = pua.process(title, description, initial_priority)
            priority = priority_info['priority']
            print(f"[DEBUG] Final priority: {priority}, SLA: {priority_info['sla_requirement']}")
            
            # Step 4: Search knowledge base
            print("[DEBUG] Searching knowledge base...")
            kb_solution = kba.process(title, description)
            
            # Validate knowledge base response
            if kb_solution and isinstance(kb_solution, str) and len(kb_solution.strip()) > 0:
                print("[DEBUG] Valid knowledge base solution found")
            else:
                print("[DEBUG] No valid knowledge base solution found")
                kb_solution = None
                
            # Step 5: Get solution recommendations
            print("[DEBUG] Generating solution recommendations...")
            solution_info = sra.process(title, description, kb_solution, category)
            print(f"[DEBUG] Solution recommendations: {solution_info}")
            
            # Step 6: Check for automation possibilities
            print("[DEBUG] Checking automation possibilities...")
            automation_info = ara.process(title, description, category, priority)
            print(f"[DEBUG] Automation analysis: {automation_info}")
            
            # Step 7: Generate response
            print("[DEBUG] Generating response...")
            response = cga.process(title, description, kb_solution)
            
            # Save ticket to database
            print("[DEBUG] Saving ticket to database...")
            ticket_id = db.save_ticket(title, description, category, priority)
            
            # Display results
            st.success(f"Ticket processed successfully! ID: {ticket_id}")
            print(f"[DEBUG] Ticket processing completed for ID: {ticket_id}")
        
        except Exception as e:
            error_message = f"An error occurred while processing the ticket: {str(e)}"
            print(f"[DEBUG] Error: {error_message}")
            st.error(error_message)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.subheader("Ticket Classification")
            st.write(f"Category: {category}")
            st.write(f"Priority: {priority}")
            st.write(f"SLA: {priority_info['sla_requirement']}")
        
        with col2:
            st.subheader("Language Analysis")
            st.write(f"Sentiment: {semantics['sentiment']}")
            st.write(f"Urgency: {semantics['urgency']}")
            st.write("Key Phrases:", ", ".join(semantics['key_phrases']))
        
        with col3:
            st.subheader("Intent Analysis")
            st.write(f"Primary Intent: {intent_info['primary_intent']}")
            st.write("Secondary Intents:", ", ".join(intent_info['secondary_intents']))
            st.write("Required Actions:", ", ".join(intent_info['required_actions']))
            st.write(f"Routing: {intent_info['routing']}")

        with col4:
            st.subheader("Solution Recommendations")
            st.write(f"Primary Solution: {solution_info['primary_solution']}")
            st.write("Alternative Approaches:", ", ".join(solution_info['alternative_approaches']))
            st.write(f"Est. Resolution Time: {solution_info['estimated_resolution_time']} mins")
            st.write(f"Confidence Level: {solution_info['confidence_level']}%")

        with col5:
            st.subheader("Automation Analysis")
            st.write(f"Can Automate: {'Yes' if automation_info['can_automate'] else 'No'}")
            if automation_info['can_automate']:
                st.write("Steps:", ", ".join(automation_info['automation_steps']))
                st.write(f"Success Probability: {automation_info['success_probability']}%")
                st.write("Required APIs:", ", ".join(automation_info['required_apis']))

        with col6:
            st.subheader("Knowledge Base Match")
            if kb_solution:
                st.write(kb_solution)
            else:
                st.write("No direct knowledge base match found.")
        
        st.subheader("Generated Response")
        st.write(response)
        
        # Add screenshot functionality
        try:
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ticket_{ticket_id}_{timestamp}.png"
            
            with st.spinner("Preparing screenshot..."):
                # Create an image with white background
                width, height = 800, 600
                img = Image.new('RGB', (width, height), 'white')
                
                # Setup for drawing text
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                
                # Draw ticket information with improved layout
                y_position = 40
                padding = 40
                line_height = 25
                
                # Draw header
                draw.text((width//2, 20), "Support Ticket Details", fill='black', font=font, anchor="mt")
                
                # Draw title
                draw.text((padding, y_position), f"Ticket ID: {ticket_id}", fill='black', font=font)
                y_position += line_height
                
                draw.text((padding, y_position), f"Title: {title}", fill='black', font=font)
                y_position += line_height
                
                draw.text((padding, y_position), f"Category: {category}", fill='black', font=font)
                y_position += line_height
                
                draw.text((padding, y_position), f"Priority: {priority}", fill='black', font=font)
                y_position += line_height
                
                # Draw description with word wrap
                description_lines = [description[i:i+60] for i in range(0, len(description), 60)]
                draw.text((padding, y_position), "Description:", fill='black', font=font)
                y_position += line_height
                
                for line in description_lines:
                    draw.text((padding, y_position), line, fill='black', font=font)
                    y_position += line_height
                
                # Convert image to bytes for download
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_bytes = img_buffer.getvalue()
                
                # Add download button
                st.download_button(
                    label="Download Ticket Screenshot",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png"
                )
        except Exception as e:
            error_message = f"Unable to generate screenshot: {str(e)}"
            print(f"[DEBUG] Screenshot error: {error_message}")
            st.warning("Screenshot functionality is currently unavailable")

# Display sample tickets (for demonstration)
st.header("Recent Tickets")
st.dataframe({
    "ID": [1, 2, 3],
    "Title": ["Login Issue", "Billing Question", "Feature Request"],
    "Category": ["Technical Issue", "Billing", "Feature Request"],
    "Priority": ["High", "Medium", "Low"]
})
