import streamlit as st
import PyPDF2
import os

def remove_password(input_pdf, password):
    try:
        # Open the PDF file
        reader = PyPDF2.PdfReader(input_pdf)

        # Check if the PDF is encrypted
        if reader.is_encrypted:
            if not password:
                return "Error: Password is required"
            if not reader.decrypt(password):
                return "Error: Incorrect password"

        # Create a writer object
        writer = PyPDF2.PdfWriter()

        # Copy pages
        for page in reader.pages:
            writer.add_page(page)

        # Create output file name
        output_pdf = "decrypted_" + os.path.basename(input_pdf.name)

        # Save the new PDF
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

        return output_pdf

    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🔐 PDF Password Remover")

uploaded_file = st.file_uploader("Upload an Encrypted PDF", type=["pdf"])
password = st.text_input("Enter PDF Password", type="password")

if uploaded_file and password:
    if st.button("Remove Password"):
        result = remove_password(uploaded_file, password)
        
        if "Error" in result:
            st.error(result)
        else:
            st.success("Success! Download your file below:")
            with open(result, "rb") as f:
                st.download_button("Download Decrypted PDF", f, file_name=result, mime="application/pdf")
