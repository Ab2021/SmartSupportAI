import streamlit as st
import io
import os
from datetime import datetime
from PIL import Image
from agents.ticket_classification import TicketClassificationAgent
from agents.priority_understanding import PriorityUnderstandingAgent
from agents.language_semantics import LanguageSemanticsAgent
from agents.knowledge_base import KnowledgeBaseAgent
from agents.content_generation import ContentGenerationAgent
from agents.intent_extraction import IntentExtractionAgent
from database.db import db

# Initialize agents
try:
    print("[DEBUG] Initializing AI agents...")
    tca = TicketClassificationAgent()
    pua = PriorityUnderstandingAgent()
    lsa = LanguageSemanticsAgent()
    kba = KnowledgeBaseAgent()
    cga = ContentGenerationAgent()
    iea = IntentExtractionAgent()
    print("[DEBUG] All agents initialized successfully")
except Exception as e:
    st.error(f"Error initializing agents: {str(e)}")
    print(f"[DEBUG] Agent initialization error: {str(e)}")
    raise

st.title("AI Customer Support System")

# Sidebar for system statistics
st.sidebar.title("System Overview")
st.sidebar.metric("Active Agents", "6")  # Updated to show actual number of agents
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
            
            # Ensure we have all required environment variables
            if not os.getenv('GROQ_API_KEY'):
                st.error("Missing GROQ API key. Please configure the environment.")
                raise ValueError("Missing GROQ API key")

            # Create and manage event loop
            async def process_ticket():
                async def run_agent_tasks():
                    tasks = [
                        iea.process_async(title, description),
                        tca.process_async(title, description),
                        lsa.process_async(title, description),
                        pua.process_async(title, description),
                        kba.process_async(title, description)
                    ]
                    return await asyncio.gather(*tasks, return_exceptions=True)

                try:
                    results = await asyncio.wait_for(run_agent_tasks(), timeout=30.0)
                    return results
                except asyncio.TimeoutError:
                    print("[DEBUG] Processing timeout")
                    raise TimeoutError("Processing timed out")
                except Exception as e:
                    print(f"[DEBUG] Error in process_ticket: {str(e)}")
                    raise

            # Execute ticket processing
            import asyncio
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(process_ticket())
                
                # Unpack results
                intent_response, classification_response, semantics_response, priority_response, kb_response = results
                
                # Process intent extraction results
                if not intent_response.success:
                    raise ValueError(f"Intent extraction failed: {intent_response.error}")
                intent_info = intent_response.data
                print(f"[DEBUG] Intent analysis: {intent_info}")

                # Process classification results
                if not classification_response.success:
                    raise ValueError(f"Classification failed: {classification_response.error}")
                ticket_data = classification_response.data
                category, initial_priority = ticket_data['category'], ticket_data['priority']
                print(f"[DEBUG] Classification: {category}, Priority: {initial_priority}")

                # Process semantics results
                if not semantics_response.success:
                    raise ValueError(f"Semantics analysis failed: {semantics_response.error}")
                semantics = semantics_response.data
                print(f"[DEBUG] Semantics analysis: {semantics}")

                # Process priority results
                if not priority_response.success:
                    raise ValueError(f"Priority analysis failed: {priority_response.error}")
                priority_info = priority_response.data
                final_priority = priority_info['priority']
                print(f"[DEBUG] Final priority: {final_priority}")

                # Process knowledge base results
                kb_solution = None
                if kb_response.success and isinstance(kb_response.data, str):
                    kb_solution = kb_response.data
                    print(f"[DEBUG] Found KB solution: {kb_solution[:100]}...")

                # Generate response
                response_data = loop.run_until_complete(
                    cga.process_async(title, description, kb_solution)
                )
                if not response_data.success:
                    raise ValueError(f"Response generation failed: {response_data.error}")
                response = response_data.data

                # Save ticket to database
                print("[DEBUG] Saving ticket to database...")
                ticket_id = db.save_ticket(title, description, category, final_priority)
                
                # Display results
                st.success(f"Ticket processed successfully! ID: {ticket_id}")
                
                # Display detailed results
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.subheader("Classification")
                    st.write(f"Category: {category}")
                    st.write(f"Priority: {final_priority}")
                    st.write(f"SLA: {priority_info['sla_requirement']}")

                with col2:
                    st.subheader("Language Analysis")
                    st.write(f"Sentiment: {semantics['sentiment']}")
                    st.write(f"Urgency: {semantics['urgency']}")
                    if semantics['key_phrases']:
                        st.write("Key Phrases:", ", ".join(semantics['key_phrases'][:3]))

                with col3:
                    st.subheader("Intent Analysis")
                    st.write(f"Primary: {intent_info['primary_intent']}")
                    if intent_info['secondary_intents']:
                        st.write("Secondary:", ", ".join(intent_info['secondary_intents'][:2]))
                    st.write(f"Routing: {intent_info['routing']}")

                with col4:
                    st.subheader("Knowledge Base")
                    if kb_solution:
                        st.write(kb_solution[:200] + "..." if len(kb_solution) > 200 else kb_solution)
                    else:
                        st.write("No direct match found")

                st.subheader("Generated Response")
                st.write(response)

                # Screenshot functionality
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ticket_{ticket_id}_{timestamp}.png"
                    
                    # Create image
                    width, height = 800, 600
                    img = Image.new('RGB', (width, height), 'white')
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.load_default()
                    
                    # Draw content
                    y_position = 40
                    padding = 40
                    line_height = 25
                    
                    # Header
                    draw.text((width//2, 20), "Support Ticket Details", fill='black', font=font, anchor="mt")
                    
                    # Ticket details
                    draw.text((padding, y_position), f"Ticket ID: {ticket_id}", fill='black', font=font)
                    y_position += line_height
                    
                    draw.text((padding, y_position), f"Title: {title}", fill='black', font=font)
                    y_position += line_height
                    
                    draw.text((padding, y_position), f"Category: {category}", fill='black', font=font)
                    y_position += line_height
                    
                    draw.text((padding, y_position), f"Priority: {final_priority}", fill='black', font=font)
                    y_position += line_height
                    
                    # Description with word wrap
                    description_lines = [description[i:i+60] for i in range(0, len(description), 60)]
                    draw.text((padding, y_position), "Description:", fill='black', font=font)
                    y_position += line_height
                    
                    for line in description_lines[:8]:  # Limit to prevent overflow
                        draw.text((padding, y_position), line, fill='black', font=font)
                        y_position += line_height
                    
                    # Save and offer download
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_bytes = img_buffer.getvalue()
                    
                    st.download_button(
                        label="Download Ticket Screenshot",
                        data=img_bytes,
                        file_name=filename,
                        mime="image/png"
                    )
                except Exception as e:
                    print(f"[DEBUG] Screenshot error: {str(e)}")
                    st.warning("Screenshot functionality unavailable")

            except TimeoutError:
                st.error("Processing timed out. Please try again.")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error processing ticket: {str(e)}")
                print(f"[DEBUG] Processing error: {str(e)}")
            finally:
                try:
                    loop.close()
                except Exception as e:
                    print(f"[DEBUG] Error closing event loop: {str(e)}")

        except Exception as e:
            st.error(f"System error: {str(e)}")
            print(f"[DEBUG] System error: {str(e)}")

# Display sample tickets
st.header("Recent Tickets")
st.dataframe({
    "ID": [1, 2, 3],
    "Title": ["Login Issue", "Billing Question", "Feature Request"],
    "Category": ["Technical Issue", "Billing", "Feature Request"],
    "Priority": ["High", "Medium", "Low"]
})