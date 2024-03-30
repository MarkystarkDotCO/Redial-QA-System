import jsonlines
import json
from datetime import datetime

# Open the JSONL file

def process(filename, task):
    with jsonlines.open(filename, 'r') as reader:
        # Read each line (JSON object) in the file
        # i=0
        # context=""
        # question=""
        # answer=""
        dialogues=[]
        
        for data in reader:
            context=""
            # print(data)
            for movie_id in data['movieMentions']:
                # movie_id = str(0)
                # movie_id = int(movie_id)
                # print("for", data["movieMentions"][movie_id])
                if data["movieMentions"][movie_id]:
                    context+="For "+ data["movieMentions"][movie_id]
                if movie_id in data["respondentQuestions"] and data["respondentQuestions"][movie_id]:
                    if data["respondentQuestions"][movie_id]['liked']==0:
                        # print("respondent don't like it")
                        context+=" respondent don't like it"
                    elif data["respondentQuestions"][movie_id]['liked']==1:
                        # print("respondent like it")
                        context+=" respondent like it"
                    else:
                        # print("respondent has no idea")
                        context+=" respondent has no idea"
                # print(data["initiatorQuestions"][movie_id]['liked'])
                # print(type(movie_id), movie_id)
                if movie_id in data["initiatorQuestions"] and data["initiatorQuestions"][movie_id]:
                    if data["initiatorQuestions"][movie_id]['liked']==0:
                        # print("initiator don't like it")
                        context+=" initiator don't like it"
                    elif data["initiatorQuestions"][movie_id]['liked']==1:
                        # print("initiator like it")
                        context+=" initiator like it"
                    else:
                        # print("initiator has no idea")
                        context+=" initiator has no idea"
                context+=", "
            # print(context)

            # sentences = "context:"+context+","
            question=[]
            answer=[]
            messages_iter = iter(data["messages"])
            # state=0
            # print(context)
            senderWorkerId=data["messages"][0]['senderWorkerId']
            for msg in messages_iter:
                # sentences+= ", "+msg['text']+", "
                # print(msg['senderWorkerId'])
                if msg['senderWorkerId']==senderWorkerId:
                    # print("Question:", msg['text'])
                    # question+=", "+msg['text']+", "
                    question.append(msg['text'])
                else:
                    # answer+=", "+msg['text']+", "
                    answer.append(msg['text'])
            # sentences+="question"+", "+question+", answer, "+answer
            # print(sentences)
            # print(context)
            # print(question)
            # print(answer)
            
            dialogues.append({"context":context, "questions":question, "answers":answer })
        # print(dialogues)
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_path = f'../../data/processed/redial_dataset_{current_date}_'+task+".json"

        # Open the file in write mode and write the dictionary as JSON
        with open(file_path, "w") as json_file:
            json.dump(dialogues, json_file)
                    # print("answer:", msg['text'])
                # if msg['senderWorkerId'] and msg['senderWorkerId']==0:
                #     question+=msg['text']
                #     try:
                #         # Get the next message
                #         next_msg = next(messages_iter)
                #         # print("Next message:", next_msg)
                #         if next_msg['senderWorkerId']==1:
                #             sentences+="question:"+question+","
                #             question=""
                #     except StopIteration:
                #         print("No next message available")
                # elif msg['senderWorkerId'] and msg['senderWorkerId']==1:
                #     answer+=msg['text']
                #     # print(sentences)
                #     try:
                #         # Get the next message
                #         next_msg = next(messages_iter)
                #         # print("Next message:", next_msg)
                #         if next_msg['senderWorkerId']==0:
                #             sentences+="answer:"+answer+","
                #             answer=""
                #             print(sentences)
                #             sentences=""
                #     except StopIteration:
                #         print("No next message available")
                
                # print("context:",context)


    # {
    #     "movieMentions": 
    #         {"203371": "Final Fantasy: The Spirits Within (2001)", 
    #         "84779": "The Triplets of Belleville (2003)",  
    #         "122159": "Mary and Max (2009)", 
    #         "151313": "A Scanner Darkly  (2006)", 
    #         "191602": "Waking Life (2001)", 
    #         "165710": "The Boss Baby (2017)"}, 
    #     "respondentQuestions": 
    #         {"203371": {"suggested": 1, "seen": 0, "liked": 1}, 
    #         "84779": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "122159": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "151313": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "191602": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "165710": {"suggested": 1, "seen": 0, "liked": 1}}, 
    #     "messages": 
    #     [{"timeOffset": 0, "text": "Hi there, how are you? I'm looking for movie recommendations", "senderWorkerId": 0, "messageId": 1021}, 
    #         {"timeOffset": 15, "text": "I am doing okay. What kind of movies do you like?", "senderWorkerId": 1, "messageId": 1022}, 
    #         {"timeOffset": 66, "text": "I like animations like @84779 and @191602", "senderWorkerId": 0, "messageId": 1023}, 
    #         {"timeOffset": 86, "text": "I also enjoy @122159", "senderWorkerId": 0, "messageId": 1024}, 
    #         {"timeOffset": 95, "text": "Anything artistic", "senderWorkerId": 0, "messageId": 1025}, 
    #         {"timeOffset": 135, "text": "You might like @165710 that was a good movie.", "senderWorkerId": 1, "messageId": 1026}, 
    #         {"timeOffset": 151, "text": "What's it about?", "senderWorkerId": 0, "messageId": 1027}, 
    #         {"timeOffset": 207, "text": "It has Alec Baldwin it is about a baby that works for a company and gets adopted it is very funny", "senderWorkerId": 1, "messageId": 1028}, 
    #         {"timeOffset": 238, "text": "That seems like a nice comedy", "senderWorkerId": 0, "messageId": 1029}, 
    #         {"timeOffset": 272, "text": "Do you have any animated recommendations that are a bit more dramatic? Like @151313 for example", "senderWorkerId": 0, "messageId": 1030}, 
    #         {"timeOffset": 327, "text": "I like comedies but I prefer films with a little more depth", "senderWorkerId": 0, "messageId": 1031}, 
    #         {"timeOffset": 467, "text": "That is a tough one but I will remember something", "senderWorkerId": 1, "messageId": 1032}, 
    #         {"timeOffset": 509, "text": "@203371 was a good one", "senderWorkerId": 1, "messageId": 1033}, 
    #         {"timeOffset": 564, "text": "Ooh that seems cool! Thanks for the input. I'm ready to submit if you are.", "senderWorkerId": 0, "messageId": 1034}, 
    #         {"timeOffset": 571, "text": "It is animated, sci fi, and has action", "senderWorkerId": 1, "messageId": 1035}, 
    #         {"timeOffset": 579, "text": "Glad I could help", "senderWorkerId": 1, "messageId": 1036}, 
    #         {"timeOffset": 581, "text": "Nice", "senderWorkerId": 0, "messageId": 1037}, 
    #         {"timeOffset": 591, "text": "Take care, cheers!", "senderWorkerId": 0, "messageId": 1038}, 
    #         {"timeOffset": 608, "text": "bye", "senderWorkerId": 1, "messageId": 1039}], 
    #     "conversationId": "391", 
    #     "respondentWorkerId": 1, 
    #     "initiatorWorkerId": 0, 
    #     "initiatorQuestions": 
    #         {"203371": {"suggested": 1, "seen": 0, "liked": 1}, 
    #         "84779": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "122159": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "151313": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "191602": {"suggested": 0, "seen": 1, "liked": 1}, 
    #         "165710": {"suggested": 1, "seen": 0, "liked": 1}}
    # }

if __name__ == "__main__":
    
    filename ="../../data/raw/train_data.jsonl"
    process(filename, 'train')