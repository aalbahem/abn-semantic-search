import os
from bs4 import BeautifulSoup
from lxml import etree


def walk_and_parse(data_dir):
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.xml'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    context = etree.iterparse(file_path, tag='ABR')
                    for action, elem in context:
                        elem_str = etree.tostring(elem, pretty_print=True).decode()

                        abr_tag = BeautifulSoup(elem_str, 'xml')
                        abrs = abr_tag.find_all('ABR')
                        for abr in abrs:
                            yield extract_entity_info(abr)



def extract_entity_info(abr_element):
    company_name_tag = abr_element.find_all('NonIndividualName')
    company_name = company_name_tag[0].text if company_name_tag else "Unknown"

    bussiness_address = abr_element.find_all('BusinessAddress')[0] # usig now only the first business address

    state_tag = bussiness_address.find_next('State')
    state = state_tag.text if state_tag else "Unknown"

    postcode_tag = bussiness_address.find_next('Postcode')
    postcode = postcode_tag.text if postcode_tag else "Unknown"

    return {
        'company_name': company_name,
        'state': state,
        'postcode': postcode
    }

if __name__ == '__main__':
    data_dir = 'test_data'
    for entity_info in walk_and_parse(data_dir):
        print(entity_info)