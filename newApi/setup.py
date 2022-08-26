import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

questionqrs = {
    'qtest1': {
        ' ADHD': [0, 10, 12, 16],
        ' Self': [4, 9, 15, 19],
        ' Anxiety': [1, 6, 13, 19],
        ' Suicide': [3, 5, 8, 14],
        ' Depression': [2, 8, 11, 17]
    }
}


ans_maps = {
    '1': 5,
    '2': 2.5,
    '3': 1,
    '4': -0.5,
    '5': -2
}

cred = credentials.Certificate(
    "coco-sih-firebase-adminsdk-qrhf1-88d3ad8656.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


class answers(BaseModel):
    u_id: str
    ans_id: str


@ app.post('/')
async def update_user_MH(ans: answers):
    adhd_s = 0
    self_s = 0
    suicide_s = 0
    anxiety_s = 0
    depression_s = 0
    result = db.collection('Answers').document(
        ans.u_id).collection('TestAnswers').document(ans.ans_id).get()
    if result.exists:
        print(result.to_dict())
        result = result.to_dict()
        # for i in range(4):
        #     adhd_s += ans_maps[result['answer']
        #                        [questionqrs[result['qtest1']][' ADHD'][i]]]
        #     self_s += ans_maps[result['answer']
        #                        [questionqrs[result['qtest1']][' Self'][i]]]
        #     suicide_s += ans_maps[result['answer']
        #                           [questionqrs[result['qtest1']][' Suicide'][i]]]
        #     anxiety_s += ans_maps[result['answer']
        #                           [questionqrs[result['qtest1']][' Anxiety'][i]]]
        #     depression_s += ans_maps[result['answer']
        #                              [questionqrs[result['qtest1']][' Depression'][i]]]

        for i in questionqrs[result['qtest1']][' ADHD']:
            adhd_s += float(result['answers'][i])
        for i in questionqrs[result['qtest1']][' Self']:
            self_s += float(result['answers'][i])
        for i in questionqrs[result['qtest1']][' Suicide']:
            suicide_s += float(result['answers'][i])
        for i in questionqrs[result['qtest1']][' Anxiety']:
            anxiety_s += float(result['answers'][i])
        for i in questionqrs[result['qtest1']][' Depression']:
            depression_s += float(result['answers'][i])

        db.collection('CHATBOT_HISTORY').document(ans.u_id).update(
            {" ADHD": firestore.Increment(adhd_s)})
        db.collection('CHATBOT_HISTORY').document(ans.u_id).update(
            {" Self": firestore.Increment(self_s)})
        db.collection('CHATBOT_HISTORY').document(ans.u_id).update(
            {" Suicide": firestore.Increment(suicide_s)})
        db.collection('CHATBOT_HISTORY').document(ans.u_id).update(
            {" Anxiety": firestore.Increment(anxiety_s)})
        db.collection('CHATBOT_HISTORY').document(ans.u_id).update(
            {" Depression": firestore.Increment(depression_s)})

    return
