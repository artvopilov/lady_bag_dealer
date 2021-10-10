class Bag:
    def __init__(self, brand, model, color, price, origin_price, image_url, url):
        self.brand = brand
        self.model = model
        self.color = color
        self.price = price
        self.origin_price = origin_price
        self.image_url = image_url
        self.url = url

    def __repr__(self):
        return f'Brand: {self.brand},  Model: {self.model}, Color: {self.color}\n' \
               f'Price: {self.price}, Origin price: {self.origin_price}\n' \
               f'Image url: {self.image_url}, Url: {self.url}'

    def __eq__(self, other):
        return self.brand is not None and self.brand == other.brand \
               and self.model is not None and self.model == other.model \
               and self.color is not None and self.color == other.color


