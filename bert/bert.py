from transformers import pipeline, pipelines
from transformers import AutoModelForSequenceClassification
from transformers import BertJapaneseTokenizer
import sys

#事前にtransformers，fugashi，ipadicをインストールする必要あり

args = sys.argv


#入力文字列がpositiveかnegativeかを判定
#scoreが1は最もpositiveで，-1は最もnegativeを意味する
#戻り値はリストでemotionにはpositiveかnegativeかが，scoreにはその度合いを表す数値が含まれている
def bert(TARGET_TEXT):
  model = AutoModelForSequenceClassification.from_pretrained("daigo/bert-base-japanese-sentiment")
  tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
  nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
  
  #感情分析の結果をresultに格納
  result = nlp(TARGET_TEXT)
  emotion = result[0]["label"]
  score = result[0]["score"]

  if emotion == "ネガティブ":
    emotion = "negative"
    score = -1 * score
  else:
    emotion = "positive"

  return [emotion, score]

#コマンドから文字列を取得
TARGET_TEXT = args[1]
#print(TARGET_TEXT)

#入力文字列の感情分析
result = bert(TARGET_TEXT)
#emotion
print(result[0])
#score


