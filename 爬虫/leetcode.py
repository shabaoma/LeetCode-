import json
import requests
import collections


class leetcode(object):

    session = requests.Session()
    question_list = []

    def read_question_list(self):
        path = "question_list.json"
        with open(path) as json_file:
            question_data = json.load(json_file)
            for x in question_data['stat_status_pairs']:
                self.question_list.append(x['stat']['question__title_slug'])

    def get_question_data(self, title):
        cookies = {'csrftoken': ''}
        self.session.headers.update({'referer': "https://leetcode.com/problems/"})
        self.session.headers.update({'x-csrftoken': ''})

        params = {
            "operationName": "questionData",
            "variables": {
                "titleSlug": title
            },
            "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    title\n    titleSlug\n    content\n    difficulty\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n}\n}\n}\n"
        }
        res = self.session.post("https://leetcode.com/graphql", json=params, cookies=cookies)
        return res.json()

    def run(self):
        self.read_question_list()

        difficulty_cnt = collections.defaultdict(int)
        question_topic_list = collections.defaultdict(list)
        topic_cnt = collections.defaultdict(int)
        topic_list = collections.defaultdict(list)
        for title in self.question_list:
            res = self.get_question_data(title)
            difficulty_cnt[res['data']['question']['difficulty']] += 1
            for topic in res['data']['question']['topicTags']:
                topic_cnt[topic['slug']] += 1
                topic_list[topic['slug']].append(res['data']['question']['title'])
                question_topic_list[res['data']['question']['title']].append(topic['slug'])

        with open("difficulty_cnt.json", "w+") as f:
            f.write(json.dumps(difficulty_cnt))
        with open("topic_cnt.json", "w+") as f:
            f.write(json.dumps(topic_cnt))
        with open("topic_list.json", "w+") as f:
            f.write(json.dumps(topic_list))
        with open("question_topic_list.json", "w+") as f:
            f.write(json.dumps(question_topic_list))

l = leetcode()
l.run()
