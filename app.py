from flask import Flask, render_template, request, jsonify
import os
from paddleocr import PaddleOCR
import json
from groq import Groq

import json
import re



app = Flask(__name__)
ocr = PaddleOCR(use_gpu=False)

groq_api_key = os.getenv('GROQ_API_KEY')

# Groq API Key
# api_key = "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"  # Replace with your actual Groq API key
# client = Groq(api_key=api_key)

# Groq API Key
# api_key = "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"  # Replace with your actual Groq API key
groq_client = Groq(api_key="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")


@app.route("/")
def index():
    return render_template("index.html")


ocr = PaddleOCR(
    use_gpu=False,  # Disable GPU usage
    use_xpu=False,  # Disable XPU (if applicable)
    use_npu=False,  # Disable NPU (if applicable)
    use_mlu=False   # Disable MLU (if applicable)
)


@app.route("/process", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # OCR the image
        result = ocr.ocr(file_path)
        extracted_text = "\n".join([line[1][0] for line in result[0]])
        print("Extracted Text:", extracted_text)  # Debugging

        # Use Groq API to process the text
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Given the following medical test results, extract and return a JSON object containing only "
                            f"the following 13 tests and their results. "
                            f"If a test from this list is not present in the data, set its value to null. Ignore any tests "
                            f"that are not in this list. Tests to include: WBC Count RBC Count Haemoglobin Hematocnt MCV MCH "
                            f"MCHC Platelet Count Neutrophils Lymphocytes Monocytes Eosinophil Basophils Data: {extracted_text} "
                            f"Response: The response should be a JSON object containing only the specified 13 tests and their results, "
                            f"with null as the value for any missing tests."
                        ),
                    }
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
            )
            response_content = completion.choices[0].message.content.strip()
            print("Response Content:", response_content)  # Debugging

            # Use regex to extract the JSON from the response string
            json_match = re.search(r'```json\n(.*?)```', response_content, re.DOTALL)
            if json_match:
                response_json = json.loads(json_match.group(1).strip())
            else:
                return "Failed to extract JSON from the response content."

        except json.JSONDecodeError:
            return "Failed to parse JSON response from the API."
        except Exception as e:
            print(f"Error during API call: {e}")
            return "An error occurred while calling the API. Please try again later."

        return render_template("result.html", data=response_json)

    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # OCR the image
        result = ocr.ocr(file_path)
        extracted_text = "\n".join([line[1][0] for line in result[0]])
        print("Extracted Text:", extracted_text)  # Debugging

        # Use Groq API to process the text
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Given the following medical test results, extract and return a JSON object containing only "
                            f"the following 13 tests and their results. "
                            f"If a test from this list is not present in the data, set its value to null. Ignore any tests "
                            f"that are not in this list. Tests to include: WBC Count RBC Count Haemoglobin Hematocnt MCV MCH "
                            f"MCHC Platelet Count Neutrophils Lymphocytes Monocytes Eosinophil Basophils Data: {extracted_text} "
                            f"Response: The response should be a JSON object containing only the specified 13 tests and their results, "
                            f"with null as the value for any missing tests."
                        ),
                    }
                ],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
            )
            response_content = completion.choices[0].message.content.strip()
            print("Response Content:", response_content)  # Debugging

            # Handle empty or invalid responses
            if not response_content.strip():
                return "The API returned an empty response. Please try again."
            response_json = json.loads(response_content)
        except json.JSONDecodeError:
            return "Failed to parse JSON response from the API."
        except Exception as e:
            print(f"Error during API call: {e}")
            return "An error occurred while calling the API. Please try again later."

        return render_template("result.html", data=response_json)

# if __name__ == "__main__":
#     app.run(debug=False)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if no port is set
    app.run(debug=True, host="0.0.0.0", port=port)