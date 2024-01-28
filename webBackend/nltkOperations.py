import heapq
import re
import urllib.request

import bs4 as bs
import nltk


# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import BartForConditionalGeneration, BartTokenizer


def singleton(cls):
    instance = {}

    def getinstance():
        if cls not in instance:
            instance[cls] = cls()
        return instance[cls]

    return getinstance()


@singleton
class NltkOperations:
    ml_tokenizer = None
    model = None

    def pre_build(self, summarize_type=None):
        # if summarize_type == 'ml':
        #     print("Generating news via ML algorithm")
        #     model_dir = os.path.join(os.getcwd(), 'cnn-model-folder')
        #     # https://huggingface.co/facebook/bart-large-cnn
        #     self.ml_tokenizer = AutoTokenizer.from_pretrained(model_dir)
        #     self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        if summarize_type == 'ml':
            self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
            self.model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        nltk.download('punkt')
        nltk.download('stopwords')

    def get_summary(self, url, algo_type):
        try:
            article_text, formatted_article_text = self.scrap_url(url)
            if algo_type == "ml":
                return self.summarize_using_bart(article_text)
                # return self.summarize_using_ml(formatted_article_text, article_text)
            else:
                return self.summarize_using_word_frequency(formatted_article_text, article_text)
        except Exception as e:
            print("Exception occured", e)
            return None

    def summarize_using_ml(self, text, article_text):
        try:
            pass
            # batch = self.ml_tokenizer(text, return_tensors='pt')
            # generated_ids = self.model.generate(batch['input_ids'])
            # generated_sentence = self.ml_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
            # summary = '.'.join(generated_sentence)
            # summary_with_key_split = summary.replace('.', '--key-navneet--')
            # clean_summary = summary.encode("ascii", "ignore").decode()
            # html_summary = self.convert_to_li(summary_with_key_split)
            # return [clean_summary, html_summary]
        except Exception as e:
            print("Exception occured", e)
            return self.summarize_using_word_frequency(text, article_text)

    def summarize_using_word_frequency(self, formatted_article_text, article_text):
        try:
            sentence_list = nltk.sent_tokenize(article_text)
            stopwords = nltk.corpus.stopwords.words('english')
            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        length_split = len(sent.split(' '))
                        if len(sent.split(' ')) < 50:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]
            summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
            summary_with_key_split = '--key-navneet--'.join(summary_sentences)
            summary = ' '.join(summary_sentences)
            clean_summary = summary.encode("ascii", "ignore").decode()
            html_summary = self.convert_to_li(summary_with_key_split)
            return [clean_summary, html_summary]
        except Exception as e:
            print(e.__traceback__)
            # print(traceback.print_stack(e))
            return None

    def scrap_url(self, url):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
            # scraped_data = urllib.request.urlopen(url)
            # article = scraped_data.read()
            article = urllib.request.urlopen(req).read()
            parsed_article = bs.BeautifulSoup(article, 'lxml').find('main')
            if parsed_article is None:
                article = urllib.request.urlopen(req).read()
                parsed_article = bs.BeautifulSoup(article, 'lxml').find('article')  # Used for techcrunch only
                if parsed_article is None:
                    return None
            paragraphs = parsed_article.find_all('p')
            article_text = ""
            for p in paragraphs:
                article_text += p.text
            # Removing Square Brackets and Extra Spaces
            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)
            article_text = article_text.encode("utf-8").decode()
            # Removing special characters and digits
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            return article_text, formatted_article_text
        except Exception as e:
            print("Something went wrong while scrapping..", e)
            return None

    def convert_to_li(self, summary):
        try:
            # Might need to split at .space because the bug where the sentence splits middle is still present
            summary_content = summary.split('--key-navneet--')[:-1]
            if len(summary_content) == 0 and len(summary) > 1:
                summary_content.append(summary)
            returning_string = "<ul>"
            for items in summary_content:
                returning_string += "<li>" + items + "</li>"
            returning_string += "</ul>"
            return returning_string
        except Exception as e:
            print("Exception while converting to list..",e)

    def remove_non_ascii(self, s):
        return "".join(c for c in s if ord(c) < 128)

    def remove_special_char(self, s):
        s = s.strip()
        urls = re.sub('\W+','-', s)
        return urls

    def clean(self, s):
        try:
            clean_string = self.remove_non_ascii(s)
            clean_string = clean_string.replace(':', '').replace('-', '').replace('"', '').replace("'", '').replace('\r',
                                                                                                                    '').replace(
                '\n', '')
            clean_string = re.sub('<[^<]+?>', '', clean_string)  # Removing html here
            return clean_string
        except Exception as e:
            return ""

    def get_url(self, url):
        url = self.remove_special_char(url)
        url = self.remove_non_ascii(url)
        url = url.rstrip('/')
        clean_url = url.split('/')
        clean_url = clean_url[len(clean_url) - 1]
        if clean_url.count('.') > 0:
            clean_url = clean_url.split('.')[0]
        return clean_url

    def summarize_using_bart(self, input_text):
        # Tokenize input text
        inputs = self.tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)

        # Generate summary
        summary_ids = self.model.generate(inputs, max_length=400, num_beams=6, length_penalty=2.0, early_stopping=True)
        generated_sentence = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        summary_with_key_split = generated_sentence.replace('.', '--key-navneet--')
        # clean_summary = summary.encode("ascii", "ignore").decode()
        html_summary = self.convert_to_li(summary_with_key_split)
        return [generated_sentence, html_summary]
