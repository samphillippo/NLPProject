from time import time

# Load SciBERT tokenizer
# tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

# # Load SciBERT model
# model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")

# test_title = "The Role of Artificial Intelligence in Transforming Healthcare: A Comprehensive Review"

# test_abstract = """"
# Artificial Intelligence (AI) has emerged as a powerful tool with the potential to revolutionize various aspects of healthcare delivery, including diagnosis, treatment, patient care, and administrative processes. In this comprehensive review, we explore the multifaceted role of AI in transforming healthcare and examine its impact on different stakeholders, including patients, healthcare providers, policymakers, and researchers.

# The rapid advancements in machine learning, deep learning, and natural language processing have paved the way for the integration of AI technologies into healthcare systems worldwide. One of the primary areas where AI is making significant strides is in medical diagnostics. Machine learning algorithms can analyze complex medical data, including imaging scans, genetic information, and electronic health records, to assist healthcare professionals in diagnosing diseases accurately and efficiently. AI-powered diagnostic tools have shown promising results in detecting various medical conditions, ranging from cancer to infectious diseases, thereby improving patient outcomes and reducing healthcare costs.

# In addition to diagnostics, AI is also driving innovation in personalized medicine. By leveraging patient-specific data, including genetic profiles, medical history, and lifestyle factors, AI algorithms can tailor treatment plans to individual patients, optimizing therapeutic outcomes and minimizing adverse effects. Moreover, AI-powered predictive analytics tools can identify high-risk patients and intervene proactively to prevent disease progression or complications, leading to improved population health and reduced healthcare expenditures.

# Furthermore, AI is reshaping the landscape of medical research and drug discovery. Machine learning algorithms can analyze large-scale biomedical datasets to identify novel disease biomarkers, predict drug responses, and accelerate the development of new therapies. AI-driven virtual screening techniques enable researchers to explore vast chemical spaces more efficiently, facilitating the discovery of potential drug candidates for various diseases, including rare and neglected conditions.

# Beyond clinical applications, AI is also enhancing healthcare management and administration. Predictive analytics and optimization algorithms can optimize resource allocation, streamline workflow processes, and improve patient flow within healthcare facilities. AI-powered chatbots and virtual assistants are enhancing patient engagement and providing round-the-clock support for healthcare inquiries, appointment scheduling, and medication adherence.

# However, the widespread adoption of AI in healthcare poses several challenges and ethical considerations. Issues such as data privacy, security, bias, transparency, and accountability must be addressed to ensure the responsible and ethical deployment of AI technologies. Moreover, concerns about the potential job displacement of healthcare workers and the digital divide in access to AI-driven healthcare services need to be carefully considered and mitigated.

# In conclusion, AI holds tremendous promise for transforming healthcare delivery, diagnosis, treatment, and management. By harnessing the power of AI, we can usher in a new era of precision medicine, improve patient outcomes, and enhance the overall quality and efficiency of healthcare services. However, to realize the full potential of AI in healthcare, interdisciplinary collaboration, regulatory frameworks, and continuous innovation are essential to address the complex challenges and opportunities ahead.
# """

test_topics = ["Test", "AI"]

def generate_embedding(model, tokenizer, title, abstract, topics):
    # start_time = time()
    token_text = title + ". " + abstract + ". " + " ".join(topics)
    tokens = tokenizer.tokenize(token_text)

    token_embeddings = []
    for token in tokens:
        # Tokenize the token separately and get the token ID
        token_ids = tokenizer(token, return_tensors="pt")["input_ids"]

        # Get the embedding for the token
        with torch.no_grad():
            output = model(input_ids=token_ids)
            token_embedding = output.last_hidden_state.mean(dim=1).squeeze()

        token_embeddings.append(token_embedding)

    # Average all token embeddings
    average_embedding = torch.stack(token_embeddings).mean(dim=0)

    # print('Total Time: {} seconds\n'.format(round((time() - start_time), 2)))
    return average_embedding

# generate_embedding(test_title, test_abstract, test_topics)
