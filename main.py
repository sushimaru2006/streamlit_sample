from fastapi import FastAPI, HTTPException
import gensim
import gdown
import zipfile
import shutil

app = FastAPI()

# Google Drive file ID
file_id = "0ByFQ96A4DgSPUm9wVWRLdm5qbmc"
url = f"https://drive.google.com/uc?id={file_id}&export=download"
output = "download.zip"
gdown.download(url, output, quiet=False)
shutil.unpack_archive('download.zip')

print("Download complete.")
model = gensim.models.KeyedVectors.load_word2vec_format('model.vec', binary=False)
print("Load complete.")

@app.get("/word_merge/")
async def merge_word(str1: str="", str2: str="", op: str="+"):
    print(op)
    if op == "plus":
        return {"status": 200, "str": model.most_similar(positive=[str1,str2])}
    if op == "minus":
        return {"status": 200, "str": model.most_similar(positive=[str1],negative=[str2])}
    return {"status": 400, "detail": "op not found"}
