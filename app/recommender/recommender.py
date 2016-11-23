class Recommender:

    def __init__(self, dao):
        self.dao = dao

    def get_similar_recipes(self, recipe):
        return self.dao.get_most_popular_recipes()
