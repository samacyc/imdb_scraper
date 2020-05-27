import scrapy


class MovieItem (scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    number_of_vote = scrapy.Field()
    duration = scrapy.Field()
    category = scrapy.Field()
    About = scrapy.Field()
    Director = scrapy.Field()
    Writers = scrapy.Field()
    movie_type = scrapy.Field()

    recommendation = scrapy.Field()


class PostsSpyder(scrapy.Spider):

    name = 'drama'

    start_urls = ['https://www.imdb.com/search/title/?genres=drama']

    def parse(self, response):
        movies = response.css('.lister-item')
        for movie in movies:
            post_url = 'https://www.imdb.com' + \
                movie.css('a::attr(href)').get()
            yield scrapy.Request(post_url, callback=self.parse_indetail)
        # number of page
        for i in range(1, 10):
            next_page = 'https://www.imdb.com/search/title/?genres=drama&start={}'.format(
                i*50+1)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_indetail(self, response):
        instance_type = 'Movie'
        type_lookup = response.css('.subtext').css('a::text').getall()
        if 'TV Series' in response.css('.subtext').css('a::text')[len(type_lookup) - 1].get():
            instance_type = 'Serie'

        item = MovieItem()
        item['title'] = response.css('h1::text').get()
        item['movie_type'] = instance_type
        item['rating'] = response.css('.ratingValue').css('span::text').get()
        item['number_of_vote'] = response.css('.ratingValue').css(
            'strong::attr(title)').get().split('on')[1].split(' ')[1]
        item['duration'] = response.css('.subtext').css('time::text').get()
        item['category'] = response.css('.subtext').css('a::text').get()
        item['About'] = response.css('.summary_text::text').get()
        item['Director'] = response.css(
            '.credit_summary_item').css('a::text').get()
        item['Writers'] = response.css(
            '.credit_summary_item')[1].css('a::text').getall()
        item['recommendation'] = response.css('.rec_item').css(
            'a').css('img::attr(title)').getall()

        return item
