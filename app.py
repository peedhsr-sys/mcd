import streamlit as st
import fitz  # PyMuPDF
import io

# वेबसाइट का टाइटल और डिज़ाइन
st.set_page_config(page_title="PDF Editor Tool", page_icon="📝")
st.title("PDF Text Editor App 📝")
st.write("अपनी PDF अपलोड करें, पुराना टेक्स्ट डालें और उसे नए टेक्स्ट से रिप्लेस करें।")

# यूज़र से इनपुट लेना
uploaded_file = st.file_uploader("यहाँ अपनी PDF फाइल अपलोड करें", type=["pdf"])
old_text = st.text_input("पुराना टेक्स्ट (जिसे हटाना है):")
new_text = st.text_input("नया टेक्स्ट (जो लिखना है):")

if st.button("PDF को एडिट करें ✨"):
    if uploaded_file is not None and old_text and new_text:
        try:
            # PDF को मेमोरी में पढ़ें
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            changes_made = False

            # हर पेज पर टेक्स्ट खोजें और रिप्लेस करें
            for page in doc:
                text_instances = page.search_for(old_text)
                if text_instances:
                    changes_made = True
                    for inst in text_instances:
                        # 1. पुराने टेक्स्ट को सफेद रंग से मिटाएं (Redact)
                        page.add_redact_annot(inst, fill=(1, 1, 1))
                        page.apply_redactions()

                        # 2. उसी जगह पर नया टेक्स्ट लिखें
                        page.insert_text(
                            inst.tl, 
                            new_text, 
                            fontname="helv", # डिफ़ॉल्ट फॉन्ट
                            fontsize=11,     
                            color=(0, 0, 0)  # काला रंग
                        )

            if changes_made:
                # नई PDF को तैयार करें
                output_pdf = io.BytesIO()
                doc.save(output_pdf)
                doc.close()
                
                st.success(f"बधाई हो! '{old_text}' को सफलतापूर्वक बदल दिया गया है।")
                
                # डाउनलोड बटन दें
                st.download_button(
                    label="नई PDF डाउनलोड करें ⬇️",
                    data=output_pdf.getvalue(),
                    file_name="Edited_Document.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning(f"इस PDF में '{old_text}' कहीं नहीं मिला। कृपया स्पेलिंग चेक करें।")

        except Exception as e:
            st.error(f"कुछ तकनीकी खराबी आ गई: {e}")
    else:
        st.error("कृपया पहले PDF अपलोड करें और दोनों बॉक्स में टेक्स्ट भरें।")
