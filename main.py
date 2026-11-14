
import os
from dotenv import load_dotenv
from openai import OpenAI
#load_dotenv是把.env文件里的配置加载到python进程的环境变量中，因为evn是普通文本文件、不会自动加载，所以需要手动加载
load_dotenv()

# 创建api客户端
clientapi = OpenAI(
    #getenv是获取环境变量中某一项配置的值的函数
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)


# ai1用来回答用户的问题
def aiAsk(question):
    #发送请求,clientapi是客户端对象，.chat是进入聊天接口,completions是找到聊天补全资源，create是执行api请求
    ai1response = clientapi.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "user", "content": question}
        ]
    )

    firstChoice = ai1response.choices[0]#把选择存为第一个候选结果
    aiMessage = firstChoice.message#存为该结果中的ai消息
    aiText = aiMessage.content#消息中ai回答的内容
    return aiText#把内容返回给其他程序


# ai2进行二次验证
def answerCheck(question,aiAnswer):
    ai2response = clientapi.chat.completions.create(
        model= os.getenv("LLM_MODEL"),
        messages= [
            {"role" : "system",
             "content": ("you are fact-checking assistant, identify factual claims in the answer and access, whether they correct or not. And give a brief overall assessment, list up to three important claims with their possible errors or uncertainties, and state clearly that no external sources have been independently verified.Use the original question for context, assess only factual claims actually made in the AI1 answer. Must keep the response under 150 words.")},
        {"role" : "user", "content" :"original question" +question+ "\nai1 answer: "+ aiAnswer}
        ]
    )
    firstChoice = ai2response.choices[0]
    aiMessage = firstChoice.message
    aiText = aiMessage.content
    return aiText

#重新核查时候，希望ai2还知道ai2上一次的判断factCheck和reportIssue也就是用户认为哪里可能会有错误
def checkAnswer_agin(question, aianswer,factCheck,reportIssue):
    response= clientapi.chat.completions.create(
        model= os.getenv("LLM_MODEL"),
        messages= [
            {"role": "system", "content": "you are review previous ai factcheck, and then consider user's reported issue, but do not assume the user is correct, reassess original answer, and explain whether your previous judgement should change, and identify remaining uncertainties. Do not invent source or claim independent external verification.Keep the revised assessment under 200 words.Focus on whether the previous judgement should change,why it should change, and what remains uncertain.Do not claim to remember earlier reports."},
            {"role":"user","content":("original question:" + question+ "\nai1 answer: "+ aianswer+"\nprevious assessment: " + factCheck+"\nuser reportIussue: "+ reportIssue)}
        ]
    )
    firstChoice = response.choices[0]#把选择存为第一个候选结果
    aiMessage = firstChoice.message#存为该结果中的ai消息
    aiText = aiMessage.content#消息中ai回答的内容
    return aiText#把内容返回给其他程序


#__是用来区分直接运行与被导入两种情况，也就是直接运行main文件时，就执行以下代码，且当app导入main时，便不执行以下代码。
if __name__ == "__main__":
   question = input("Enter your question: ") 
   aiAnswer = aiAsk(question)
   factCheck = answerCheck(question,aiAnswer)
   print("AI Answer:")
   print(aiAnswer)
   print("Fact Check:")
   print(factCheck)