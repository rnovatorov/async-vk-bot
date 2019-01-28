import os
import random
import operator

import trio
import async_vk_api
import async_vk_bot


class MathQuiz:

    def __init__(self, bot, peer_id, n_questions=5, difficulty=10):
        self.bot = bot
        self.peer_id = peer_id
        self.n_questions = n_questions
        self.difficulty = difficulty

    async def start(self):
        score = 0
        for question, correct_answer in self.generate_questions():
            await self.send(question)
            if await self.wait_answer() == correct_answer:
                score += 1
        await self.send(f'Your score is {score}/{self.n_questions}.')

    async def send(self, message):
        await self.bot.api.messages.send(
            peer_id=self.peer_id,
            message=message
        )

    async def wait_answer(self):
        event = await self.bot.wait(lambda e: (
            e['type'] == 'message_new'
            and
            e['object']['peer_id'] == self.peer_id
        ))
        return event['object']['text']

    def generate_questions(self):
        questions = []

        for _ in range(self.n_questions):
            a = random.randint(-self.difficulty, self.difficulty)
            b = random.randint(-self.difficulty, self.difficulty)
            op_name, op = random.choice([
                ('+', operator.add),
                ('-', operator.sub)
            ])
            question = f'{a} {op_name} {b} = ?'
            answer = str(op(a, b))
            questions.append((question, answer))

        return questions


class Router:

    def __init__(self, bot, start_cmd='/math_quiz'):
        self.bot = bot
        self.start_cmd = start_cmd
        self.peer_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async with self.bot.sub(lambda e: (
                e['type'] == 'message_new'
                and
                e['object']['text'] == self.start_cmd
                and
                e['object']['peer_id'] not in self.peer_ids
            )) as events:
                async for event in events:
                    peer_id = event['object']['peer_id']
                    await nursery.start(self.math_quiz, peer_id)

    async def math_quiz(self, peer_id, task_status=trio.TASK_STATUS_IGNORED):
        self.peer_ids.add(peer_id)

        task_status.started()
        math_quiz = MathQuiz(self.bot, peer_id)
        await math_quiz.start()

        self.peer_ids.remove(peer_id)


async def main():
    api = async_vk_api.make_api(
        access_token=os.getenv('VK_API_ACCESS_TOKEN'),
        version='5.89',
    )
    bot = async_vk_bot.make_bot(api)
    router = Router(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(router)


if __name__ == '__main__':
    trio.run(main)
