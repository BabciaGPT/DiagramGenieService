import base64


def check_code_base64(ai_response, generator):
    if ai_response.plantuml_code:
        try:
            diagram_base64 = generator.generate_from_code(
                ai_response.plantuml_code.replace("\\n", "\n")
            )
            return base64.b64encode(diagram_base64).decode("utf-8")
        except Exception as e:
            print(str(e))
            return None
