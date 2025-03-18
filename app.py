import streamlit as st
import pypdf
import io

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file using pypdf
    """
    try:
        # Create a PDF reader object
        pdf_reader = pypdf.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = []
        for page in pdf_reader.pages:
            text.append(page.extract_text())
            
        return "\n".join(text)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def main():
    # Set page title
    st.title("PDF Text Extractor")
    
    # Add description
    st.write("""
    Upload a PDF file to extract its text content. 
    The application will process the file and display the extracted text below.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf",
        help="Upload a PDF file to extract its text content"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write("File Details:")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
        
        # Add a button to process the file
        if st.button("Extract Text"):
            with st.spinner("Processing PDF..."):
                # Extract text from the PDF
                text = extract_text_from_pdf(uploaded_file)
                
                if text:
                    # Create an expander for the extracted text
                    with st.expander("Extracted Text", expanded=True):
                        st.text_area(
                            "Content",
                            value=text,
                            height=400,
                            disabled=True
                        )
                        
                        # Add download button for the extracted text
                        st.download_button(
                            label="Download extracted text",
                            data=text,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_extracted.txt",
                            mime="text/plain"
                        )

if __name__ == "__main__":
    main()
