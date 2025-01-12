import pytesseract
import re


def match_content_by_list_regex(text: str, list_regex: list, num_content_to_remove_space: int = 0):
    results = []
    for idx, pattern in enumerate(list_regex):
        # Find the first match
        match = re.search(pattern, text, re.DOTALL)

        # Extract and print the content if found
        if match:
            content = match.group(1).strip()
            if num_content_to_remove_space > 0 and num_content_to_remove_space == idx:
                content = content.replace(" ", "")  # Remove spaces if specified
                if len(content) == 26:
                    print("Bank account is correct!")
                else:
                    raise ValueError(f"Bank account is wrong! check: {content}")

            if len(content) == 0:
                raise ValueError("Content is empty!")

            results.append(content)
        else:
            print("No match found")
    return results


def clean_up_item_in_list(list_items: list, string_to_clean: str, new_string: str):
    list_clean_up = [item.replace(string_to_clean, new_string) for item in list_items]
    return list_clean_up


def extract_important_info_by_ocr(image):
    text = pytesseract.image_to_string(image, lang='pol')  # Perform OCR
    # print(text) # Output the extracted text

    # Regular expression to extract the first match
    company_pattern = r"\nUbezpieczający\n(.*?)SPÓŁKA Z OGRANICZONĄ\nODPOWIEDZIALNOŚCIĄ\n"
    polisy_nr_pattern = r"(?:numer polisy:|Polisa nr)\s*(\d+)\n"
    company_adres_pattern = r"\n\nadres:\s*(.*?)\ne-mail"

    payer_info = match_content_by_list_regex(
        text=text,
        list_regex=[company_pattern, polisy_nr_pattern, company_adres_pattern],
        num_content_to_remove_space=0
    )
    payer_info[0] = payer_info[0] + " sp. z o.o."

    if len(payer_info) != 3:
        raise ValueError("The length of payer_info is not 3. It is {}".format(len(payer_info)))

    payment_pattern = r"\n\nPłatności\n\n(.*?)(\nóżnica:|termin płatności:)"
    recipient_text = match_content_by_list_regex(
        text=text,
        list_regex=[payment_pattern],
        num_content_to_remove_space=0
    )

    recipient_name_pattern = r"\n*\s*odbiorca:\s*(.*?)\n"
    recipient_adres_pattern = r"SA\n(.*?)\nnr rachunku:"
    recipient_bank_pattern = r"\nnr rachunku:\s*(.*?)\ntytuł"
    pay_amount_pattern = r"(?:kwota:|składka przed zmianą:|składka po zmianie:)\s*(\d+)\s?(?:zł|zl)"

    recipient_detail_info = match_content_by_list_regex(
        # text=text,
        text=recipient_text[0],
        list_regex=[recipient_name_pattern, recipient_adres_pattern, recipient_bank_pattern, pay_amount_pattern],
        num_content_to_remove_space=2
    )
    if len(recipient_detail_info) != 4:
        raise ValueError("The length of recipient_detail_info is not 4. It is {}".format(len(recipient_detail_info)))

    results = recipient_detail_info + payer_info

    if len(results) != 7:
        raise ValueError("The length of results_final is not 7. It is {}".format(len(results)))

    final_results = clean_up_item_in_list(list_items=results, string_to_clean="\n", new_string="")
    final_results = clean_up_item_in_list(list_items=final_results, string_to_clean="ALEJA", new_string="al")

    return final_results
