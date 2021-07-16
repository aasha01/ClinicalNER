import src.DAO.ConnectUMLS as umls_extract


def extract_entity_word(word):
    return umls_extract.get_entity(word)


def extract_entity_sentence(sentence):
    entity_list = []
    for i, word in enumerate(sentence):
        entity_list.append(extract_entity_word(word))
    return entity_list


if __name__ == "__main__":
    text = "The malleolus is non-tender medially or laterally with no ligamentous tenderness either"
    print(extract_entity_sentence(text))