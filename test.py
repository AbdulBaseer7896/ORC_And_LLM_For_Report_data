
# from groq import Groq

# # Provide the API key in the code
# api_key = "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"
# client = Groq(api_key=api_key)

# # Create the completion request
# completion = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {
#             "role": "user",
#             "content": (
#                 "\"Given the following medical test results, extract and return a JSON object containing only the following 13 tests and their results. "
#                 "If a test from this list is not present in the data, set its value to null. Ignore any tests that are not in this list. "
#                 "Tests to include: WBC Count RBC Count Haemoglobin Hematocnt MCV MCH MCHC Platelet Count Neutrophils Lymphocytes Monocytes Eosinophil Basophils "
#                 "Data: {Flabs Hello@flabs.in +917253928905 https://www.flabs.in/ Name : Mr Dummy Patient ID PN2 Age/Gender : 20/Male Report ID : RE1 "
#                 "Referred By : Self Collection Date: 24/06/2023 08:49PM Phone No. : Report Date 24/06/2023 09:02PM HAEMATOLOGY COMPLETE BLOOD COUNT (CBC) "
#                 "TEST DESCRIPTION RESULT REF.RANGE UNIT Haemoglobin 15 13-17 g/dL Total Leucocyte Count 5000 4000-10000 /cumm Differential Leucocyte Count "
#                 "Neutrophils 50 40-80 % Lymphocytes 40 20 - 40 % Eosinophils 1 1 - 6 % Monocytes 6 2-10 % Basophils 0.00 0-1 % Absolute Leucocyte Count "
#                 "Absolute Neutrophils 2500.00 2000 -7000 /cumm Absolute Lymphocytes 2000.00 1000 -3000 /cumm Absolute Eosinophils 50.00 20 - 500 /cumm "
#                 "Absolute Monocytes 450.00 200 - 1000 /cumm RBC Indices RBC Count 5 4.5- 5.5 Mil- lion/cumm MCV 80.00 81-101 fL MCH 30.00 27-32 pg "
#                 "MCHC 37.50 31.5-34.5 g/dL Hct 40 40 - 50 % RDW-CV 12 11.6-14.0 % RDW-SD 40 39 - 46 fL Platelets Indices Platelet Count 300000 150000 - 410000 /cumm "
#                 "PCT 35 MPV 8 7.5-11.5 fL PDW 9 Interpretation:} Response: {The response should be a JSON object containing only the specified 13 tests "
#                 "and their results, with null as the value for any missing tests.}\""
#             )
#         }
#     ],
#     temperature=1,
#     max_completion_tokens=1024,
#     top_p=1,
#     stream=False,  # Set to False for a single response
#     stop=None,
# )

# # Extract the JSON response
# response_content = completion.choices[0].message.content.strip()

# # Print only the JSON response
# print("this si the responce data " , response_content)


# # Extract the JSON response
# response_content = completion.choices[0].message.content.strip()

# # Find the JSON object in the response
# import json
# import re

# # Extract JSON using regex
# json_match = re.search(r"\{.*\}", response_content, re.DOTALL)
# if json_match:
#     json_data = json_match.group(0)
#     # Print the JSON response
#     print("this is just the josn " , json_data)
# else:
#     print("No valid JSON found in the response.")






from paddleocr import PaddleOCR
from groq import Groq
import re
import json

print("step 1")

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR for English

print("step 2")

# Function to extract text from an image
def extract_text_from_image(image_path):
    print("step 3")
    result = ocr.ocr(image_path, cls=True)  # Perform OCR on the image
    print("step 4")
    extracted_text = ""
    for line in result[0]:
        print("step 5")
        extracted_text += line[1][0] + " "  # Concatenate the detected text
    print("step 6")
    return extracted_text.strip()

# Groq API Key
api_key = "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"  # Replace with your actual Groq API key
client = Groq(api_key=api_key)

print("step 7")


# File path of the image
image_path = "test_2.jpg"  # Replace with your image file path

print("step 8")

# Extract text from the image
extracted_text = extract_text_from_image(image_path)
print("step 9999")

# Create the completion request using the extracted text
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": (
                f"\"Given the following medical test results, extract and return a JSON object containing only the following 13 tests and their results. "
                "If a test from this list is not present in the data, set its value to null. Ignore any tests that are not in this list. "
                "Tests to include: WBC Count RBC Count Haemoglobin Hematocnt MCV MCH MCHC Platelet Count Neutrophils Lymphocytes Monocytes Eosinophil Basophils "
                f"Data: {extracted_text} "
                "Response: {The response should be a JSON object containing only the specified 13 tests and their results, with null as the value for any missing tests.}\""
            )
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,  # Set to False for a single response
    stop=None,
)

print("step 10")
# Extract the JSON response
response_content = completion.choices[0].message.content.strip()

print("step 11")

# Find and print the JSON object in the response
json_match = re.search(r"\{.*\}", response_content, re.DOTALL)
print("step 12")

if json_match:
    print("step 13")
    json_data = json_match.group(0)
    print("step 14")
    print(json_data)
    print("step 15")
else:
    print("No valid JSON found in the response.")
