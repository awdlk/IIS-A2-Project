import streamlit
from main import answerCheck, aiAsk, checkAnswer_agin #导入函数，ps:这儿不是调用
streamlit.title("verification of ai answer")
streamlit.warning("Do not ask questions again after using the built-in translation feature of the webpage, as it may not be compatible")

#保存ai的结果和用户的反馈，如果不用streamlit.session_state，则点击这个新按钮时，原来ask ai的按钮可能会不成立导致页面上的ai回答消失
if "result" not in streamlit.session_state:
    streamlit.session_state.result= None

if"feedback" not in streamlit.session_state:
    streamlit.session_state.feedback =None

if"reportIssue" not in streamlit.session_state:
    streamlit.session_state.reportIssue = None

if "recheckResult" not in streamlit.session_state:
    streamlit.session_state.recheckResult = None

question = streamlit.text_area("enter question: ")#从网页获取用户的输入
if streamlit.button("ask ai"):
    if question.strip():#strip是移除没啥用的空白字符、也就是清理用户输入
        with streamlit.spinner("ai working……"):
            aiAnswer =aiAsk(question)
            factCheck= answerCheck(question,aiAnswer)
        streamlit.session_state.result ={"question": question,"aianswer":aiAnswer,"factcheck":factCheck}#在会话状态中找result，没有就创建初始值none，然后再创建结果
        #session_state.result是保存ai回答，防止其他按钮触发页面重新执行后回答消失
        #重新收集反馈
        streamlit.session_state.feedback =None
        #session_state.feedback是保存用户的选择，让程序知道用户点击的是maybe correct还是maybe not correct,并显示feedback
        streamlit.session_state.reportIssue =None#提出新问题时清除旧报告
        streamlit.session_state.recheckResult = None #清除之前的ai给出的回答


    else:
        streamlit.warning("enter question")

        # 读取session_state，然后显示结果
if streamlit.session_state.result is not None: 
    result = streamlit.session_state.result
    streamlit.write("user asks:",result["question"])
    streamlit.subheader("ai1 Answer")
    streamlit.write(result["aianswer"])
    streamlit.subheader("ai2 factCheck")
    streamlit.write(result["factcheck"])
    streamlit.info("user do not get any external sources at now")#这里后面要改，api外部资源功能未完成
    #这里是用户反馈的按钮
    streamlit.subheader("feedback")#修改feedback是为了让程序知道用户刚才选择了什么，因为用户点击按钮时候streamlit会重新执行一遍所有内容，因此如果不修改就会导致执行到这里的时候依旧是none
    streamlit.write("do you agree for the assessment which from ai2?")

    if streamlit.button("maybe correct"):
        streamlit.session_state.feedback= "maybe correct"
        streamlit.session_state.reportIssue = None 
        streamlit.session_state.recheckResult = None#确保如果改变主意后把反馈从not correct更改到correct后，之前错误的反馈没有保留
    if streamlit.button("maybe not correct"):
        streamlit.session_state.feedback ="maybe not correct"
    if streamlit.session_state.feedback =="maybe correct":
        streamlit.success("thank you")
    elif streamlit.session_state.feedback =="maybe not correct":
        streamlit.warning("ai2 may gives unrelibale assessment, please check with yourself")
        reason = streamlit.text_area("what looklike not correct?")

        #用户要提交报告
        if streamlit.button("submit report"):
            if reason.strip():
                streamlit.session_state.reportIssue = reason.strip()
                streamlit.session_state.recheckResult= None
            else:
                streamlit.warning("please describe your problem")

#提交了报告后才可以进行重新审查
        if streamlit.session_state.reportIssue is not None:
            streamlit.success("your report has been recorded")
            streamlit.write("reportIssue:",streamlit.session_state.reportIssue)

            if streamlit.button("request recheck"):
             with streamlit.spinner("ai2 is reviewing……"):
                newCheck = checkAnswer_agin(result["question"],result["aianswer"],result["factcheck"],streamlit.session_state.reportIssue)
             streamlit.session_state.recheckResult = newCheck

            if  streamlit.session_state.recheckResult is not None:
                streamlit.subheader("revised assessment")
                streamlit.write(streamlit.session_state.recheckResult)

                streamlit.info("This reassessment has not independently verified external sources.")
