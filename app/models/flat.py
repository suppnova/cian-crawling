class Flat:
    def __init__(self, container):
        self.address = ", ".join(
            (c.text for c in container.find_all("a", {"data-name": "GeoLabel"}))
        )
        self.main_price = int(
            container.find("span", {"data-mark": "MainPrice"})
            .text[:-1]
            .replace(" ", "")
        )
        self.price_per_m2 = int(
            container.find("p", {"data-mark": "PriceInfo"}).text[:-5].replace(" ", "")
        )
        self.area = round(self.main_price / self.price_per_m2, 2)
