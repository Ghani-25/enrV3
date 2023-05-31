import pinecone
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("Ghani-25/LF_enrich_sim", device='cpu')
pinecone.init(api_key='6da2a094-a957-4f4d-8892-059610a05980', environment='northamerica-northeast1-gcp')
index = pinecone.Index('find-region')

def enrichir(query, count):
    xq = model.encode(query).tolist()
    result = index.query(xq, top_k=count, includeMetadata=False)
    res = result.to_dict() #conversion to dict
    lis = list(res.values())[0]
    filtered_lis = [{'id': i['id'], 'score': i['score']} for i in lis if i['score'] > 0.75]
    return filtered_lis
