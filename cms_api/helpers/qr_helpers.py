import base64


def get_student_code_from_qr(qr_code_srt):
    qr_code_segment = qr_code_srt.split("|")

    match (qr_code_segment[0]):
        case "CMS_V1":
            base64_string = qr_code_segment[1]
            try:
                decoded_str = base64.b64decode(base64_string).decode("utf-8")
                return decoded_str.split("|")[1]
            except:
                return None
        case _:
            return None
