from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)


import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Всточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
	BookRecommendation(id=4, title="Автостопом по галактике"),
	BookRecommendation(id=5, title="Основание"),
	BookRecommendation(id=6, title="Имя розы"),
	BookRecommendation(id=7, title="Девять врат"),
	BookRecommendation(id=8, title="Тень ветра"),
	BookRecommendation(id=9, title="Ангелы и демоны"),
	BookRecommendation(id=10, title="Мастер и Маргарита"),
    ],

    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=11, title="Дюна"),
	BookRecommendation(id=12, title="Основание"),
	BookRecommendation(id=13, title="Невидимый человек"),
	BookRecommendation(id=14, title="Гиперион"),
	BookRecommendation(id=15, title="Нейромант"),
	BookRecommendation(id=16, title="Солярис"),
	BookRecommendation(id=17, title="Левиафан"),
	BookRecommendation(id=18, title="Марсианские хроники"),
	BookRecommendation(id=19, title="Игра Эндера"),
	BookRecommendation(id=20, title="451 по Фаренгейту"),
    ],

    BookCategory.SELF_HELP: [
        BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=22, title="Как завоевать друзей и оказывать влияние на людей"),
        BookRecommendation(id=23, title="Человек в поисках смысла"),
	BookRecommendation(id=24, title="Думай и богатей"),
	BookRecommendation(id=25, title="Пробуждение"),
	BookRecommendation(id=26, title="Сила настоящего"),
	BookRecommendation(id=27, title="Путь художника"),
	BookRecommendation(id=28, title="Магия утра"),
	BookRecommendation(id=29, title="Игра Эндера"),
	BookRecommendation(id=30, title="Сила подсознания"),
    ],
}


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()