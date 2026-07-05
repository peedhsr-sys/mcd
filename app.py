import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="PDF Auto Editor", page_icon="📄")

st.title("PDF Auto Editor 📄")
st.write("Upload a PDF, find the specific text (like a name), and replace it instantly.")

# User Inputs
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])
old_text = st.text_input("Text to find (e.g., the old name):")
new_text = st.text_input("New text to replace it with:")

if st.button("Auto Edit PDF"):
    if uploaded_file and old_text and new_text:
        try:
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            changes_made = False

            # Scan pages and replace text
            for page in doc:
                text_instances = page.search_for(old_text)
                if text_instances:
                    changes_made = True
                    for inst in text_instances:
                        # Erase old text (White background)
                        page.add_redact_annot(inst, fill=(1, 1, 1))
                        page.apply_redactions()

                        # Insert new text in the exact same place
                        # Using 'helv' (Helvetica) as it closely matches standard PDF fonts
                        page.insert_text(
                            inst.tl, 
                            new_text, 
                            fontname="helv", 
                            fontsize=11, 
                            color=(0, 0, 0)
                        )

            if changes_made:
                output_pdf = io.BytesIO()
                doc.save(output_pdf)
                doc.close()
                
                st.success("Success! Text replaced perfectly.")
                st.download_button(
                    label="Download Edited PDF ⬇️",
                    data=output_pdf.getvalue(),
                    file_name="Edited_Document.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Could not find that exact text in the PDF. Please check for spelling or spaces.")

        except Exception as e:
            st.error(f"System Error: {e}")
    else:
        st.error("Please upload a PDF and fill in both fields before clicking edit.")
