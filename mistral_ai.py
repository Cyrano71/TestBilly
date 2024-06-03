#----------------------------STEP1 : EXTRACT-------------------------
import PyPDF2

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file_obj.close()
    return text
   

#----------------------------STEP2 : FEED THE MODEL-------------------------
import mistralai

mistralai.api_key = "nXnjzxeTAjskhWosIQqEY6dukvyjjyIC"

generation = mistralai.Generation(
       model="your_model_here",
       prompt="your_prompt_here",
       max_new_tokens=10,
       do_sample=True,
       top_k=5
   )
response = generation.create()
print(response["choices"][0]["text"])